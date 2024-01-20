import inspect
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor

import ophyd
from bec_lib import Alarms, BECService, MessageEndpoints, bec_logger, messages
from bec_lib.connector import ConnectorBase
from bec_lib.device import OnFailure
from bec_lib.messages import BECStatus
from ophyd import OphydObject, Staged
from ophyd.utils import errors as ophyd_errors

from device_server.devices.devicemanager import DeviceManagerDS
from device_server.rpc_mixin import RPCMixin

logger = bec_logger.logger

consumer_stop = threading.Event()


class DisabledDeviceError(Exception):
    """Exception raised when a disabled device is accessed"""


class InvalidDeviceError(Exception):
    """Exception raised when an invalid device is accessed"""


class DeviceServer(RPCMixin, BECService):
    """DeviceServer using ophyd as a service
    This class is intended to provide a thin wrapper around ophyd and the devicemanager. It acts as the entry point for other services
    """

    def __init__(self, config, connector_cls: ConnectorBase) -> None:
        super().__init__(config, connector_cls, unique_service=True)
        self._tasks = []
        self.device_manager = None
        self.threads = []
        self.sig_thread = None
        self.sig_thread = self.connector.consumer(
            MessageEndpoints.scan_queue_modification(),
            cb=self.consumer_interception_callback,
            parent=self,
        )
        self.sig_thread.start()
        self.executor = ThreadPoolExecutor(max_workers=4)
        self._start_device_manager()

    def _start_device_manager(self):
        self.device_manager = DeviceManagerDS(self, status_cb=self.update_status)
        self.device_manager.initialize(self.bootstrap_server)

    def start(self) -> None:
        """start the device server"""
        if consumer_stop.is_set():
            consumer_stop.clear()

        self.threads = [
            self.connector.consumer(
                MessageEndpoints.device_instructions(),
                event=consumer_stop,
                cb=self.instructions_callback,
                parent=self,
            )
        ]
        for thread in self.threads:
            thread.start()
        self.status = BECStatus.RUNNING

    def update_status(self, status: BECStatus):
        """update the status of the device server"""
        self.status = status

    def stop(self) -> None:
        """stop the device server"""
        consumer_stop.set()
        for thread in self.threads:
            thread.join()
        self.status = BECStatus.IDLE

    def shutdown(self) -> None:
        """shutdown the device server"""
        super().shutdown()
        self.stop()
        self.sig_thread.signal_event.set()
        self.sig_thread.join()
        self.device_manager.shutdown()

    def _update_device_metadata(self, instr) -> None:
        devices = instr.content["device"]
        if not isinstance(devices, list):
            devices = [devices]
        for dev in devices:
            device_root = dev.split(".")[0]
            self.device_manager.devices.get(device_root).metadata = instr.metadata

    @staticmethod
    def consumer_interception_callback(msg, *, parent, **_kwargs) -> None:
        """callback for receiving scan modifications / interceptions"""
        mvalue = messages.ScanQueueModificationMessage.loads(msg.value)
        if mvalue is None:
            logger.warning("Failed to parse scan queue modification message.")
            return
        logger.info(f"Receiving: {mvalue.content}")
        if mvalue.content.get("action") in ["pause", "abort", "halt"]:
            parent.stop_devices()

    def stop_devices(self) -> None:
        """stop all enabled devices"""
        logger.info("Stopping devices after receiving 'abort' request.")
        self.status = BECStatus.BUSY
        for dev in self.device_manager.devices.enabled_devices:
            if dev.read_only:
                # don't stop devices that we haven't set
                continue
            if hasattr(dev.obj, "stop"):
                dev.obj.stop()
        self.status = BECStatus.RUNNING

    def _assert_device_is_enabled(self, instructions: messages.DeviceInstructionMessage) -> None:
        devices = instructions.content["device"]

        if isinstance(devices, str):
            devices = [devices]

        for dev in devices:
            dev = dev.split(".")[0]
            if not self.device_manager.devices[dev].enabled:
                raise DisabledDeviceError(f"Cannot access disabled device {dev}.")

    def _assert_device_is_valid(self, instructions: messages.DeviceInstructionMessage) -> None:
        devices = instructions.content["device"]
        if not devices:
            raise InvalidDeviceError("At least one device must be specified.")
        if isinstance(devices, str):
            devices = [devices]
        for dev in devices:
            dev = dev.split(".")[0]
            if dev not in self.device_manager.devices:
                raise InvalidDeviceError(f"There is no device with the name {dev}.")

    def handle_device_instructions(self, msg: str) -> None:
        """Parse a device instruction message and handle the requested action. Action
        types are set, read, rpc, kickoff or trigger.

        Args:
            msg (str): A DeviceInstructionMessage string containing the action and its parameters

        """
        action = None
        try:
            instructions = messages.DeviceInstructionMessage.loads(msg)
            if not instructions.content["device"]:
                return
            action = instructions.content["action"]
            self._assert_device_is_valid(instructions)
            if action != "rpc":
                # rpc has its own error handling
                self._assert_device_is_enabled(instructions)
            self._update_device_metadata(instructions)

            if action == "set":
                self._set_device(instructions)
            elif action == "read":
                self._read_device(instructions)
            elif action == "rpc":
                self.run_rpc(instructions)
            elif action == "kickoff":
                self._kickoff_device(instructions)
            elif action == "complete":
                self._complete_device(instructions)
            elif action == "trigger":
                self._trigger_device(instructions)
            elif action == "stage":
                self._stage_device(instructions)
            elif action == "unstage":
                self._unstage_device(instructions)
            elif action == "pre_scan":
                self._pre_scan(instructions)
            else:
                logger.warning(f"Received unknown device instruction: {instructions}")
        except ophyd_errors.LimitError as limit_error:
            content = traceback.format_exc()
            logger.error(content)
            self.connector.raise_alarm(
                severity=Alarms.MAJOR,
                source=instructions.content,
                content=content,
                alarm_type=limit_error.__class__.__name__,
                metadata=instructions.metadata,
            )
        except Exception as exc:  # pylint: disable=broad-except
            if action == "rpc":
                self._send_rpc_exception(exc, instructions)
            else:
                content = traceback.format_exc()
                self.connector.log_error({"source": msg, "message": content})
                logger.error(content)
                self.connector.raise_alarm(
                    severity=Alarms.MAJOR,
                    source=instructions.content,
                    content=content,
                    alarm_type=exc.__class__.__name__,
                    metadata=instructions.metadata,
                )

    @staticmethod
    def instructions_callback(msg, *, parent, **_kwargs) -> None:
        """callback for handling device instructions"""
        parent.executor.submit(parent.handle_device_instructions, msg.value)

    def _trigger_device(self, instr: messages.DeviceInstructionMessage) -> None:
        logger.debug(f"Trigger device: {instr}")
        devices = instr.content["device"]
        if not isinstance(devices, list):
            devices = [devices]
        for dev in devices:
            obj = self.device_manager.devices.get(dev)
            obj.metadata = instr.metadata
            status = obj.obj.trigger()
            status.__dict__["instruction"] = instr
            status.add_callback(self._status_callback)

    def _kickoff_device(self, instr: messages.DeviceInstructionMessage) -> None:
        logger.debug(f"Kickoff device: {instr}")
        obj = self.device_manager.devices.get(instr.content["device"]).obj
        kickoff_args = inspect.getfullargspec(obj.kickoff).args
        kickoff_parameter = instr.content["parameter"].get("configure", {})
        if len(kickoff_args) > 1:
            obj.kickoff(metadata=instr.metadata, **kickoff_parameter)
            return
        obj.configure(kickoff_parameter)
        status = obj.kickoff()
        status.__dict__["instruction"] = instr
        status.add_callback(self._status_callback)

    def _complete_device(self, instr: messages.DeviceInstructionMessage) -> None:
        if instr.content["device"] is None:
            devices = [dev.name for dev in self.device_manager.devices.enabled_devices]
        else:
            devices = instr.content["device"]
            if not isinstance(devices, list):
                devices = [devices]
        for dev in devices:
            obj = self.device_manager.devices.get(dev).obj
            if not hasattr(obj, "complete"):
                # if the device does not have a complete method, we assume that it is done
                status = ophyd.StatusBase()
                status.obj = obj
                status.set_finished()
            else:
                logger.debug(f"Completing device: {dev}")
                status = obj.complete()
            status.__dict__["instruction"] = instr
            status.add_callback(self._status_callback)

    def _set_device(self, instr: messages.DeviceInstructionMessage) -> None:
        device_obj = self.device_manager.devices.get(instr.content["device"])
        if device_obj.read_only:
            raise DisabledDeviceError(
                f"Setting the device {device_obj.name} is currently disabled."
            )
        logger.debug(f"Setting device: {instr}")
        val = instr.content["parameter"]["value"]
        obj = self.device_manager.devices.get(instr.content["device"]).obj
        # self.device_manager.add_req_done_sub(obj)
        status = obj.set(val)
        status.__dict__["instruction"] = instr
        status.add_callback(self._status_callback)

    def _pre_scan(self, instr: messages.DeviceInstructionMessage) -> None:
        devices = instr.content["device"]
        if not isinstance(devices, list):
            devices = [devices]
        pipe = self.producer.pipeline()
        for dev in devices:
            obj = self.device_manager.devices.get(dev)
            obj.metadata = instr.metadata
            if hasattr(obj.obj, "pre_scan"):
                obj.obj.pre_scan()
            dev_msg = messages.DeviceReqStatusMessage(
                device=dev, success=True, metadata=instr.metadata
            ).dumps()
            self.producer.set_and_publish(MessageEndpoints.device_req_status(dev), dev_msg, pipe)
        pipe.execute()

    def _status_callback(self, status):
        pipe = self.producer.pipeline()
        if hasattr(status, "device"):
            device_name = status.device.root.name
        else:
            device_name = status.obj.root.name
        dev_msg = messages.DeviceReqStatusMessage(
            device=device_name, success=status.success, metadata=status.instruction.metadata
        ).dumps()
        logger.debug(f"req status for device {device_name}: {status.success}")
        self.producer.set_and_publish(
            MessageEndpoints.device_req_status(device_name), dev_msg, pipe
        )
        response = status.instruction.metadata.get("response")
        if response:
            self.producer.lpush(
                MessageEndpoints.device_req_status(status.instruction.metadata["RID"]),
                dev_msg,
                pipe,
                expire=18000,
            )

        pipe.execute()

    def _read_device(self, instr: messages.DeviceInstructionMessage) -> None:
        # check performance -- we might have to change it to a background thread
        devices = instr.content["device"]
        if not isinstance(devices, list):
            devices = [devices]

        self._read_and_update_devices(devices, instr.metadata)

    def _read_and_update_devices(self, devices: list[str], metadata: dict) -> list:
        start = time.time()
        pipe = self.producer.pipeline()
        signal_container = []
        for dev in devices:
            device_root = dev.split(".")[0]
            self.device_manager.devices.get(device_root).metadata = metadata
            obj = self.device_manager.devices.get(device_root).obj
            try:
                signals = obj.read()
                signal_container.append(signals)
            except Exception as exc:
                signals = self._retry_obj_method(dev, obj, "read", exc)

            self.producer.set_and_publish(
                MessageEndpoints.device_read(device_root),
                messages.DeviceMessage(signals=signals, metadata=metadata).dumps(),
                pipe,
            )
            self.producer.set_and_publish(
                MessageEndpoints.device_readback(device_root),
                messages.DeviceMessage(signals=signals, metadata=metadata).dumps(),
                pipe,
            )
            self.producer.set(
                MessageEndpoints.device_status(device_root),
                messages.DeviceStatusMessage(
                    device=device_root, status=0, metadata=metadata
                ).dumps(),
                pipe,
            )
        pipe.execute()
        logger.debug(
            f"Elapsed time for reading and updating status info: {(time.time()-start)*1000} ms"
        )
        return signal_container

    def _read_config_and_update_devices(self, devices: list[str], metadata: dict) -> list:
        start = time.time()
        pipe = self.producer.pipeline()
        signal_container = []
        for dev in devices:
            self.device_manager.devices.get(dev).metadata = metadata
            obj = self.device_manager.devices.get(dev).obj
            try:
                signals = obj.read_configuration()
                signal_container.append(signals)
            except Exception as exc:
                signals = self._retry_obj_method(dev, obj, "read_configuration", exc)
            self.producer.set_and_publish(
                MessageEndpoints.device_read_configuration(dev),
                messages.DeviceMessage(signals=signals, metadata=metadata).dumps(),
                pipe,
            )
        pipe.execute()
        logger.debug(
            f"Elapsed time for reading and updating status info: {(time.time()-start)*1000} ms"
        )
        return signal_container

    def _retry_obj_method(self, device: str, obj: OphydObject, method: str, exc: Exception) -> dict:
        self.device_manager.connector.raise_alarm(
            severity=Alarms.WARNING,
            alarm_type="Warning",
            source="DeviceServer",
            content=f"Failed to run {method} on device {device}.",
            metadata={},
        )
        device_root = device.split(".")[0]
        ds_dev = self.device_manager.devices.get(device_root)
        if ds_dev.on_failure == OnFailure.RAISE:
            raise exc

        if ds_dev.on_failure == OnFailure.RETRY:
            # try to read it again, may have been only a glitch
            signals = getattr(obj, method)()
        elif ds_dev.on_failure == OnFailure.BUFFER:
            # if possible, fall back to past readings
            logger.warning(
                f"Failed to run {method} on device {device_root}. Trying to load an old value."
            )
            if method == "read":
                old_msg = messages.DeviceMessage.loads(
                    self.producer.get(MessageEndpoints.device_read(device_root))
                )
            elif method == "read_configuration":
                old_msg = messages.DeviceMessage.loads(
                    self.producer.get(MessageEndpoints.device_read_configuration(device_root))
                )
            else:
                raise ValueError(f"Unknown method {method}.")
            if not old_msg:
                raise exc
            signals = old_msg.content["signals"]
        return signals

    def _stage_device(self, instr: messages.DeviceInstructionMessage) -> None:
        devices = instr.content["device"]
        if not isinstance(devices, list):
            devices = [devices]

        pipe = self.producer.pipeline()
        for dev in devices:
            obj = self.device_manager.devices[dev].obj
            if hasattr(obj, "_staged"):
                # pylint: disable=protected-access
                if obj._staged == Staged.yes:
                    logger.info(f"Device {obj.name} was already staged and will be first unstaged.")
                    self.device_manager.devices[dev].obj.unstage()
                self.device_manager.devices[dev].obj.stage()
            self.producer.set(
                MessageEndpoints.device_staged(dev),
                messages.DeviceStatusMessage(device=dev, status=1, metadata=instr.metadata).dumps(),
                pipe,
            )
        pipe.execute()

    def _unstage_device(self, instr: messages.DeviceInstructionMessage) -> None:
        devices = instr.content["device"]
        if not isinstance(devices, list):
            devices = [devices]

        pipe = self.producer.pipeline()
        for dev in devices:
            obj = self.device_manager.devices[dev].obj
            if hasattr(obj, "_staged"):
                # pylint: disable=protected-access
                if obj._staged == Staged.yes:
                    self.device_manager.devices[dev].obj.unstage()
                else:
                    logger.debug(f"Device {obj.name} was already unstaged.")
            self.producer.set(
                MessageEndpoints.device_staged(dev),
                messages.DeviceStatusMessage(device=dev, status=0, metadata=instr.metadata).dumps(),
                pipe,
            )
        pipe.execute()
