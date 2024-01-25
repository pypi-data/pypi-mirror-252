# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "15/10/2019"


import logging

from silx.utils.enum import Enum as _Enum

_logger = logging.getLogger(__name__)


class _InputType(_Enum):
    SINOGRAM = "sinogram"
    RADIOS_X2 = "2 radios"
    COMPOSITE = "composite"


class _Constrain(_Enum):
    FULL_TURN = "full turn"


class AxisMode(_Enum):
    centered = "centered"
    global_ = "global"
    manual = "manual"
    growing_window_sinogram = "sino-growing-window"
    growing_window_radios = "radios-growing-window"
    sliding_window_sinogram = "sino-sliding-window"
    sliding_window_radios = "radios-sliding-window"
    sino_coarse_to_fine = "sino-coarse-to-fine"
    composite_coarse_to_fine = "composite-coarse-to-fine"
    read = "read"

    @classmethod
    def from_value(cls, value):
        # ensure backward compatiblity with workflow defined before COR method on sinograms
        if value == "growing-window":
            _logger.warning(
                "Axis mode requested is 'growing-window'. To insure backward compatibility replace it by 'growing-window-radios'"
            )
            value = AxisMode.growing_window_radios
        elif value == "sliding-window":
            _logger.warning(
                "Axis mode requested is 'sliding-window'. To insure backward compatibility replace it by 'sliding-window-radios'"
            )
            value = AxisMode.sliding_window_radios

        return super().from_value(value=value)


_VALID_INPUTS = {
    AxisMode.centered: (_InputType.RADIOS_X2,),
    AxisMode.global_: (_InputType.RADIOS_X2,),
    AxisMode.manual: (_InputType.RADIOS_X2,),
    AxisMode.growing_window_radios: (_InputType.RADIOS_X2,),
    AxisMode.sliding_window_radios: (_InputType.RADIOS_X2,),
    AxisMode.sliding_window_sinogram: (_InputType.SINOGRAM,),
    AxisMode.growing_window_sinogram: (_InputType.SINOGRAM,),
    AxisMode.sino_coarse_to_fine: (_InputType.SINOGRAM,),
    AxisMode.composite_coarse_to_fine: (
        _InputType.COMPOSITE,
    ),  # in fact it is more an n radio constrain
    AxisMode.read: None,
}

_AXIS_MODE_CONSTRAIN = {
    AxisMode.sino_coarse_to_fine: (_Constrain.FULL_TURN,),
    AxisMode.composite_coarse_to_fine: (_Constrain.FULL_TURN,),
}
