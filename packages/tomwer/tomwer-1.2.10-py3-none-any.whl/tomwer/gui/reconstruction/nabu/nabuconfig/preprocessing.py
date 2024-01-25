# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2020 European Synchrotron Radiation Facility
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
__date__ = "06/12/2021"


import logging
from typing import Optional

from silx.gui import qt

from tomwer.core.process.reconstruction.nabu.utils import (
    _NabuStages,
    _RingCorrectionMethod,
)
from tomwer.gui.reconstruction.nabu.nabuconfig.base import _NabuStageConfigBase
from tomwer.gui.utils.scrollarea import QComboBoxIgnoreWheel as QComboBox
from tomwer.gui.utils.scrollarea import QDoubleSpinBoxIgnoreWheel as QDoubleSpinBox
from tomwer.utils import docstring

_logger = logging.getLogger(__name__)


class _NabuPreProcessingConfig(_NabuStageConfigBase, qt.QWidget):
    """
    Widget to define the configuration of the nabu preprocessing
    """

    sigConfChanged = qt.Signal(str)
    """Signal emitted when the configuration change. Parameter is the option
    modified
    """

    def __init__(self, parent, scrollArea):
        _NabuStageConfigBase.__init__(self, stage=_NabuStages.PRE)
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QGridLayout())

        # default options
        ## flat field
        self._flatFieldCB = qt.QCheckBox("flat field correction", self)
        self._flatFieldCB.setToolTip("Whether to enable flat-field " "normalization")
        self.layout().addWidget(self._flatFieldCB, 0, 0, 1, 2)
        self.registerWidget(self._flatFieldCB, "optional")

        ## double flat field
        self._dffCB = qt.QCheckBox("double flat field correction", self)
        self._dffCB.setToolTip("Whether to enable double flat field " "normalization")
        self.layout().addWidget(self._dffCB, 1, 0, 1, 2)
        self._dffSigmaLabel = qt.QLabel("sigma:", self)
        self._dffSigmaLabel.setAlignment(qt.Qt.AlignRight)
        self.layout().addWidget(self._dffSigmaLabel, 1, 2, 1, 1)
        self._dffSigmaQDSB = QDoubleSpinBox(parent=self, scrollArea=scrollArea)
        self._dffSigmaQDSB.setMinimum(0.0)
        self._dffSigmaQDSB.setDecimals(2)
        self._dffSigmaQDSB.setSingleStep(0.1)
        self.layout().addWidget(self._dffSigmaQDSB, 1, 3, 1, 1)
        self.registerWidget(self._flatFieldCB, "required")
        self._dffOptWidgets = [
            self.registerWidget(self._dffSigmaLabel, "required"),
            self.registerWidget(self._dffSigmaQDSB, "required"),
        ]

        ## sino ring corrcetion
        self._sinoRingCorrectionCB = qt.QLabel("rings removal method", self)
        self._sinoRingCorrectionCB.setToolTip("Sinogram rings removal method")
        self.layout().addWidget(self._sinoRingCorrectionCB, 2, 0, 1, 2)
        self.registerWidget(self._sinoRingCorrectionCB, "required")

        self._sinoRingCorrectionMthd = QComboBox(parent=self, scrollArea=scrollArea)
        for method in _RingCorrectionMethod:
            self._sinoRingCorrectionMthd.addItem(method.value)
        ## force method to be None by default
        idx = self._sinoRingCorrectionMthd.findText(_RingCorrectionMethod.NONE.value)
        self._sinoRingCorrectionMthd.setCurrentIndex(idx)

        self.layout().addWidget(self._sinoRingCorrectionMthd, 2, 2, 1, 1)
        self.registerWidget(self._sinoRingCorrectionMthd, "required")

        self._sinoRingsOpts = SinoRingsOptions(parent=self)
        self.layout().addWidget(self._sinoRingsOpts, 3, 1, 1, 3)

        ## ccd filter
        self._ccdFilterCB = qt.QCheckBox("CCD hot spot correction", self)
        self._ccdFilterCB.setToolTip("Whether to enable the CCD hotspots " "correction")
        self.layout().addWidget(self._ccdFilterCB, 4, 0, 1, 2)
        self.registerWidget(self._ccdFilterCB, "optional")

        ## ccd filter threshold
        self._ccdHotspotLabel = qt.QLabel("threshold:", self)
        self._ccdHotspotLabel.setAlignment(qt.Qt.AlignRight)
        self.layout().addWidget(self._ccdHotspotLabel, 5, 2, 1, 1)
        self._ccdThreshold = QDoubleSpinBox(self, scrollArea)
        self._ccdThreshold.setMinimum(0.0)
        self._ccdThreshold.setMaximum(999999)
        self._ccdThreshold.setSingleStep(0.01)
        self._ccdThreshold.setDecimals(6)
        tooltip = (
            "If ccd_filter_enabled = 1, a median filter is applied on "
            "the 3X3 neighborhood\nof every pixel. If a pixel value "
            "exceeds the median value more than this parameter,\nthen "
            "the pixel value is replaced with the median value."
        )
        self._ccdThreshold.setToolTip(tooltip)
        self.layout().addWidget(self._ccdThreshold, 5, 3, 1, 1)
        self._ccdOptWidgets = [
            self.registerWidget(self._ccdHotspotLabel, "optional"),
            self.registerWidget(self._ccdThreshold, "optional"),
        ]

        ## sr current normalization
        self._normalizeCurrent = qt.QCheckBox("normalize with current", self)
        self._normalizeCurrent.setToolTip(
            "Whether to normalize frames with Synchrotron Current. This can correct the effect of a beam refill not taken into account by flats."
        )
        self.layout().addWidget(self._normalizeCurrent, 6, 0, 1, 2)
        self.registerWidget(self._normalizeCurrent, "required")

        ## take logarithm
        self._takeLogarithmCB = qt.QCheckBox("take logarithm", self)
        self.layout().addWidget(self._takeLogarithmCB, 7, 0, 1, 2)
        self.registerWidget(self._takeLogarithmCB, "advanced")

        ## log min clip value
        self._clipMinLogValueLabel = qt.QLabel("log min clip value:", self)
        self._clipMinLogValueLabel.setAlignment(qt.Qt.AlignRight)
        self.layout().addWidget(self._clipMinLogValueLabel, 8, 2, 1, 1)
        self._clipMinLogValue = QDoubleSpinBox(self, scrollArea=scrollArea)
        self._clipMinLogValue.setMinimum(0.0)
        self._clipMinLogValue.setMaximum(9999999)
        self._clipMinLogValue.setSingleStep(0.01)
        self._clipMinLogValue.setDecimals(6)
        self.layout().addWidget(self._clipMinLogValue, 8, 3, 1, 1)
        self._takeLogOpt = [
            self.registerWidget(self._clipMinLogValueLabel, "optional"),
            self.registerWidget(self._clipMinLogValue, "optional"),
        ]

        ## log max clip value
        self._clipMaxLogValueLabel = qt.QLabel("log max clip value:", self)
        self._clipMaxLogValueLabel.setAlignment(qt.Qt.AlignRight)
        self.layout().addWidget(self._clipMaxLogValueLabel, 9, 2, 1, 1)
        self._clipMaxLogValue = QDoubleSpinBox(self, scrollArea=scrollArea)
        self._clipMaxLogValue.setMinimum(0.0)
        self._clipMaxLogValue.setMaximum(9999999)
        self._clipMaxLogValue.setSingleStep(0.01)
        self._clipMaxLogValue.setDecimals(6)
        self.layout().addWidget(self._clipMaxLogValue, 9, 3, 1, 1)
        self._takeLogOpt.extend(
            [
                self.registerWidget(self._clipMaxLogValueLabel, "optional"),
                self.registerWidget(self._clipMaxLogValue, "optional"),
            ]
        )

        ## tilt correction
        self._tiltCorrection = TiltCorrection("tilt correction", self)
        self.registerWidget(self._tiltCorrection, "advanced")
        self.layout().addWidget(self._tiltCorrection, 10, 0, 1, 4)

        # option dedicated to Helical
        ## process file
        self._processFileQLE = qt.QLabel("file containing weights maps", self)
        self._processFileQLE.setToolTip(
            "also know as 'process_file'. If you don't have this file it can be created from the 'helical-prepare-weights' widget"
        )
        self.layout().addWidget(self._processFileQLE, 20, 0, 1, 1)
        self._processFileQLE = qt.QLineEdit("", self)
        self.registerWidget(self._processFileQLE, "advanced")
        self.layout().addWidget(self._processFileQLE, 20, 1, 1, 3)

        # style

        # spacer for style
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer, 99, 0, 1, 1)

        # set up
        self._flatFieldCB.setChecked(True)
        self.setDFFOptVisible(False)

        self._ccdFilterCB.setChecked(False)
        self._normalizeCurrent.setChecked(False)
        self._ccdThreshold.setValue(0.04)

        self._clipMinLogValue.setValue(1e-6)
        self._clipMaxLogValue.setValue(10.0)
        self._takeLogarithmCB.setChecked(True)
        self.setCCDOptsVisible(False)
        self._sinoRingCorrectionMthd.setCurrentText("None")
        self._sinoRingsOpts.setVisible(False)
        self._tiltCorrection.setChecked(False)

        # connect signal / slot
        self._ccdFilterCB.toggled.connect(self.setCCDOptsVisible)
        self._takeLogarithmCB.toggled.connect(self.setLogClipValueVisible)
        self._flatFieldCB.toggled.connect(self._flatFieldChanged)
        self._dffCB.toggled.connect(self._dffChanged)
        self._dffCB.toggled.connect(self.setDFFOptVisible)
        self._dffSigmaQDSB.valueChanged.connect(self._dffSigmaChanged)
        self._ccdFilterCB.toggled.connect(self._ccdFilterChanged)
        self._normalizeCurrent.toggled.connect(self._normalizeCurrentChanged)
        self._ccdThreshold.editingFinished.connect(self._ccdFilterThresholdChanged)
        self._clipMinLogValue.editingFinished.connect(self._logMinClipChanged)
        self._clipMaxLogValue.editingFinished.connect(self._logMaxClipChanged)
        self._takeLogarithmCB.toggled.connect(self._takeLogarithmChanged)
        self._sinoRingCorrectionMthd.currentIndexChanged.connect(
            self._sinoRingCorrectionChanged
        )
        self._sinoRingsOpts._levels.valueChanged.connect(self._sinoRingOptsChanged)
        self._sinoRingsOpts._sigma.valueChanged.connect(self._sinoRingOptsChanged)

        self._tiltCorrection.toggled.connect(self._tiltCorrectionChanged)
        self._tiltCorrection.sigChanged.connect(self._tiltCorrectionChanged)

    def _flatFieldChanged(self, *args, **kwargs):
        self._signalConfChanged("flatfield")

    def _dffChanged(self, *args, **kwargs):
        self._signalConfChanged("double_flatfield_enabled")

    def _dffSigmaChanged(self, *args, **kwargs):
        self._signalConfChanged("dff_sigma")

    def _ccdFilterChanged(self, *args, **kwargs):
        self._signalConfChanged("ccd_filter_enabled")

    def _normalizeCurrentChanged(self, *args, **kwargs):
        self._signalConfChanged("normalize_srcurrent")

    def _ccdFilterThresholdChanged(self, *args, **kwargs):
        self._signalConfChanged("ccd_filter_threshold")

    def _logMinClipChanged(self, *args, **kwargs):
        self._signalConfChanged("log_min_clip")

    def _logMaxClipChanged(self, *args, **kwargs):
        self._signalConfChanged("log_max_clip")

    def _takeLogarithmChanged(self, *args, **kwargs):
        self._signalConfChanged("take_logarithm")

    def _sinoRingCorrectionChanged(self, *args, **kwargs):
        self._sinoRingsOpts.setVisible(
            self.getSinoRingcorrectionMethod() in (_RingCorrectionMethod.MUNCH.value,)
        )
        self._signalConfChanged("sino_rings_correction")

    def _sinoRingOptsChanged(self, *args, **kwargs):
        self._signalConfChanged("sino_rings_options")

    def _tiltCorrectionChanged(self, *args, **kwargs):
        self._signalConfChanged("tilt_correction")

    def _signalConfChanged(self, param, *args, **kwargs):
        self.sigConfChanged.emit(param)

    def setDFFOptVisible(self, visible):
        for widget in self._dffOptWidgets:
            widget.setVisible(visible)

    def setCCDOptsVisible(self, visible):
        for widget in self._ccdOptWidgets:
            widget.setVisible(visible)

    def setLogClipValueVisible(self, visible):
        for widget in self._takeLogOpt:
            widget.setVisible(visible)

    def isFlatFieldActivate(self):
        return self._flatFieldCB.isChecked()

    def isDoubleFlatFieldActivate(self):
        return self._dffCB.isChecked()

    def getDFFSigma(self) -> float:
        """

        :return: double flat field sigma
        """
        return self._dffSigmaQDSB.value()

    def isCCDFilterActivate(self):
        return self._ccdFilterCB.isChecked()

    def getCCDThreshold(self) -> float:
        return float(self._ccdThreshold.text())

    def getNormalizeCurrent(self) -> bool:
        return self._normalizeCurrent.isChecked()

    def setNormalizeCurrent(self, normalize: bool) -> None:
        self._normalizeCurrent.setChecked(normalize)

    def getLogMinClipValue(self) -> float:
        return float(self._clipMinLogValue.text())

    def getLogMaxClipValue(self) -> float:
        return float(self._clipMaxLogValue.text())

    def getTakeLogarithm(self):
        return self._takeLogarithmCB.isChecked()

    def getSinoRingcorrectionMethod(self) -> str:
        return self._sinoRingCorrectionMthd.currentText()

    def getSinoRingcorrectionOptions(self) -> str:
        return " ; ".join(
            [
                f"{key}={value}"
                for key, value in self._sinoRingsOpts.getOptions().items()
            ]
        )

    def setSinoRingcorrectionOptions(self, options: str) -> None:
        opt_as_dict = {}
        for opt in options.split(";"):
            opt = opt.replace(" ", "")
            key, value = opt.split("=")
            opt_as_dict[key] = value

        self._sinoRingsOpts.setOptions(opt_as_dict)

    @docstring(_NabuStageConfigBase)
    def getConfiguration(self):
        tilt_correction, autotilt_opts = self._tiltCorrection.getTiltCorrection()
        return {
            "flatfield": int(self.isFlatFieldActivate()),
            "double_flatfield_enabled": int(self.isDoubleFlatFieldActivate()),
            "dff_sigma": self.getDFFSigma(),
            "ccd_filter_enabled": int(self.isCCDFilterActivate()),
            "ccd_filter_threshold": self.getCCDThreshold(),
            "take_logarithm": self.getTakeLogarithm(),
            "log_min_clip": self.getLogMinClipValue(),
            "log_max_clip": self.getLogMaxClipValue(),
            "sino_rings_correction": self.getSinoRingcorrectionMethod(),
            "sino_rings_options": self.getSinoRingcorrectionOptions(),
            "tilt_correction": tilt_correction,
            "autotilt_options": autotilt_opts,
            "normalize_srcurrent": int(self.getNormalizeCurrent()),
        }

    @docstring(_NabuStageConfigBase)
    def setConfiguration(self, conf):
        try:
            self._setConfiguration(conf)
        except Exception as e:
            _logger.error(e)

    def _setConfiguration(self, conf: dict):
        ff = conf.get("flatfield", None)
        if ff is not None:
            self._flatFieldCB.setChecked(bool(ff))

        dff = conf.get("double_flatfield_enabled", None)
        if dff is not None:
            self._dffCB.setChecked(bool(dff))

        dff_sigma = conf.get("dff_sigma", None)
        if dff_sigma not in (None, "", "none"):
            self._dffSigmaQDSB.setValue(float(dff_sigma))

        ccd_filter = conf.get("ccd_filter_enabled", None)
        if ccd_filter not in (None, "", "none"):
            self._ccdFilterCB.setChecked(bool(ccd_filter))

        ccd_filter_threshold = conf.get("ccd_filter_threshold", None)
        if ccd_filter_threshold not in (None, "", "none"):
            self._ccdThreshold.setValue(float(ccd_filter_threshold))

        normalize_srcurrent = conf.get("normalize_srcurrent", None)
        if normalize_srcurrent is not None:
            self.setNormalizeCurrent(bool(normalize_srcurrent))

        take_logarithm = conf.get("take_logarithm", None)
        if take_logarithm not in (None, "", "none"):
            self._takeLogarithmCB.setChecked(bool(take_logarithm))

        clip_value = conf.get("log_min_clip", None)
        if clip_value not in (None, "", "none"):
            self._clipMinLogValue.setValue(float(clip_value))

        clip_value = conf.get("log_max_clip", None)
        if clip_value not in (None, "", "none"):
            self._clipMaxLogValue.setValue(float(clip_value))

        sino_rings_correction = conf.get("sino_rings_correction", None)
        if sino_rings_correction is not None:
            if sino_rings_correction == "":
                sino_rings_correction = _RingCorrectionMethod.NONE
            sino_rings_correction = _RingCorrectionMethod.from_value(
                sino_rings_correction
            ).value
            idx = self._sinoRingCorrectionMthd.findText(sino_rings_correction)
            if idx >= 0:
                self._sinoRingCorrectionMthd.setCurrentIndex(idx)
        sino_rings_options = conf.get("sino_rings_options", None)
        if sino_rings_options is not None:
            self.setSinoRingcorrectionOptions(options=sino_rings_options)

        tilt_correction = conf.get("tilt_correction")
        autotilt_options = conf.get("autotilt_options")
        self._tiltCorrection.setTiltCorrection(
            tilt_correction=tilt_correction, auto_tilt_options=autotilt_options
        )


