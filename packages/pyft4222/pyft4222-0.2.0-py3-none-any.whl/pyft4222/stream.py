"""Module encapsulating all possible FT4222 USB stream modes.

FT4222 chip can be set into one of 4 possible modes externally.
Each mode has a specific set of available USB stream interfaces.

Each class represents a specific mode of stream and encapsulates it.

Important:
    Do not instantiate classes in this module directly. Use functions
    from the ft4222 module instead.
"""

from enum import Enum, auto
from typing import Literal, Union

from koda import Ok

from pyft4222.gpio import Gpio
from pyft4222.handle import GenericHandle
from pyft4222.i2c.master import I2CMaster
from pyft4222.i2c.slave import I2CSlave
from pyft4222.spi.master import SpiMasterMulti, SpiMasterSingle
from pyft4222.spi.slave import SpiSlaveProto, SpiSlaveRaw
from pyft4222.wrapper import Ft4222Exception, Ft4222Status, FtHandle, gpio
from pyft4222.wrapper.i2c import master as i2c_master
from pyft4222.wrapper.i2c import slave as i2c_slave
from pyft4222.wrapper.spi import master as spi_master
from pyft4222.wrapper.spi import slave as spi_slave


class InterfaceType(Enum):
    """FT4222 USB interface type.

    The FT4222 chip can be set (externally) into 4 distinct modes,
    each supporting a certain functions over number of USB streams:

    +---------------+-------------+------------+------------+-------------+
    |               |   MODE 0    |   MODE 1   |   MODE 2   |   MODE 3    |
    +---------------+-------------+------------+------------+-------------+
    | Stream #0 (A) | Data Stream | SPI Master | SPI Master | Data Stream |
    | Stream #1 (B) | GPIO        | SPI Master | SPI Master | N/A         |
    | Stream #2 (C) | N/A         | SPI Master | SPI Master | N/A         |
    | Stream #3 (D) | N/A         | GPIO       | SPI Master | N/A         |
    +---------------+-------------+------------+------------+-------------+

    To select the configuration mode/interface type, you must tie the
    DCNF1, DCNF0 pins to corresponding values.

    More info can be found in the FT4222H Datasheet:
    https://ftdichip.com/wp-content/uploads/2020/07/DS_FT4222H.pdf
    """

    DATA_STREAM = auto()
    """All serial protocols are supported in this mode, excluding GPIO"""
    GPIO = auto()
    """Only GPIO is supported"""
    SPI_MASTER = auto()
    """Only SPI Master is supported"""


