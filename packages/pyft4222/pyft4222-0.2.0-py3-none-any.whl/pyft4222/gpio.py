from typing import Generic, List

from pyft4222.handle import GenericProtocolHandle, StreamHandleType
from pyft4222.wrapper import Ft4222Exception, Ft4222Status, GpioTrigger
from pyft4222.wrapper.gpio import (
    GpioHandle,
    PortId,
    get_trigger_status,
    read,
    read_trigger_queue,
    set_input_trigger,
    set_waveform_mode,
    write,
)


class Gpio(
    Generic[StreamHandleType],
    GenericProtocolHandle[GpioHandle, "Gpio", StreamHandleType],
):
    """A class encapsulating GPIO functions."""

    def __init__(self, ft_handle: GpioHandle, stream_handle: StreamHandleType):
        """Initialize the class with given FT4222 handle and a mode class type.

        Args:
            ft_handle:      FT4222 handle initialized in any SPI Master mode
            stream_handle:  Calling stream mode handle. Used in 'uninitialize()' method.
        """
        super().__init__(ft_handle, stream_handle)

    def read(self, port_id: PortId) -> bool:
        """Read state of the given GPIO port.

        Args:
            port_id:            ID of the port to read

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            bool:               Port state (True -> '1', False -> '0')
        """
        if self._handle is not None:
            return read(self._handle, port_id)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "GPIO has been uninitialized!"
            )

    def write(self, port_id: PortId, state: bool) -> None:
        """Set state of the given GPIO port.

        Args:
            port_id:    ID of the port to set
            state:      New port state (True -> '1', False -> '0')

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is not None:
            write(self._handle, port_id, state)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "GPIO has been uninitialized!"
            )

    def set_input_trigger(self, port_id: PortId, triggers: GpioTrigger) -> None:
        """Set software trigger conditions for the selected GPIO port.

        Args:
            port_id:        GPIO port ID
            triggers:       OR-map of triggers to enable

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is not None:
            set_input_trigger(self._handle, port_id, triggers)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "GPIO has been uninitialized!"
            )

    def get_queued_trigger_event_count(self, port_id: PortId) -> int:
        """Get the size of trigger event queue.

        Args:
            port_id:            GPIO port ID

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            int:                Number of pending events in the event queue
        """
        if self._handle is not None:
            return get_trigger_status(self._handle, port_id)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "GPIO has been uninitialized!"
            )

    def read_trigger_queue(
        self, port_id: PortId, event_read_count: int
    ) -> List[GpioTrigger]:
        """Read events from the trigger event queue.

        Args:
            port_id:            GPIO port ID
            event_read_count:   Number of events to read from queue

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            List[GpioTrigger]:  List of trigger events
        """
        if self._handle is not None:
            return read_trigger_queue(self._handle, port_id, event_read_count)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "GPIO has been uninitialized!"
            )

    def set_waveform_mode(self, enable: bool) -> None:
        """Enable or disable the waveform mode.

        TODO: Add description

        Args:
            enable:             Enable waveform mode?

        Raises:
            Ft4222Exception:    In case of unexpected error
        """
        if self._handle is not None:
            set_waveform_mode(self._handle, enable)
        else:
            raise Ft4222Exception(
                Ft4222Status.DEVICE_NOT_OPENED, "GPIO has been uninitialized!"
            )