class SinoRingsOptions(qt.QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.setLayout(qt.QFormLayout())
        self._sigma = qt.QDoubleSpinBox(self)
        self._sigma.setRange(0.0, 2147483647)
        self.layout().addRow("sigma", self._sigma)

        self._levels = qt.QSpinBox(self)
        self._levels.setRange(0, 2147483647)
        self.layout().addRow("levels", self._levels)

        # set up
        self._sigma.setValue(1.0)
        self._levels.setValue(10)

    def getOptions(self) -> dict:
        return {
            "sigma": self._sigma.value(),
            "levels": self._levels.value(),
        }

    def setOptions(self, options: dict) -> None:
        if "sigma" in options:
            self._sigma.setValue(float(options["sigma"]))
        if "levels" in options:
            self._levels.setValue(int(options["levels"]))


class TiltCorrection(qt.QGroupBox):
    """
    GroupBox dedicated to nabu TiltCorrection
    """

    sigChanged = qt.Signal()
    """Signal emit when parameters of the tilt options changed"""

    def __init__(self, text, parent=None, *args, **kwargs) -> None:
        super().__init__(text, parent, *args, **kwargs)
        self.setCheckable(True)
        self.setLayout(qt.QFormLayout())
        self._tiltManualRB = qt.QRadioButton("angle", self)
        self._angleValueSB = qt.QDoubleSpinBox(self)
        self._angleValueSB.setRange(-360, 360)
        self._angleValueSB.setSuffix("°")
        self.layout().addRow(self._tiltManualRB, self._angleValueSB)

        self._autoManualRB = qt.QRadioButton("auto", self)
        self._autoModeCB = qt.QComboBox(self)
        self._modes = {
            "1d-correlation": "auto-detect tilt with the 1D correlation method (fastest, but works best for small tilts)",
            "fft-polar": "auto-detect tilt with polar FFT method (slower, but works well on all ranges of tilts)",
        }
        for value, tooltip in self._modes.items():
            self._autoModeCB.addItem(value)
            idx = self._autoModeCB.findText(value)
            self._autoModeCB.setItemData(idx, tooltip, qt.Qt.ToolTipRole)
        self.layout().addRow(self._autoManualRB, self._autoModeCB)
        self._autoTiltOptions = qt.QLineEdit("", self)
        self._autoTiltOptions.setPlaceholderText("low_pass=1; high_pass=20 ; ...")
        self._autotiltOptsLabel = qt.QLabel("autotilt options")
        self._autotiltOptsLabel.setToolTip(
            """
        Options for methods computing automatically the detector tilt. \n
        The parameters are separated by commas and passed as 'name=value', for example: low_pass=1; high_pass=20. Mind the semicolon separator (;). \n
        For more details please see https://www.silx.org/pub/nabu/doc/apidoc/nabu.estimation.tilt.html#nabu.estimation.tilt.CameraTilt.compute_angle
        """
        )
        self.layout().addRow(self._autotiltOptsLabel, self._autoTiltOptions)

        # set up
        self._autoManualRB.setChecked(True)

        # connect signal / slot
        self._tiltManualRB.toggled.connect(self._updateVisiblity)
        self._autoManualRB.toggled.connect(self._updateVisiblity)

        self._tiltManualRB.toggled.connect(self._changed)
        self._autoManualRB.toggled.connect(self._changed)
        self._angleValueSB.valueChanged.connect(self._changed)

        self._updateVisiblity()

    def _changed(self, *args, **kwargs):
        self.sigChanged.emit()

    def _updateVisiblity(self):
        self._angleValueSB.setEnabled(self._tiltManualRB.isChecked())
        self._autoModeCB.setEnabled(self._autoManualRB.isChecked())
        self._autotiltOptsLabel.setVisible(self._autoManualRB.isChecked())
        self._autoTiltOptions.setVisible(self._autoManualRB.isChecked())

    def getTiltCorrection(self) -> tuple:
        """
        return (tilt value, autotilt options (if any))
        """
        if not self.isChecked():
            return "", ""
        elif self._tiltManualRB.isChecked():
            return self._angleValueSB.value(), ""
        else:
            return self._autoModeCB.currentText(), self._autoTiltOptions.text()

    def setTiltCorrection(
        self, tilt_correction: str, auto_tilt_options: Optional[str] = None
    ) -> None:
        if tilt_correction in ("", None):
            self.setChecked(False)
        elif tilt_correction in self._modes.keys():
            self.setChecked(True)
            self._autoManualRB.setChecked(True)
            idx = self._autoModeCB.findText(tilt_correction)
            self._autoModeCB.setCurrentIndex(idx)
        else:
            self.setChecked(True)
            self._tiltManualRB.setChecked(True)
            self._angleValueSB.setValue(float(tilt_correction))
        if auto_tilt_options is not None:
            self._autoTiltOptions.setText(auto_tilt_options)