class ProtocolStream(GenericHandle[FtHandle, "ProtocolStream"]):
    """A class representing an open FT4222 stream in "Data Stream" mode.

    Attributes:
        tag:    Can be used to disambiguate between different stream types
    """

    tag: Literal[InterfaceType.DATA_STREAM]

    def __init__(self, ft_handle: FtHandle):
        """Initialize ProtocolHandle with given FtHandle.

        Args:
            ft_handle:          Handle to an opened FT4222 device

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            ProtocolHandle:     FT4222 USB stream handle
        """
        super().__init__(ft_handle)
        self.tag = InterfaceType.DATA_STREAM

    def init_single_spi_master(
        self,
        clk_div: spi_master.ClkDiv,
        clk_polarity: spi_master.ClkPolarity,
        clk_phase: spi_master.ClkPhase,
        sso_map: spi_master.SsoMap,
    ) -> SpiMasterSingle["ProtocolStream"]:
        """Initialize SPI Master mode, using single data line.

        Args:
            clk_div:        Divisor of system clock to create serial clock
            clk_polarity:   Serial clock polarity
            clk_phase:      Serial clock phase
            sso_map:        Slave select map

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            SpiMasterSingle:    SPI Master mode handle
        """
        if self._handle is not None:
            result = spi_master.init(
                self._handle,
                spi_master.IoMode.SINGLE,
                clk_div,
                clk_polarity,
                clk_phase,
                sso_map,
            )
            if isinstance(result, Ok):
                self._handle = None
                return SpiMasterSingle(result.val, self)
            else:
                raise Ft4222Exception(result.val)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)

    def init_dual_spi_master(
        self,
        clk_div: spi_master.ClkDiv,
        clk_polarity: spi_master.ClkPolarity,
        clk_phase: spi_master.ClkPhase,
        sso_map: spi_master.SsoMap,
    ) -> SpiMasterMulti["ProtocolStream"]:
        """Initialize SPI Master mode, using two data lines.

        Args:
            clk_div:        Divisor of system clock to create serial clock
            clk_polarity:   Serial clock polarity
            clk_phase:      Serial clock phase
            sso_map:        Slave select map

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            SpiMasterMulti:     SPI Master mode handle
        """
        if self._handle is not None:
            result = spi_master.init(
                self._handle,
                spi_master.IoMode.DUAL,
                clk_div,
                clk_polarity,
                clk_phase,
                sso_map,
            )
            if isinstance(result, Ok):
                self._handle = None
                return SpiMasterMulti(result.val, self)
            else:
                raise Ft4222Exception(result.val)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)

    def init_quad_spi_master(
        self,
        clk_div: spi_master.ClkDiv,
        clk_polarity: spi_master.ClkPolarity,
        clk_phase: spi_master.ClkPhase,
        sso_map: spi_master.SsoMap,
    ) -> SpiMasterMulti["ProtocolStream"]:
        """Initialize SPI Master mode, using four data lines.

        Args:
            clk_div:        Divisor of system clock to create serial clock
            clk_polarity:   Serial clock polarity
            clk_phase:      Serial clock phase
            sso_map:        Slave select map

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            SpiMasterMulti:     SPI Master mode handle
        """
        if self._handle is not None:
            result = spi_master.init(
                self._handle,
                spi_master.IoMode.QUAD,
                clk_div,
                clk_polarity,
                clk_phase,
                sso_map,
            )
            if isinstance(result, Ok):
                self._handle = None
                return SpiMasterMulti(result.val, self)
            else:
                raise Ft4222Exception(result.val)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)

    def init_raw_spi_slave(self) -> SpiSlaveRaw["ProtocolStream"]:
        """Initialize SPI Slave in raw mode.

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            SpiSlaveRaw:        SPI Slave raw mode handle
        """
        if self._handle is not None:
            result = spi_slave.init_ex(
                self._handle,
                spi_slave.IoProtocol.NO_PROTOCOL,
            )
            if isinstance(result, Ok):
                self._handle = None
                return SpiSlaveRaw(result.val, self)
            else:
                raise Ft4222Exception(result.val)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)

    def init_proto_spi_slave(
        self,
        proto_type: Union[
            Literal[spi_slave.IoProtocol.NO_ACK],
            Literal[spi_slave.IoProtocol.WITH_PROTOCOL],
        ],
    ) -> SpiSlaveProto["ProtocolStream"]:
        """Initialize SPI Slave in selected protocol mode.

        For protocol details, see:
        https://www.ftdichip.com/Support/Documents/AppNotes/AN_329_User_Guide_for_LibFT4222.pdf

        Protocol details can be found in chapter 3.4.

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            SpiSlaveProto:      SPI Slave protocol mode handle
        """
        if self._handle is not None:
            result = spi_slave.init_ex(self._handle, proto_type)
            if isinstance(result, Ok):
                self._handle = None
                return SpiSlaveProto(result.val, self)
            else:
                raise Ft4222Exception(result.val)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)

    def init_i2c_master(self, kbps: int) -> I2CMaster["ProtocolStream"]:
        """Initialize I2C Master.

        Args:
            kbps:   I2C clock/transmission speed in kbit/s (60 - 3400)

        Raises:
            Ft4222Exception:    In case of an unexpected error

        Returns:
            I2CMaster:          I2C Master handle
        """
        if self._handle is not None:
            result = i2c_master.init(self._handle, kbps)
            if isinstance(result, Ok):
                self._handle = None
                return I2CMaster(result.val, self)
            else:
                raise Ft4222Exception(result.val)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)

    def init_i2c_slave(self) -> I2CSlave["ProtocolStream"]:
        """Initialize I2C Slave.

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            I2CSlave:           I2C Slave handle
        """
        if self._handle is not None:
            result = i2c_slave.init(self._handle)
            if isinstance(result, Ok):
                self._handle = None
                return I2CSlave(result.val, self)
            else:
                raise Ft4222Exception(result.val)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)


