# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2019 Carter Nelson
# SPDX-FileCopyrightText: Copyright (c) 2024 Finn Scheller
#
# SPDX-License-Identifier: MIT

"""
`digital_inout`
====================================================

Digital input/output of the PCA9674.
Enables the use of the PCA9674 I/O as a digitalio pin object.

* Author(s): Finn Scheller
"""

import digitalio

try:
    from digitalio import Direction

    from .pca9674 import PCA9674
except ImportError:
    pass

__version__ = "1.0.0"
__repo__ = "https://github.com/XENONFFM/CircuitPython_PCA9674.git"


# Internal helpers to simplify setting and getting a bit inside an integer.
def _get_bit(val, bit: int) -> int:
    return val & (1 << bit) > 0


def _enable_bit(val, bit: int) -> int:
    return val | (1 << bit)


def _clear_bit(val, bit: int) -> int:
    return val & ~(1 << bit)


class DigitalInOut:
    """Digital input/output of the pca9674.  The interface is exactly the
    same as the digitalio.DigitalInOut class, however:

      * PCA9674 family does not support pull-down resistors

    Exceptions will be thrown when attempting to set unsupported pull
    configurations.
    """

    def __init__(self, pin_number: int, pca9674: PCA9674) -> None:
        """Specify the pin number of the PCA9674 (0...7 for PCA9674) instance."""
        self._pin = pin_number
        self._pca = pca9674

    # kwargs in switch functions below are _necessary_ for compatibility
    # with DigitalInout class (which allows specifying pull, etc. which
    # is unused by this class).  Do not remove them, instead turn off pylint
    # in this case.
    # pylint: disable=unused-argument
    def switch_to_output(self, value: bool = False, **kwargs) -> None:
        """Switch the pin state to a digital output with the provided starting
        value (True/False for high or low, default is False/low).
        """
        self.direction = digitalio.Direction.OUTPUT
        self.value = value

    def switch_to_input(self, invert_polarity: bool = False, **kwargs) -> None:
        """Switch the pin state to a digital input with the provided starting
        pull-up resistor state.
        """
        self.direction = digitalio.Direction.INPUT
        self.invert_polarity = invert_polarity

    # pylint: enable=unused-argument

    @property
    def value(self) -> bool:
        """The value of the pin, either True for high or False for
        low.  Note you must configure as an output or input appropriately
        before reading and writing this value.
        """
        return _get_bit(self._pca.gpio, self._pin)

    @value.setter
    def value(self, val: bool) -> None:
        if val:
            self._pca.gpio = _enable_bit(self._pca.gpio, self._pin)
        else:
            self._pca.gpio = _clear_bit(self._pca.gpio, self._pin)

    @property
    def direction(self) -> bool:
        """The direction of the pin, either True for an input or
        False for an output.
        """
        if _get_bit(self._pca.iodir, self._pin):
            return digitalio.Direction.INPUT
        return digitalio.Direction.OUTPUT

    @direction.setter
    def direction(self, val: Direction) -> None:
        if val == digitalio.Direction.INPUT:
            self._pca.iodir = _enable_bit(self._pca.iodir, self._pin)
        elif val == digitalio.Direction.OUTPUT:
            self._pca.iodir = _clear_bit(self._pca.iodir, self._pin)
        else:
            raise ValueError("Expected INPUT or OUTPUT direction!")

    @property
    def invert_polarity(self) -> bool:
        """The polarity of the pin, either True for an Inverted or
        False for an normal.
        """
        if _get_bit(self._pca.ipol, self._pin):
            return True
        return False

    @invert_polarity.setter
    def invert_polarity(self, val: bool) -> None:
        if val:
            self._pca.ipol = _enable_bit(self._pca.ipol, self._pin)
        else:
            self._pca.ipol = _clear_bit(self._pca.ipol, self._pin)
