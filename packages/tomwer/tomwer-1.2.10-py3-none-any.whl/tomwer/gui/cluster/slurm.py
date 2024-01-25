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
__date__ = "11/10/2021"


from typing import Optional

from silx.gui import qt
from sluurp.utils import get_partitions

from tomwer.core.settings import SlurmSettings, SlurmSettingsMode
from tomwer.gui.utils.qt_utils import block_signals


class SlurmSettingsDialog(qt.QDialog):
    sigConfigChanged = qt.Signal()
    """Signal emit when the SlurmSetting changed"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setLayout(qt.QVBoxLayout())
        self._mainWidget = SlurmSettingsWindow(parent=self)
        self._mainWidget.setWindowFlags(qt.Qt.Widget)
        self.layout().addWidget(self._mainWidget)

        # buttons for validation
        self._buttons = qt.QDialogButtonBox(self)
        types = qt.QDialogButtonBox.Close
        self._buttons.setStandardButtons(types)
        self.layout().addWidget(self._buttons)

        self._buttons.button(qt.QDialogButtonBox.Close).clicked.connect(self.close)

        # connect signal /slot
        self._mainWidget.sigConfigChanged.connect(self._configChanged)

    def _configChanged(self, *args, **kwargs):
        self.sigConfigChanged.emit()

    def isSlurmActive(self):
        return self._mainWidget.isSlurmActive()

    def getConfiguration(self) -> dict:
        return self._mainWidget.getConfiguration()

    def setConfiguration(self, config: dict) -> None:
        self._mainWidget.setConfiguration(config=config)


class SlurmSettingsWindow(qt.QMainWindow):
    """
    Main window to define slurm settings.
    Composed of the SlurmSettingsWidget and a combobox with some predefined settings
    """

    sigConfigChanged = qt.Signal()
    """Signal emit when the SlurmSetting changed"""

    def __init__(self, parent: Optional[qt.QWidget] = None) -> None:
        super().__init__(parent)
        self._mainWidget = qt.QWidget(self)
        self._mainWidget.setLayout(qt.QFormLayout())

        self._modeCombox = qt.QComboBox(self)
        self._mainWidget.layout().addRow("configuration: ", self._modeCombox)
        self._modeCombox.addItems(SlurmSettingsMode.values())
        self._modeCombox.setCurrentText(SlurmSettingsMode.GENERIC.value)

        self._settingsWidget = SlurmSettingsWidget(self)
        self._mainWidget.layout().addRow(self._settingsWidget)

        self.setCentralWidget(self._mainWidget)

        # set up
        self._reloadPredefinedSettings()

        # connect signal / slot
        self._modeCombox.currentIndexChanged.connect(self._reloadPredefinedSettings)
        self._settingsWidget.sigConfigChanged.connect(self._configChanged)
        # when the settings widget is edited them we automatically move to 'manual' settings. To notify visually the user
        self._settingsWidget.sigConfigChanged.connect(self._switchToManual)

    def _reloadPredefinedSettings(self, *args, **kkwargs):
        """
        reload settings from some predefined configuration
        """
        mode = self.getCurrentSettingsMode()
        settingsClass = SlurmSettingsMode.get_settings_class(mode)
        if settingsClass:
            with block_signals(self._settingsWidget):
                self.setConfiguration(
                    {
                        "cpu-per-task": settingsClass.N_CORES_PER_TASK,
                        "n_tasks": settingsClass.N_TASKS,
                        "n_jobs": settingsClass.N_JOBS,
                        "memory": settingsClass.MEMORY_PER_WORKER,
                        "partition": settingsClass.PARTITION,
                        "n_gpus": settingsClass.N_GPUS_PER_WORKER,
                        "job_name": settingsClass.PROJECT_NAME,
                        "walltime": settingsClass.DEFAULT_WALLTIME,
                        "python_venv": settingsClass.PYTHON_VENV,
                    }
                )

    def _configChanged(self, *args, **kwargs):
        self.sigConfigChanged.emit()

    def _switchToManual(self):
        self._modeCombox.setCurrentText(SlurmSettingsMode.MANUAL.value)

    def getCurrentSettingsMode(self) -> SlurmSettingsMode:
        return SlurmSettingsMode.from_value(self._modeCombox.currentText())

    def setCurrentSettingsMode(self, mode: SlurmSettingsMode) -> SlurmSettingsMode:
        mode = SlurmSettingsMode.from_value(mode)
        self._modeCombox.setCurrentText(mode.value)

    # expose API
    def getConfiguration(self) -> dict:
        return self._settingsWidget.getConfiguration()

    def getSlurmClusterConfiguration(self) -> dict:
        return self._settingsWidget.getSlurmClusterConfiguration()

    def setConfiguration(self, config: dict) -> None:
        self._settingsWidget.setConfiguration(config=config)

    def isSlurmActive(self):
        return self._settingsWidget.isSlurmActive()


class SlurmSettingsWidget(qt.QWidget):
    """Widget used to define Slurm configuration to be used"""

    sigConfigChanged = qt.Signal()
    """Signal emit when the SlurmSetting changed"""

    def __init__(
        self,
        parent=None,
        n_gpu=SlurmSettings.N_GPUS_PER_WORKER,
        jobLimitation: Optional[int] = 1,
    ) -> None:
        """
        :param int n_gpu: if provided will set the value to the number of gpu requested
                          (default is one as most of the job are nabu reconstruction)
        :param Optional[int] jobLimitation: if set then will hide the option to define the number of job
        """
        super().__init__(parent=parent)
        self.setLayout(qt.QFormLayout())

        # queues
        self._queue = qt.QComboBox(self)
        self._queue.setEditable(True)
        for partition in get_partitions():
            self._queue.addItem(partition)
        self.layout().addRow("queue / partition", self._queue)

        # n workers
        self._nWorkers = qt.QSpinBox(self)
        self._nWorkers.setRange(1, 100)
        self.layout().addRow("number of task", self._nWorkers)

        # ncores active
        self._nCores = qt.QSpinBox(self)
        self._nCores.setRange(1, 500)
        self.layout().addRow("number of cores per task", self._nCores)

        # memory
        self._memory = qt.QSpinBox(self)
        self._memory.setRange(1, 10000)
        self._memory.setSuffix("GB")
        self.layout().addRow("memory per task", self._memory)

        # gpu
        self._nGpu = qt.QSpinBox(self)
        self._nGpu.setRange(0, 12)
        self.layout().addRow("number of GPUs per task", self._nGpu)

        # n jobs
        self._nJobs = qt.QSpinBox(self)
        self._nJobs.setRange(1, 100000)
        self._nJobs.setValue(1)
        self._nJobsLabel = qt.QLabel("number of job", self)
        self.layout().addRow(self._nJobsLabel, self._nJobs)
        self._nJobs.setToolTip("Define on how many part the job should be split in")
        self._nJobsLabel.setVisible(jobLimitation is None)
        self._nJobs.setVisible(jobLimitation is None)

        # wall time
        self._wallTimeQLE = qt.QLineEdit("", self)
        self._wallTimeLabel = qt.QLabel("wall time", self)
        self.layout().addRow(self._wallTimeLabel, self._wallTimeQLE)

        # python exe
        self._pythonVenv = qt.QLineEdit("", self)
        self.layout().addRow(
            "source script before processing (python venv)", self._pythonVenv
        )
        self._pythonVenv.setToolTip(
            """
            Optional path to a bash script to source before executing the script.
            """
        )

        # job name
        self._jobName = qt.QLineEdit("", self)
        self._jobName.setToolTip(
            """Job name. Can contains several keyword that will be formatted:
            - scan: will be replaced by the scan name
            - process: will be replaced by the process name (nabu slices, nabu volume...)
            - info: some extra information that can be provided by the process to `specify` the processing
            note: those key word have to be surronding by surrounded `{` and `}` in order to be formatted.
            """
        )
        self._job_nameQLabel = qt.QLabel("job name", self)
        self.layout().addRow(self._job_nameQLabel, self._jobName)

        # port
        # fixme: replace by a dedicated widget / validator for TCP adress
        self._port = _PortRangeSelection(self)
        self._port.setRange(0, 99999)
        self._port.setToolTip("TCP Port for the dask-distributed scheduler")
        self._portLabel = qt.QLabel("port", self)
        self.layout().addRow(self._portLabel, self._port)

        # dashboard port
        self._dashboardPort = qt.QSpinBox(self)
        self._dashboardPort.setRange(0, 99999)
        self._dashboardPort.setToolTip("TCP Port for the dashboard")
        self._dashboardPortLabel = qt.QLabel("dashboard port", self)
        self.layout().addRow(self._dashboardPortLabel, self._dashboardPort)

        # simplify gui
        self._wallTimeLabel.hide()
        self._wallTimeQLE.hide()
        self._dashboardPort.hide()
        self._dashboardPortLabel.hide()
        self._jobName.hide()
        self._job_nameQLabel.hide()
        self._portLabel.hide()  # for now we don't use the port. This can be done automatically
        self._port.hide()  # for now we don't use the port. This can be done automatically

        # set up the gui
        self._nCores.setValue(SlurmSettings.N_CORES_PER_TASK)
        self._nWorkers.setValue(SlurmSettings.N_TASKS)
        self._memory.setValue(SlurmSettings.MEMORY_PER_WORKER)
        self._queue.setCurrentText(SlurmSettings.PARTITION)
        self._nGpu.setValue(n_gpu)
        self._jobName.setText(SlurmSettings.PROJECT_NAME)
        self._wallTimeQLE.setText(SlurmSettings.DEFAULT_WALLTIME)
        self._pythonVenv.setText(SlurmSettings.PYTHON_VENV)

        # connect signal / slot
        self._nCores.valueChanged.connect(self._configurationChanged)
        self._nWorkers.valueChanged.connect(self._configurationChanged)
        self._memory.valueChanged.connect(self._configurationChanged)
        self._queue.currentTextChanged.connect(self._configurationChanged)
        self._nGpu.valueChanged.connect(self._configurationChanged)
        self._jobName.editingFinished.connect(self._configurationChanged)
        self._wallTimeQLE.editingFinished.connect(self._configurationChanged)
        self._pythonVenv.editingFinished.connect(self._configurationChanged)
        self._port.sigRangeChanged.connect(self._configurationChanged)
        self._dashboardPort.valueChanged.connect(self._configurationChanged)

    def _configurationChanged(self, *args, **kwargs):
        self.sigConfigChanged.emit()

    def getNCores(self) -> int:
        return self._nCores.value()

    def setNCores(self, n: int) -> None:
        self._nCores.setValue(int(n))

    def getNWorkers(self) -> int:
        return self._nWorkers.value()

    def setNWorkers(self, n) -> None:
        self._nWorkers.setValue(int(n))

    def getMemory(self) -> int:
        return self._memory.value()

    def setMemory(self, memory: int) -> None:
        self._memory.setValue(int(memory))

    def getQueue(self) -> str:
        return self._queue.currentText()

    def setQueue(self, text: str) -> None:
        self._queue.setCurrentText(text)

    def getNGPU(self) -> int:
        return self._nGpu.value()

    def setNGPU(self, n: int) -> None:
        self._nGpu.setValue(int(n))

    def getNJobs(self) -> int:
        return self._nJobs.value()

    def setNJobs(self, value: int):
        self._nJobs.setValue(int(value))

    def getProjectName(self):
        return self._jobName.text()

    def setProjectName(self, name):
        self._jobName.setText(name)

    def getWallTime(self):
        return self._wallTimeQLE.text()

    def setWallTime(self, walltime):
        self._wallTimeQLE.setText(walltime)

    def getPythonExe(self):
        return self._pythonVenv.text()

    def setPythonExe(self, python_venv):
        self._pythonVenv.setText(python_venv)

    def setConfiguration(self, config: dict) -> None:
        old = self.blockSignals(True)
        active_slurm = config.get("active_slurm", None)
        if active_slurm is not None:
            self._slurmCB.setChecked(active_slurm)

        n_cores = config.get("cpu-per-task", None)
        if n_cores is not None:
            self.setNCores(n_cores)

        n_workers = config.get("n_tasks", None)
        if n_workers is not None:
            self.setNWorkers(n_workers)

        memory = config.get("memory", None)
        if memory is not None:
            if isinstance(memory, str):
                memory = memory.replace(" ", "").lower().rstrip("gb")
            self.setMemory(int(memory))

        queue_ = config.get("partition", None)
        if queue_ is not None:
            queue_ = queue_.rstrip("'").rstrip('"')
            queue_ = queue_.lstrip("'").lstrip('"')
            self.setQueue(queue_)

        n_gpu = config.get("n_gpus", None)
        if n_gpu is not None:
            self.setNGPU(int(n_gpu))

        project_name = config.get("job_name", None)
        if project_name is not None:
            self.setProjectName(project_name)

        wall_time = config.get("walltime", None)
        if wall_time is not None:
            self.setWallTime(wall_time)

        python_venv = config.get("python_venv", None)
        if python_venv is not None:
            python_venv = python_venv.rstrip("'").rstrip('"')
            python_venv = python_venv.lstrip("'").lstrip('"')
            self.setPythonExe(python_venv)

        n_jobs = config.get("n_jobs", None)
        if n_jobs is not None:
            self.setNJobs(n_jobs)

        self.blockSignals(old)
        self.sigConfigChanged.emit()

    def getConfiguration(self) -> dict:
        return {
            "cpu-per-task": self.getNCores(),
            "n_tasks": self.getNWorkers(),
            "n_jobs": self.getNJobs(),
            "memory": self.getMemory(),
            "partition": self.getQueue(),
            "n_gpus": self.getNGPU(),
            "job_name": self.getProjectName(),
            "walltime": self.getWallTime(),
            "python_venv": self.getPythonExe(),
        }

    def getSlurmClusterConfiguration(self):
        from tomwer.core.cluster import SlurmClusterConfiguration

        return SlurmClusterConfiguration().from_dict(self.getConfiguration())


class _PortRangeSelection(qt.QWidget):
    sigRangeChanged = qt.Signal()
    """Signal emit when the port range change"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setLayout(qt.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        # from label
        self._fromLabel = qt.QLabel("from", self)
        self._fromLabel.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        self.layout().addWidget(self._fromLabel)
        self._fromQSpinBox = qt.QSpinBox(self)
        self.layout().addWidget(self._fromQSpinBox)
        # to label
        self._toLabel = qt.QLabel("to", self)
        self._toLabel.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        self.layout().addWidget(self._toLabel)
        self._toQSpinBox = qt.QSpinBox(self)
        self.layout().addWidget(self._toQSpinBox)
        # steps label
        self._stepLabel = qt.QLabel("step", self)
        self._stepLabel.setAlignment(qt.Qt.AlignRight | qt.Qt.AlignVCenter)
        self.layout().addWidget(self._stepLabel)
        self._stepQSpinBox = qt.QSpinBox(self)
        self.layout().addWidget(self._stepQSpinBox)

        # connect signal / slot
        self._fromQSpinBox.valueChanged.connect(self._rangeChanged)
        self._toQSpinBox.valueChanged.connect(self._rangeChanged)
        self._stepQSpinBox.valueChanged.connect(self._rangeChanged)

    def _rangeChanged(self, *args, **kwargs):
        self.sigRangeChanged.emit()

    def getRange(self) -> tuple:
        return (
            self._fromQSpinBox.value(),
            self._toQSpinBox.value(),
            self._stepQSpinBox.value(),
        )

    def setRange(self, min_: int, max_: int, step: Optional[int] = None) -> None:
        self._fromQSpinBox.setValue(min(min_, max_))
        self._toQSpinBox.setValue(max(min_, max_))
        if step is not None:
            self._stepQSpinBox.setValue(step)