class GpioStream(GenericHandle[FtHandle, "GpioStream"]):
    """A class representing an open FT4222 stream in "GPIO" mode.

    Attributes:
        tab:    Can be used to disambiguate between different stream types
    """

    tag: Literal[InterfaceType.GPIO]

    def __init__(self, ft_handle: FtHandle):
        """Initialize GpioHandle with given FtHandle.

        Args:
            ft_handle:          Handle to an opened FT4222 device
        """
        super().__init__(ft_handle)
        self.tag = InterfaceType.GPIO

    def init_gpio(self, dirs: gpio.DirTuple) -> Gpio["GpioStream"]:
        """Initialize GPIO.

        Args:
            dirs:       A 4-tuple selecting the direction of associated GPIO pin

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            Gpio:               GPIO handle
        """
        if self._handle is not None:
            result = gpio.init(self._handle, dirs)
            if isinstance(result, Ok):
                self._handle = None
                return Gpio(result.val, self)
            else:
                raise Ft4222Exception(result.val)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)


class SpiStream(GenericHandle[FtHandle, "SpiStream"]):
    """A class representing an open FT4222 stream in "SPI Master" mode.

    Attributes:
        tag:    Can be used to disambiguate between different stream types

    """

    tag: Literal[InterfaceType.SPI_MASTER]

    def __init__(self, ft_handle: FtHandle):
        """Initialize SpiMasterHandle with given FtHandle.

        Args:
            ft_handle:          Handle to an opened FT4222 device

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            SpiMasterHandle
        """
        super().__init__(ft_handle)
        self.tag = InterfaceType.SPI_MASTER

    def init_single_spi_master(
        self,
        clk_div: spi_master.ClkDiv,
        clk_polarity: spi_master.ClkPolarity,
        clk_phase: spi_master.ClkPhase,
        sso_map: spi_master.SsoMap,
    ) -> SpiMasterSingle["SpiStream"]:
        """Initialize SPI Master mode, using single data line.

        Args:
            clk_div:        Divisor of system clock to create serial clock
            clk_polarity:   Serial clock polarity
            clk_phase:      Serial clock phase
            sso_map:        Slave select map

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            SpiMasterSingle:    SPI Master mode handle
        """
        if self._handle is not None:
            result = spi_master.init(
                self._handle,
                spi_master.IoMode.SINGLE,
                clk_div,
                clk_polarity,
                clk_phase,
                sso_map,
            )
            if isinstance(result, Ok):
                self._handle = None
                return SpiMasterSingle(result.val, self)
            else:
                raise Ft4222Exception(result.val)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)

    def init_dual_spi_master(
        self,
        clk_div: spi_master.ClkDiv,
        clk_polarity: spi_master.ClkPolarity,
        clk_phase: spi_master.ClkPhase,
        sso_map: spi_master.SsoMap,
    ) -> SpiMasterMulti["SpiStream"]:
        """Initialize SPI Master mode, using two data lines.

        Args:
            clk_div:        Divisor of system clock to create serial clock
            clk_polarity:   Serial clock polarity
            clk_phase:      Serial clock phase
            sso_map:        Slave select map

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            SpiMasterMulti:     SPI Master mode handle
        """
        if self._handle is not None:
            result = spi_master.init(
                self._handle,
                spi_master.IoMode.DUAL,
                clk_div,
                clk_polarity,
                clk_phase,
                sso_map,
            )
            if isinstance(result, Ok):
                self._handle = None
                return SpiMasterMulti(result.val, self)
            else:
                raise Ft4222Exception(result.val)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)

    def init_quad_spi_master(
        self,
        clk_div: spi_master.ClkDiv,
        clk_polarity: spi_master.ClkPolarity,
        clk_phase: spi_master.ClkPhase,
        sso_map: spi_master.SsoMap,
    ) -> SpiMasterMulti["SpiStream"]:
        """Initialize SPI Master mode, using four data lines.

        Args:
            clk_div:        Divisor of system clock to create serial clock
            clk_polarity:   Serial clock polarity
            clk_phase:      Serial clock phase
            sso_map:        Slave select map

        Raises:
            Ft4222Exception:    In case of unexpected error

        Returns:
            SpiMasterMulti:     SPI Master mode handle
        """
        if self._handle is not None:
            result = spi_master.init(
                self._handle,
                spi_master.IoMode.QUAD,
                clk_div,
                clk_polarity,
                clk_phase,
                sso_map,
            )
            if isinstance(result, Ok):
                self._handle = None
                return SpiMasterMulti(result.val, self)
            else:
                raise Ft4222Exception(result.val)
        else:
            raise Ft4222Exception(Ft4222Status.INVALID_HANDLE)
