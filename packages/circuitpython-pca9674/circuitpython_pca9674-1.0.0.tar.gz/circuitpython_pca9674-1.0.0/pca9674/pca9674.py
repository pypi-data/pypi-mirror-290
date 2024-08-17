# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2024 Finn Scheller
#
# SPDX-License-Identifier: MIT
"""
`pca9674`
================================================================================
CircuitPython module for the NXP PCA9674 and PCA9674A I2C I/O extenders.

* Author(s): Finn Scheller

Implementation Notes
--------------------

**Hardware:**

* Product page https://www.nxp.com/products/interfaces/ic-spi-i3c-interface-devices/general-purpose-i-o-gpio/remote-8-bit-i-o-expander-for-fm-plus-ic-bus-with-interrupt:PCA9674_PCA9674A
* Data sheet https://www.nxp.com/docs/en/data-sheet/PCA9674_PCA9674A.pdf

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

# imports

__version__ = "1.0.0"
__repo__ = "https://github.com/XENONFFM/CircuitPython_PCA9674.git"

from adafruit_bus_device import i2c_device
from micropython import const

from .digital_inout import DigitalInOut

try:
    from busio import I2C
except ImportError:
    pass

_PCA9674_ADDRESS = const(0x10)
_BUFFER = bytearray(1)


class PCA9674:
    """Supports PCA9674(A) instance on specified I2C bus and optionally
    at the specified I2C address.

        :param ~I2C i2c: The i2c bus
        :param int address: The I2C address of the device
        :param int pin_config: The initial pin configuration, defaults to 0x00 (all pins as outputs)

        Configure each pin as input (0) or output (1). To set all pins as inputs, use 0xFF.
        The PCA9674(A) has 8 pins, numbered 1-8.
        The least significant bit (LSB) corresponds to pin 1.

        Example: To set pins 1, 2, 5, 6 as outputs and 3, 4, 7, 8 as inputs,
        use 0xF0 (in binary: 0b11001100).

    """

    def __init__(self, i2c: I2C, address: int = _PCA9674_ADDRESS, pin_config=0x00):
        self.i2c = i2c
        self._device = i2c_device.I2CDevice(i2c, address)
        self.address = address
        self.io_dir = pin_config  # set all pins as outputs

    def pin_mode(self, pin: int, mode: int):
        if pin < 1 or pin > 8:
            raise ValueError("Pin number must be between 1 and 8")
        if mode is not self.OUTPUT or mode is not self.INPUT:
            raise ValueError("Mode must be either 'OUTPUT' or 'INPUT'")
        try:
            self.i2c.try_lock()
            self.io_dir = self.io_dir and mode << pin
            self.i2c.writeto(self.address, self.io_dir)
        finally:
            self.i2c.unlock()

    def readPins(self):
        try:
            self.i2c.try_lock()
            read_byte = bytearray(1)
            self.i2c.readfrom_into(self.address, read_byte)
        finally:
            self.i2c.unlock()
        return read_byte[0]

    def readPin(self, pin: int):
        if pin < 1 or pin > 8:
            raise ValueError("Pin number must be between 1 and 8")
        return (self.read() >> pin) & 1

    def get_pin(self, pin: int):
        if not 1 <= pin <= 8:
            raise ValueError("Pin number must be 1-8.")
        return DigitalInOut(pin, self)

    @property
    def iodir(self) -> int:
        """The raw IODIR direction register.  Each bit represents
        direction of a pin, either 1 for an input or 0 for an output mode.
        """
        return self._read_u8()

    @iodir.setter
    def iodir(self, val: int) -> None:
        self._write_u8(val)

    @property
    def ipol(self) -> int:
        """The raw IPOL output register.  Each bit represents the
        polarity value of the associated pin (0 = normal, 1 = inverted), assuming that
        pin has been configured as an input previously.
        """
        return 0

    @ipol.setter
    def ipol(self, val: int) -> None:
        pass

    @property
    def gpio(self) -> int:
        """The raw GPIO output register.  Each bit represents the
        output value of the associated pin (0 = low, 1 = high), assuming that
        pin has been configured as an output previously.
        """
        return self._read_u8()

    @gpio.setter
    def gpio(self, val: int) -> None:
        self._write_u8(val)

    def _read_u8(self) -> int:
        # Read an unsigned 8 bit value from the specified 8-bit register.
        with self._device as bus_device:
            bus_device.readinto(_BUFFER)
            return _BUFFER[0]

    def _write_u8(self, val: int) -> None:
        # Write an 8 bit value to the specified 8-bit register.
        with self._device as bus_device:
            _BUFFER[0] = val
            bus_device.write(_BUFFER)
