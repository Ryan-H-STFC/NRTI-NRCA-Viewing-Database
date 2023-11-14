from __future__ import annotations
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.rcsetup
import matplotlib.pyplot as plt
# from matplotlib.backends.backend_qt5agg import (
#     FigureCanvasQTAgg as FigureCanvas,
# )
from matplotlib.backends.backend_qt5agg import (
    NavigationToolbar2QT as NavigationToolbar
)
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QRegExp, pyqtSignal
from PyQt5.QtGui import QCursor, QRegExpValidator, QIcon

from PyQt5.QtWidgets import (
    QAction,
    QCheckBox,
    QColorDialog,
    QComboBox,
    QCompleter,
    QDialog,
    QDialogButtonBox,
    QDockWidget,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLineEdit,
    QMainWindow,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QSplitter,
    QTableView,
    QVBoxLayout,
    QWidget,

)
from copy import deepcopy

from pyparsing import Literal

from element.ElementDataStructure import ElementData
from myPyQt.ButtonDelegate import ButtonDelegate
from myPyQt.CustomSortingProxy import CustomSortingProxy
from myPyQt.ExtendedComboBox import ExtendedComboBox
from myPyQt.ExtendedTableModel import ExtendedQTableModel
from myPyQt.InputElementsDialog import InputElementsDialog

from myMatplotlib.CustomFigureCanvas import FigureCanvas
from myMatplotlib.BlittedCursor import BlittedCursor

from helpers.nearestNumber import nearestnumber
from helpers.getRandomColor import getRandomColor
from helpers.getWidgets import getLayoutWidgets


# todo -------------------- Issues/Feature TODO list --------------------
# todo - Add periodic table GUI for selection.
# todo - Maximas after changing threshold wont have correct annotations due to integral and peak widths not calculated
# todo   correctly yet.
# todo - Matplotlib icons
# todo - PyQt5 Unit Testing
# todo - Incorporate multiprocessing and multithreading?
# todo - Fix issues with Maxima not displaying after zoom


# ? Should this ask for the filepath or just be require to be in the format as seen in the repository,
# ? Download the repository and run the program without altering the file structure, will save having
# ? to enter filepaths in console during start up.


# Asking for filepath where the user has saved script
# filepath is where the data and the code has been saved. The sourceFilepath is the path to the latest data folder
# ! Maybe Change back to inputs if requried

#  input('Enter the filepath where the latest NRCA code data folder is \n For Example:'
#                         'C://Users/ccj88542/NRCA/Rehana/Latest/main/data: \n')

# print(filepath)
# print(sourceFilepath)

# ! fonts = font_manager.findSystemFonts(
#     fontpaths="C:\\Users\\gzi47552\\Documents\\NRTI-NRCA-Viewing-Database\\src\\fonts")
# ! for font in fonts:
# !    font_manager.fontManager.addfont(font)
# ! matplotlib.rcParams["font.family"] = 'Roboto Mono'

matplotlib.rcParamsDefault["path.simplify"] = True
matplotlib.rcParamsDefault["agg.path.chunksize"] = 10000


class DatabaseGUI(QWidget):  # Acts just like QWidget class (like a template)
    """
    Class responsible for creating and manipulating the GUI, used in selecting and graphing the data of elements or
    isotopes within the NRTI/NRCA Database.
    """
    resized = pyqtSignal()

    # init constructure for classes
    def __init__(self) -> None:
        """
        Initialisator for DatabaseGUI class
        """
        # Allows for adding more things to the QWidget template
        super(DatabaseGUI, self).__init__()

        self.styleWindows = "Fusion"

        self.styleMain = """
        #mainWindow{{
            background-color: {bg_color};
        }}

        *{{
            font-family: 'Roboto Mono';
            font-size: 10pt;
            font-weight: 400;
        }}

        QAction {{
            background-color: {bg_color};
            color: {text_color};
        }}

        QCheckBox{{
            color: {text_color};
        }}

        QCheckbox::indicator:checked{{
            image: url(./src/img/checkbox-component-checked.svg);
        }}

        QCheckbox::indicator:unchecked{{
            image: url(./src/img/checkbox-component-unchecked.svg);
        }}

        QComboBox{{
            font-family: 'Roboto Mono';
            font-size: 10pt;
            font-weight: 400;
        }}

        QMenuBar{{
            background-color: {bg_color};
            color: {text_color};
        }}

        QSplitter::handle:vertical{{
            image: url(./src/img/drag-component.svg);
            height: 11px;
        }}

        QLabel#numPeakLabel, #thresholdLabel, #orderlabel, #compoundLabel, #peakLabel{{
            font: 10pt 'Roboto Mono';
            color: {text_color};
        }}

        QPushButton#plotEnergyBtn, #plotTOFBtn, #clearBtn, #pdBtn, #compoundBtn{{
            font: 10pt 'Roboto Mono Medium';
            font-weight: 500;
        }}

        QPushButton#plotEnergyBtn:disabled,
                   #plotTOFBtn:disabled,
                   #clearBtn:disabled,
                   #pdBtn:disabled,
                   #compoundBtn:disabled{{
            color: #AAA;
        }}

        QPushButton#plotEnergyBtn:enabled,
                   #plotTOFBtn:enabled,
                   #clearBtn:enabled,
                   #pdBtn:enabled,
                   #compoundBtn:enabled {{
            color: #000;
        }}

        QCheckBox#gridCheck, #thresholdCheck, #label_check, #orderByIntegral, #orderByPeakW, #peakCheck {{
            font-weight: 500;
        }}

        QCheckBox#grid_check::indicator:unchecked,
                 #thresholdCheck::indicator:unchecked,
                 #label_check::indicator:unchecked,
                 #peakCheck::indicator:unchecked
                 {{
                   image: url(./src/img/checkbox-component-unchecked.svg);
                   color: {text_color};
                 }}

        QCheckBox#grid_check::indicator:checked,
                 #thresholdCheck::indicator:checked,
                 #label_check::indicator:checked,
                 #peakCheck::indicator:checked
                 {{
                     image: url(./src/img/checkbox-component-checked.svg);
                     color: {text_color};
                 }}

        QCheckBox#grid_check:disabled,
                 #thresholdCheck:disabled,
                 #label_check:disabled
                 {{
                     color: #AAA;
                 }}
        QCheckBox#grid_check:enabled,
                 #thresholdCheck:enabled,
                 #label_check:enabled
        {{
            color: {text_color};
        }}

        QDockWidget{{
            background-color: {bg_color};
            color: {text_color};
        }}

        QDockWidget::title{{
            color: {text_color};
        }}

        QRadioButton#orderByIntegral:enabled,
                    #orderByPeakW:enabled
                    {{
                        color: {text_color};
                    }}
        QRadioButton#orderByIntegral::indicator:unchecked,
                    #orderByPeakW::indicator:unchecked
                    {{
                        image: url(./src/img/radio-component-unchecked);
                        color: #AAA;
                    }}

        QRadioButton#orderByIntegral::indicator:checked,
                    #orderByPeakW::indicator:checked
                    {{
                        image: url(./src/img/radio-component-checked);
                        color: {text_color};
                    }}

        QWidget#peakCanvasContainer{{
            margin: 9px;
            background-color: #FFF;
        }}

        QWidget#mainContainer {{
            background-color: {text_color};
        }}

        QHeaderView {{
            font-size: 7.5pt;
        }}

        QHeaderView::section:horizontal{{
            border-top: 1px solid #000;
            border-bottom: 1px solid #000;
        }}

        QHeaderView::section:horizontal:!last{{
            border-right: 1px solid #000;
        }}

        QHeaderView::down-arrow{{
            image: url(./src/img/expand-down-component.svg);
        }}

        QHeaderView::up-arrow{{
            image: url(./src/img/expand-up-component.svg);
        }}

        QTableView#dataTable {{
            font-size: 8pt;
            border-style: none;
        }}

        QMessageBox QLabel{{
            color: {text_color};
        }}

        QDialog {{
            background-color: {bg_color};
        }}

        QDialog#inputWindow
        {{
            color: {text_color};
            background-color: {bg_color};
        }}

        QDialog#inputWindow QLabel{{
            color: {text_color};
        }}

        QDialog#optionsDialog QCombobox{{
            background-color: {text_color};
        }}
        """

        # Setting global variables
        self.data = None
        self.x = []  # ! Depreciated
        self.y = []  # ! Depreciated
        self.xArray = []
        self.yArray = []
        self.numRows = None
        self.numTotPeaks = []

        self.ax = None
        self.ax2 = None
        self.peakCanvas = None
        self.plotFilepath = None
        self.firstLimit = None
        self.secondLimit = None
        self.plotCount = -1
        self.graphs = dict()
        self.annotations = []
        self.localHiddenAnnotations = []
        self.plottedSubstances = []
        self.rows = None
        self.tableLayout = dict()
        self.arrays = dict()
        self.selectionName = None
        self.xi = None
        self.yj = None
        self.peaknum = None
        self.interact = None
        self.clickcount = None
        self.gridSettings = {"which": "major", "axis": "both", "color": "#444"}

        self.peakInfoIsNull = None
        self.graphData = None
        self.peakLimitsX = dict()
        self.peakLimitsY = dict()
        self.peakList = None
        self.orderByIntegral = True
        self.firstClickX = None
        self.filepath = f"{os.path.dirname(__file__)}\\"
        self.dataFilepath = f"{self.filepath}data\\Graph Data\\"
        self.elementData = dict()
        self.elementDataNames = []
        self.compoundData = dict()
        self.isCompound = False

        self.maxPeak = 50
        self.thresholds = dict()

        self.distributionDir = self.filepath + "data\\Distribution Information\\"
        self.defaultDistributions = dict()
        self.elementDistributions = dict()

        thresholdFilepath = self.filepath + "data\\threshold_exceptions.txt"

        file = pd.read_csv(thresholdFilepath, header=None)

        for line in file.values:
            symbol = line[0].split(' ')[0]
            self.thresholds[symbol] = (line[0].split(' ')[1].replace('(', ''), line[1].replace(')', ''))

        dist_filePaths = [f for f in os.listdir(self.distributionDir) if f.endswith(".csv")]
        for filepath in dist_filePaths:
            name = filepath[:-4]
            dist = pd.read_csv(f"{self.distributionDir}{filepath}", header=None)
            self.defaultDistributions[name] = dict({d[0]: d[1] for d in dist.values})

        self.elementDistributions = deepcopy(self.defaultDistributions)

        self.setStyleSheet(self.styleMain.format(bg_color="#202020", text_color="#FFF"))
        self.initUI()
        self.setAcceptDrops(True)

    def initUI(self) -> None:
        """
        ``initUI``
        Creates the UI.
        """
        self.setObjectName('mainWindow')
        self.setGeometry(350, 50, 1600, 900)
        self.setWindowTitle("NRTI/NRCA Viewing Database")
        self.resized.connect(self.adjustCanvas)

        mainLayout = QGridLayout()

        menubarLayout = QHBoxLayout()
        menubarLayout.setContentsMargins(0, 0, 0, 0)

        sidebarLayout = QVBoxLayout()
        sidebarLayout.setContentsMargins(0, 0, 0, 0)

        canvasLayout = QVBoxLayout()
        canvasLayout.setContentsMargins(0, 0, 0, 0)

        # * ----------------------------------------------

        # ¦ -------------- MENU BAR - FILE ---------------
        # Creating actions for file menu
        menubar = QMenuBar(self)
        menubar.setObjectName("menubar")

        newAction = QAction(QIcon("./src/img/add-component.svg"), "&New", self)
        newAction.setShortcut("Ctrl+N")
        newAction.triggered.connect(self.clear)

        importAction = QAction(QIcon("./src/img/upload-component.svg"), "&Import Data", self)
        importAction.setShortcut("Ctrl+I")

        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(newAction)
        fileMenu.addAction(importAction)
        importAction.triggered.connect(self.importdata)

        # * ----------------------------------------------

        # ¦ --------------- MENU BAR - EDIT --------------
        # Creates menu bar and add actions
        editpeakAction = QAction(QIcon("./src/img/edit-component.svg"), "&Edit Peak Limits", self)
        editpeakAction.setShortcut("Ctrl+E")
        editpeakAction.triggered.connect(self.editPeakLimits)

        editThresholdAction = QAction(QIcon("./src/img/edit-component.svg"), "&Edit Threshold", self)
        editThresholdAction.setShortcut("Ctrl+Shift+T")
        editThresholdAction.triggered.connect(self.editThresholdLimit)

        editDistribution = QAction(QIcon("./src/img/edit-component.svg"), "&Edit Distribution", self)
        editDistribution.setShortcut("Ctrl+Shift+D")
        editDistribution.triggered.connect(self.editDistribution)
        # fileMenu.addAction(saveAction)

        editMenu = menubar.addMenu("&Edit")
        editMenu.addAction(editpeakAction)
        editMenu.addAction(editThresholdAction)
        editMenu.addAction(editDistribution)

        menubarLayout.addWidget(menubar, alignment=Qt.AlignLeft)
        # Adding label which shows number of peaks
        self.peaklabel = QLabel()
        self.peaklabel.setObjectName('numPeakLabel')
        self.peaklabel.setText("")
        self.peaklabel.setAlignment(Qt.AlignVCenter)

        self.peaklabel.setContentsMargins(0, 10, 0, 0)
        menubarLayout.addWidget(self.peaklabel, alignment=Qt.AlignVCenter)
        # Threshold Label
        self.thresholdLabel = QLabel()
        self.thresholdLabel.setObjectName('thresholdLabel')
        self.thresholdLabel.setText("Nothing has been selected")
        self.thresholdLabel.setAlignment(Qt.AlignRight)
        self.thresholdLabel.setContentsMargins(0, 10, 0, 0)

        menubarLayout.addWidget(self.thresholdLabel, alignment=Qt.AlignRight)

        # * ----------------------------------------------

        # ¦ --------------- MENU BAR - VIEW --------------

        viewMenu = menubar.addMenu("&View")
        appearenceMenu = viewMenu.addMenu("Appearence")

        defaultAppearence = QAction(QIcon("./src/img/changeAppearence-component.svg"), "&Dark Theme", self)
        defaultAppearence.setShortcut("Ctrl+Shift+1")
        defaultAppearence.triggered.connect(self.viewDarkStyle)

        windowsAppearence = QAction(QIcon("./src/img/changeAppearence-component.svg"), "&Light Theme", self)
        windowsAppearence.setShortcut("Ctrl+Shift+2")
        windowsAppearence.triggered.connect(self.viewLightStyle)

        highContrastAppearence = QAction(QIcon("./src/img/changeAppearence-component.svg"), "&High Contrast", self)
        highContrastAppearence.setShortcut("Ctrl+Shift+3")
        highContrastAppearence.triggered.connect(self.viewHighContrastStyle)

        appearenceMenu.addAction(defaultAppearence)
        appearenceMenu.addAction(windowsAppearence)
        appearenceMenu.addAction(highContrastAppearence)

        # * ----------------------------------------------

        # ¦ ------------- MENU BAR - OPTIONS -------------

        optionsMenu = menubar.addMenu("&Options")

        gridlineOptions = QAction(QIcon("./src/img/grid-component.svg"), "&Grid Line Settings", self)
        gridlineOptions.setShortcut("Ctrl+Shift+G")
        gridlineOptions.triggered.connect(self.gridLineOptions)

        maxPeaksOption = QAction(QIcon("./src/img/edit-component.svg"), "&Max Peak Quantity", self)
        maxPeaksOption.setShortcut("Ctrl+Shift+Q")
        maxPeaksOption.triggered.connect(self.editMaxPeaks)

        optionsMenu.addAction(gridlineOptions)
        optionsMenu.addAction(maxPeaksOption)

        # * ----------------------------------------------

        # ¦ --------------- Combobox Group ---------------
        # For copying data directory to local directory for plotting later
        # Establishing source and destination directories

        # Creating a list of substances stored in the NRCA database data directory
        self.selectionName = [None]
        for file in os.listdir(f"{self.filepath}data\\Graph Data\\"):
            filename = os.fsdecode(file)
            if ".csv" not in filename[-4:]:
                continue
            filename = filename[:-4]
            self.selectionName.append(filename)

        # Creating combo box (drop down menu)
        self.combobox = ExtendedComboBox()
        self.combobox.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.combobox.setObjectName("combobox")

        self.combobox.addItems(self.selectionName)
        # self.combobox.setEditable(True)
        self.combobox.lineEdit().setPlaceholderText("Select an Isotope / Element")
        # self.combobox.setInsertPolicy(QComboBox.NoInsert)
        # self.combobox.setMaxVisibleItems(15)

        # completer = CustomQCompleter(self.combobox)
        # completer.setCompletionMode(QCompleter.PopupCompletion)
        # completer.setModel(self.combobox.model())

        # self.combobox.setCompleter(completer)

        sidebarLayout.addWidget(self.combobox)

        # Upon selecting an option, it records the option
        # and connects to the method 'displayData'
        self.combobox.editTextChanged.connect(lambda: self.plotSelectionProxy(
            index=self.combobox.currentIndex(),
            comboboxName=self.combobox.objectName()
        ))
        # * ----------------------------------------------

        pointingCursor = QCursor(Qt.PointingHandCursor)

        # ¦ ---------------- Button Group ----------------

        self.btnLayout = QVBoxLayout()

        self.plotEnergyBtn = QPushButton("Plot in Energy", self)
        self.plotEnergyBtn.setObjectName("plotEnergyBtn")
        self.plotEnergyBtn.setCursor(pointingCursor)
        self.plotEnergyBtn.__name__ = "plotEnergyBtn"
        self.plotEnergyBtn.resize(self.plotEnergyBtn.sizeHint())
        self.plotEnergyBtn.setEnabled(False)
        self.btnLayout.addWidget(self.plotEnergyBtn)
        self.plotEnergyBtn.clicked.connect(self.updateGuiData)

        self.plotTOFBtn = QPushButton("Plot in ToF", self)
        self.plotTOFBtn.setCursor(pointingCursor)
        self.plotTOFBtn.setObjectName("plotTOFBtn")
        self.plotTOFBtn.__name__ = "plotToFBtn"
        self.plotTOFBtn.resize(self.plotTOFBtn.sizeHint())
        self.plotTOFBtn.setEnabled(False)
        self.btnLayout.addWidget(self.plotTOFBtn)
        self.plotTOFBtn.clicked.connect(lambda: self.updateGuiData(tof=True))

        self.clearBtn = QPushButton("Clear All", self)
        self.clearBtn.setObjectName("clearBtn")
        self.clearBtn.setCursor(pointingCursor)
        self.clearBtn.__name__ = "clearBtn"
        self.clearBtn.resize(self.clearBtn.sizeHint())
        self.clearBtn.setEnabled(False)
        self.btnLayout.addWidget(self.clearBtn)
        self.clearBtn.clicked.connect(self.clear)

        self.pdBtn = QPushButton("Peak Detection", self)
        self.pdBtn.setObjectName("pdBtn")
        self.pdBtn.setCursor(pointingCursor)
        self.pdBtn.__name__ = "pdBtn"
        self.pdBtn.resize(self.pdBtn.sizeHint())
        self.pdBtn.setEnabled(False)
        self.btnLayout.addWidget(self.pdBtn)
        self.pdBtn.clicked.connect(self.GetPeaks)

        sidebarLayout.addLayout(self.btnLayout)

        # * ----------------------------------------------

        # ¦ --------------- Checkbox Group ---------------

        self.toggleLayout = QVBoxLayout()
        self.toggleLayout.setObjectName('toggleLayout')

        self.gridCheck = QCheckBox("Grid Lines", self)
        self.gridCheck.setCursor(pointingCursor)
        self.gridCheck.setObjectName("grid_check")
        self.gridCheck.__name__ = "gridCheck"

        self.gridCheck.setEnabled(False)
        self.toggleLayout.addWidget(self.gridCheck)
        self.gridCheck.stateChanged.connect(lambda: self.toggleGridlines(self.gridCheck.isChecked(),
                                                                         **self.gridSettings))

        self.thresholdCheck = QCheckBox("Peak Detection Limits", self)
        self.thresholdCheck.setCursor(pointingCursor)
        self.thresholdCheck.setObjectName("thresholdCheck")
        self.thresholdCheck.__name__ = "thresholdCheck"
        self.thresholdCheck.setEnabled(False)
        self.toggleLayout.addWidget(self.thresholdCheck)
        self.thresholdCheck.stateChanged.connect(self.toggleThreshold)

        self.peakLabelCheck = QCheckBox("Hide Peak Labels", self)
        self.peakLabelCheck.setCursor(pointingCursor)
        self.peakLabelCheck.setObjectName("label_check")
        self.peakLabelCheck.__name__ = "labelCheck"
        self.peakLabelCheck.setEnabled(False)
        self.toggleLayout.addWidget(self.peakLabelCheck)
        self.peakLabelCheck.stateChanged.connect(self.toggleAnnotations)

        sidebarLayout.addLayout(self.toggleLayout)

        # * ------------------------------------------------

        # ¦ --------------- Peak Order Group ---------------

        peakOrderLayout = QVBoxLayout()
        peakOrderLayout.setSpacing(5)
        peakCheckLayout = QHBoxLayout()
        peakCheckLayout.setSpacing(5)
        peakOrderLabel = QLabel(self, text="Peak Order")
        peakOrderLabel.setObjectName('orderlabel')

        radioBtnGroup = QGroupBox()
        self.byIntegralCheck = QRadioButton(radioBtnGroup, text="By Integral")
        self.byIntegralCheck.setObjectName('orderByIntegral')
        self.byIntegralCheck.setChecked(True)
        self.byIntegralCheck.clicked.connect(self.onPeakOrderChange)
        self.byPeakWidthCheck = QRadioButton(radioBtnGroup, text="By Peak Width")
        self.byPeakWidthCheck.setObjectName('orderByPeakW')
        self.byPeakWidthCheck.clicked.connect(self.onPeakOrderChange)

        peakCheckLayout.addWidget(self.byIntegralCheck)
        peakCheckLayout.addWidget(self.byPeakWidthCheck)

        peakOrderLayout.addWidget(peakOrderLabel)
        peakOrderLayout.addItem(peakCheckLayout)

        sidebarLayout.addLayout(peakOrderLayout)

        # * -----------------------------------------------

        # ¦ ----------- Compound Creater Group ------------

        compoundCreaterLayout = QVBoxLayout()
        compoundCreaterLayout.setSpacing(5)
        compoundLabel = QLabel(self, text="Compound Creation")
        compoundLabel.setObjectName("compoundLabel")
        compoundCreaterBtn = QPushButton("Create Compound", self)
        compoundCreaterBtn.setObjectName("compoundBtn")
        compoundCreaterBtn.clicked.connect(self.createCompound)
        self.compoundCombobox = ExtendedComboBox()
        self.compoundCombobox.lineEdit().setPlaceholderText("Select a Compound")
        self.compoundCombobox.setObjectName("compoundComboBox")
        self.compoundCombobox.editTextChanged.connect(lambda: self.plotSelectionProxy(
            index=self.compoundCombobox.currentIndex(),
            comboboxName=self.compoundCombobox.objectName()
        ))
        self.compoundNames = [None]
        for file in os.listdir(f"{self.filepath}data\\Graph Data\\Compound Data\\"):
            filename = os.fsdecode(file)
            if ".csv" not in filename[-4:]:
                continue
            filename = filename[:-4]
            self.compoundNames.append(filename)
        self.compoundCombobox.addItems(self.compoundNames)
        compoundCreaterLayout.addWidget(compoundLabel)
        compoundCreaterLayout.addWidget(compoundCreaterBtn)
        compoundCreaterLayout.addWidget(self.compoundCombobox)

        sidebarLayout.addLayout(compoundCreaterLayout)

        # * -----------------------------------------------

        # ¦ ----------------- Plot Canvas -----------------
        self.figure = plt.figure()  # Creating canvas to plot graph on and toolbar
        self.canvas = FigureCanvas(self.figure, self)
        self.canvas.__name__ = "canvas"
        self.canvas.mpl_connect('pick_event', self.hideGraph)
        self.toolbar = NavigationToolbar(self.canvas, self)

        canvasLayout.addWidget(self.toolbar)
        canvasLayout.addWidget(self.canvas)

        # * -----------------------------------------------

        # ¦ -------------------- Table --------------------
        # Adding table to display peak information
        self.table = QTableView()
        self.table.setObjectName('dataTable')
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setMinimumHeight(200)

        # * -----------------------------------------------

        container = QWidget(self)
        container.setObjectName('mainContainer')
        container.setLayout(canvasLayout)
        container.setMinimumHeight(300)

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(container)
        splitter.addWidget(self.table)
        splitter.setHandleWidth(10)

        contentLayout = QHBoxLayout()
        contentLayout.addWidget(splitter)
        sidebarLayout.setAlignment(Qt.AlignTop)

        mainLayout.addItem(menubarLayout, 0, 0, 1, 6, Qt.AlignTop)
        mainLayout.addItem(sidebarLayout, 1, 0, 1, 1, Qt.AlignTop)
        mainLayout.addItem(contentLayout, 1, 1, 1, 6)
        self.btnLayout.setSpacing(10)
        self.toggleLayout.setSpacing(10)

        sidebarLayout.setSpacing(50)

        # If double-clicking cell, can trigger plot peak

        self.table.doubleClicked.connect(self.PlotPeakWindow)

        self.setLayout(mainLayout)  # Generating layout
        self.show()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        """
        ``resizeEvent`` On resize of connected widget event handler.

        Args:
            event (QtGui.QResizeEvent): Event triggered on resizing.

        Returns:
            ``None``
        """
        self.resized.emit()
        return super(DatabaseGUI, self).resizeEvent(event)

    def adjustCanvas(self) -> None:
        """
        ``adjustCanvas`` Apply tight layout to figure.
        """
        self.figure.tight_layout()

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        """
        ``dragEnterEvent`` handles file drag enter event and verification

        Args:
            ``event`` (QDragEnterEvent): Event triggerd on mouse dragging into the window.
        """
        if event.mimeData().hasUrls():
            for file in event.mimeData().urls():
                filepath = file.toLocalFile()
                if any([ext for ext in ['.csv', '.txt', '.dat'] if ext in filepath]):
                    event.acceptProposedAction()
                else:
                    event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event: QtGui.QDropEvent) -> None:
        """
        ``dropEvent`` handles the drop event and calls to plot each data file

        Args:
            ``event`` (QDropEvent): PyQtEvent
        """
        for url in event.mimeData().urls():
            filepath = url.toLocalFile()
            name = filepath.split('/')[-1].split('.')[0]
            self.updateGuiData(False, filepath, True, name)

    def editPeakLimits(self) -> None:
        """
        ``editPeakLimits`` Edit Peaks opens a dialog window to alter limits of integration for peaks of the selected
        element, recaluating the integral and peak widths to place into the table.
        """
        # Click count to disconnect after two limits have been selected
        if self.plottedSubstances == []:
            QMessageBox.warning(self, "Error", "You have not plotted anything")
            return

        optionsWindow = InputElementsDialog(self, self.styleSheet())

        optionsWindow.elements.addItems(self.elementData.keys())
        optionsWindow.elements.setMaxVisibleItems(5)

        elementPeaks = ExtendedComboBox()
        elementPeaks.setValidator(QRegExpValidator(QRegExp("[+-]?([0-9]*[.])?[0-9]+")))

        firstLimitLayout = QHBoxLayout()
        firstLimitX = QLineEdit()

        firstLimitX.setValidator(QRegExpValidator(QRegExp("[+-]?([0-9]*[.])?[0-9]+")))
        firstLimitBtn = QPushButton()
        firstLimitBtn.setObjectName("first")
        firstLimitBtn.setIcon(QIcon(".\\src\\img\\add-component.svg"))
        firstLimitLayout.addWidget(firstLimitX)
        firstLimitLayout.addWidget(firstLimitBtn)

        secondLimitLayout = QHBoxLayout()
        secondLimitX = QLineEdit()
        secondLimitX.setValidator(QRegExpValidator(QRegExp("[+-]?([0-9]*[.])?[0-9]+")))
        secondLimitBtn = QPushButton()
        secondLimitBtn.setObjectName("second")
        secondLimitBtn.setIcon(QIcon(".\\src\\img\\add-component.svg"))
        secondLimitLayout.addWidget(secondLimitX)
        secondLimitLayout.addWidget(secondLimitBtn)

        optionsWindow.inputForm.addRow(QLabel("Peak X-Coord:"), elementPeaks)
        optionsWindow.inputForm.addRow(QLabel("1st Limit X:"), firstLimitLayout)
        optionsWindow.inputForm.addRow(QLabel("2nd Limit X:"), secondLimitLayout)

        applyBtn = optionsWindow.buttonBox.addButton(QDialogButtonBox.Ok)
        applyBtn.setText("Apply")
        cancelBtn = optionsWindow.buttonBox.addButton(QDialogButtonBox.Cancel)

        optionsWindow.inputForm.setSpacing(5)
        optionsWindow.mainLayout.insertItem(1, optionsWindow.inputForm)

        optionsWindow.setWindowTitle("Edit Peaks for Substance")
        optionsWindow.mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        optionsWindow.setLayout(optionsWindow.mainLayout)
        elements = optionsWindow.elements

        ax = self.ax2 if self.ax2 is not None else self.ax

        def onAccept():

            elementName = elements.itemText(elements.currentIndex() or 0)
            element = self.elementData[elementName]
            peak = float(elementPeaks.currentText())
            leftLimit = float(firstLimitX.placeholderText() if firstLimitX.text(
            ) == '' else firstLimitX.text())
            rightLimit = float(secondLimitX.placeholderText() if secondLimitX.text(
            ) == '' else secondLimitX.text())

            tableMax_x = nearestnumber(element.tableData["Energy (eV)"][1:], peak)

            row = element.tableData[1:].loc[
                (element.tableData["Energy (eV)"][1:].astype(float) == tableMax_x)
            ]
            integral = row["Integral"].iloc[0]

            result = self.elementData[elementName].PeakIntegral(leftLimit, rightLimit)

            print(f"Peak: {peak}\n")
            print(f"Integral: {integral}\t-\tEstimate: {result}")
            self.figure.canvas.mpl_disconnect(optionsWindow.motionEvent)
            self.figure.canvas.mpl_disconnect(optionsWindow.buttonPressEvent)
        applyBtn.clicked.connect(onAccept)

        def onClose():
            self.figure.canvas.mpl_disconnect(optionsWindow.motionEvent)
            self.figure.canvas.mpl_disconnect(optionsWindow.buttonPressEvent)
            optionsWindow.close()
        cancelBtn.clicked.connect(onClose)

        def onElementChange(index):

            element = self.elementData.get(elements.currentText(), False)
            elementPeaks.blockSignals(True)
            firstLimitX.setText(None)
            secondLimitX.setText(None)
            elementPeaks.clear()
            if not element:
                elements.lineEdit().setText(None)
                elements.setCurrentIndex(0)
                return

            if element.maxima[0].size == 0 or element.maxPeakLimitsX == {}:
                elementPeaks.setEnabled(False)
                firstLimitX.setEnabled(False)
                secondLimitX.setEnabled(False)
                applyBtn.setEnabled(False)
                elementPeaks.setCurrentText("Null")
                firstLimitX.setPlaceholderText("Null")
                secondLimitX.setPlaceholderText("Null")
                elementPeaks.blockSignals(False)

                return
            elementPeaks.setEnabled(True)
            firstLimitX.setEnabled(True)
            secondLimitX.setEnabled(True)
            elementPeaks.addItems([str(peak) for peak in element.maxima[0] if element.maxPeakLimitsX.get(peak, False)])
            elementPeaks.blockSignals(False)

            onPeakChange(elements.currentIndex())

        def onPeakChange(index):

            element = self.elementData.get(elements.currentText(), False)
            if not element or elementPeaks.currentText() == '':
                elements.lineEdit().setText(None)
                elements.setCurrentIndex(0)
                elementPeaks.setCurrentIndex(0)
                return
            firstLimitX.setText(None)
            secondLimitX.setText(None)
            if element.maxPeakLimitsX == {}:
                elements.setCurrentIndex(0)
                elementPeaks.setCurrentText("Null")
                firstLimitX.setPlaceholderText("Null")
                secondLimitX.setPlaceholderText("Null")
                applyBtn.setEnabled(False)
                return
            applyBtn.setEnabled(True)
            peak = float(elementPeaks.currentText())
            firstLimitX.setPlaceholderText(str(element.maxPeakLimitsX[peak][0]))
            secondLimitX.setPlaceholderText(str(element.maxPeakLimitsX[peak][1]))

            try:
                optionsWindow.blittedCursor.on_remove()
                del optionsWindow.blitterCursor

            except AttributeError:
                pass

        def onLimitChange():

            limitLeft = firstLimitX.placeholderText() if firstLimitX.text(
            ) == '' else firstLimitX.text()
            limitRight = secondLimitX.placeholderText() if secondLimitX.text(
            ) == '' else secondLimitX.text()
            peak = float(elementPeaks.currentText())
            if limitLeft == 'Null' or limitRight == 'Null':
                applyBtn.setEnabled(False)
                return
            if float(limitLeft) > peak or float(limitRight) < peak:
                applyBtn.setEnabled(False)
                return
            try:
                optionsWindow.blittedCursor.on_remove()
                del optionsWindow.blittedCursor

            except AttributeError:
                pass
            for line in ax.get_lines() + ax.texts:
                if 'cursor' in line.get_gid():
                    line.remove()
            applyBtn.setEnabled(True)

        def onLimitSelect(event):
            if not optionsWindow.blittedCursor.valid:
                return
            else:
                if optionsWindow.which == 'first':
                    firstLimitX.setText(f"{round(optionsWindow.blittedCursor.x, 3)}")
                if optionsWindow.which == 'second':
                    secondLimitX.setText(f"{round(optionsWindow.blittedCursor.x, 3)}")

            try:
                optionsWindow.blittedCursor.on_remove()
                del optionsWindow.blittedCursor

            except AttributeError:
                pass
            self.figure.canvas.mpl_disconnect(optionsWindow.motionEvent)
            self.figure.canvas.mpl_disconnect(optionsWindow.buttonPressEvent)

        def connectLimitSelect(btn):
            optionsWindow.which = btn.objectName()
            optionsWindow.blittedCursor = BlittedCursor(ax=ax, axisType='x', which=optionsWindow.which)

            self.figure.canvas.mpl_disconnect(optionsWindow.motionEvent)
            self.figure.canvas.mpl_disconnect(optionsWindow.buttonPressEvent)
            optionsWindow.motionEvent = self.figure.canvas.mpl_connect(
                'motion_notify_event',
                lambda event: optionsWindow.blittedCursor.on_mouse_move(event, float(elementPeaks.currentText())))
            optionsWindow.buttonPressEvent = self.figure.canvas.mpl_connect("button_press_event", onLimitSelect)
        firstLimitBtn.pressed.connect(lambda: connectLimitSelect(firstLimitBtn))
        secondLimitBtn.pressed.connect(lambda: connectLimitSelect(secondLimitBtn))

        optionsWindow.elements.currentIndexChanged.connect(
            lambda: onElementChange(index=optionsWindow.elements.currentIndex()))
        elementPeaks.currentIndexChanged.connect(lambda: onPeakChange(elements.currentIndex()))
        firstLimitX.textChanged.connect(onLimitChange)
        secondLimitX.textChanged.connect(onLimitChange)

        onElementChange(elements.currentIndex())
        optionsWindow.setModal(False)
        optionsWindow.show()

    def editDistribution(self) -> None:
        """
        ``editDistribution`` Opens a dialog window with options to alter the natural abundence of elements and compounds
        updating the graph data of any relevant plots.
        """

        optionsWindow = InputElementsDialog(self, self.styleSheet())
        optionsWindow.elements.addItems(
            [el for el in self.combobox.getAllItemText() if 'element' in el])
        optionsWindow.elements.addItems(self.compoundCombobox.getAllItemText())

        totalLabel = QLabel()

        applyBtn = optionsWindow.buttonBox.addButton(QDialogButtonBox.Apply)
        applyBtn.setEnabled(False)
        applyBtn.setText("Apply")
        resetBtn = optionsWindow.buttonBox.addButton(QDialogButtonBox.Reset)
        cancelBtn = optionsWindow.buttonBox.addButton(QDialogButtonBox.Cancel)

        optionsWindow.mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        optionsWindow.setWindowTitle("Edit Distribution")
        optionsWindow.setLayout(optionsWindow.mainLayout)

        optionsWindow.mainLayout.insertWidget(len(optionsWindow.children()) - 2, totalLabel)

        elements = optionsWindow.elements

        def onAccept():

            elementName = elements.itemText(elements.currentIndex() or 0)
            if elementName == '':
                return
            for widget in getLayoutWidgets(optionsWindow.mainLayout, QWidget):

                title = widget.findChild(QLabel).text()[:-1]
                if widget.findChild(QLineEdit).text() == '':
                    dist = float(widget.findChild(QLineEdit).placeholderText())
                else:
                    dist = float(widget.findChild(QLineEdit).text())

                self.elementDistributions[elementName][title] = dist

            for title, Tof in self.plottedSubstances:

                if elementName == title:
                    title = f"{title}-{'ToF' if Tof else 'Energy'}"

                    self.elementData[title].distributions = self.elementDistributions[elementName]

                    self.elementData[title].isDistAltered = True
                    self.elementData[title].isGraphDrawn = False
                    self.isCompound = self.elementData[title].isCompound
                    self.data = elementName

                    self.updateGuiData(tof=Tof, distAltered=True)
                    break
        applyBtn.clicked.connect(onAccept)
        cancelBtn.clicked.connect(optionsWindow.reject)

        def onReset():
            onElementChange(reset=True)
            applyBtn.setEnabled(True)
        resetBtn.clicked.connect(onReset)

        def onElementChange(index=0, reset: bool = False):

            elementName = elements.itemText(index)
            if elementName == '':
                elements.setCurrentIndex(0)
                return
            totalLabel.setStyleSheet("color: {text_color};")
            for widget in getLayoutWidgets(optionsWindow.mainLayout, QWidget):
                if widget.objectName() == "isotopeDistribution":
                    optionsWindow.mainLayout.removeWidget(widget)
                    widget.deleteLater()

            total = 0
            acc = str(max([len(str(a)) - 2 for a in self.defaultDistributions[elementName].values()] + [2]))
            if reset:
                items = self.defaultDistributions
            else:
                items = self.elementDistributions
            for i, (name, dist) in enumerate(items[elementName].items()):
                total += dist
                sublayout = QHBoxLayout()
                proxyWidget = QWidget()
                newQLineEdit = QLineEdit()

                newQLineEdit.setValidator(QRegExpValidator(
                    QRegExp("(0?(\\.[0-9]{1," + acc + "})?|1(\\.0{1," + acc + "})?)")))
                newQLineEdit.setPlaceholderText(str(dist))
                title = QLabel(f"{name}:")

                sublayout.addWidget(title)
                sublayout.addWidget(newQLineEdit)
                sublayout.setSpacing(1)
                proxyWidget.setLayout(sublayout)
                proxyWidget.setFixedHeight(38)
                proxyWidget.setObjectName("isotopeDistribution")
                newQLineEdit.textChanged.connect(onDistributionChange)
                optionsWindow.mainLayout.insertWidget(i + 1, proxyWidget)
            optionsWindow.updateGeometry()
            totalLabel.setText(f"Total: {round(total, int(acc)-1)}")
        optionsWindow.elements.setFocus()
        optionsWindow.elements.editTextChanged.connect(lambda: onElementChange(optionsWindow.elements.currentIndex()))

        def onDistributionChange():

            elementName = elements.itemText(elements.currentIndex() or 0)
            if elementName == '':
                return
            total: float = 0
            acc = min([len(str(a)) - 2 for a in self.defaultDistributions[elementName].values()])
            for widget in getLayoutWidgets(optionsWindow.mainLayout, QWidget):
                lineEdit = widget.findChild(QLineEdit)
                distribution = lineEdit.placeholderText() if lineEdit.text() == '' else lineEdit.text()
                if distribution == ".":
                    continue
                total += float(distribution)
            total = round(total, acc)
            totalLabel.setText(f"Total: {total}")
            applyBtn.setEnabled(False)
            if total < 1:
                totalLabel.setStyleSheet("color: #FFF;")
            elif total > 1:
                totalLabel.setStyleSheet("color: #F00;")
            else:
                totalLabel.setStyleSheet("color: #0F0;")
                applyBtn.setEnabled(True)

        onElementChange(optionsWindow.elements.currentIndex())
        optionsWindow.setModal(False)
        optionsWindow.show()

    def editThresholdLimit(self) -> None:
        """
        ``editThresholdLimit`` Creates a GUI to alter the threshold value for a selected graph, recomputing maximas and
        drawing the relevant annotations
        """
        if self.elementData == {}:
            return

        optionsWindow = InputElementsDialog(self, self.styleSheet())
        optionsWindow.inputForm.windowTitle = "Threshold Input"

        elements = optionsWindow.elements

        elements.addItems(self.elementData.keys())

        inputThreshold = QLineEdit()
        inputThreshold.setPlaceholderText(str(self.elementData[elements.currentText()].threshold))
        inputThreshold.setValidator(QRegExpValidator(QRegExp("[+-]?([0-9]*[.])?[0-9]+")))

        optionsWindow.inputForm.addRow(QLabel("Threshold:"), inputThreshold)

        applyBtn = optionsWindow.buttonBox.addButton(QDialogButtonBox.Apply)
        cancelBtn = optionsWindow.buttonBox.addButton(QDialogButtonBox.Cancel)
        applyBtn.setEnabled(False)

        optionsWindow.setWindowTitle("Edit Threshold Value")
        optionsWindow.mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        optionsWindow.mainLayout.insertItem(1, optionsWindow.inputForm)
        optionsWindow.setLayout(optionsWindow.mainLayout)

        def close():
            optionsWindow.close()
        cancelBtn.clicked.connect(close)

        def onElementChange(index):
            if elements.itemText(index) == '':
                elements.setCurrentIndex(0)
                inputThreshold.setText(None)
                return
            inputThreshold.setPlaceholderText(str(self.elementData[elements.itemText(index)].threshold))
        elements.editTextChanged.connect(lambda: onElementChange(elements.currentIndex()))

        def onThresholdTextChange():
            if inputThreshold.text() == '':
                applyBtn.setEnabled(False)
            else:
                applyBtn.setEnabled(True)
        inputThreshold.textChanged.connect(onThresholdTextChange)

        def onAccept():
            substance_name = elements.currentText()
            if inputThreshold.text() == '':
                return
            threshold_value = float(inputThreshold.text())

            self.elementData[substance_name].threshold = threshold_value
            self.elementData[substance_name].UpdatePeaks()
            self.toggleThreshold()
            self.drawAnnotations(self.elementData[substance_name])
            for element in self.elementData.values():
                if element.isMaxDrawn:
                    element.isGraphUpdating = True
                    self.PlottingPD(element, True)
                if element.isMinDrawn:
                    element.isGraphUpdating = True
                    self.PlottingPD(element, False)
        applyBtn.clicked.connect(onAccept)

        inputThreshold.setFocus(True)
        optionsWindow.setModal(False)
        optionsWindow.show()

    def gridLineOptions(self):
        """
        ``gridLineOptions`` Opens a dialog with settings related to the gridlines of the canvas.
        Options include: Which axis to plot gridlines for, which type; major, minor or both ticks, as well as color.
        """

        optionsWindowDialog = QDialog()
        optionsWindowDialog.setWindowTitle("Gridline Options")
        mainLayout = QVBoxLayout()
        formLayout = QFormLayout()

        gridlineLayout = QHBoxLayout()
        gridlineGroup = QGroupBox()

        majorRadioBtn = QRadioButton(text="Major")
        majorRadioBtn.setObjectName("gridline")
        majorRadioBtn.setChecked(True)
        minorRadioBtn = QRadioButton(text="Minor")
        minorRadioBtn.setObjectName("gridline")
        bothRadioBtn = QRadioButton(text="Both")
        bothRadioBtn.setObjectName("gridline")

        gridlineLayout.addWidget(majorRadioBtn)
        gridlineLayout.addWidget(minorRadioBtn)
        gridlineLayout.addWidget(bothRadioBtn)

        gridlineGroup.setLayout(gridlineLayout)

        axisLayout = QHBoxLayout()
        axisGroup = QGroupBox()

        xAxisRadioBtn = QRadioButton(text="X")
        xAxisRadioBtn.setObjectName("axis")
        yAxisRadioBtn = QRadioButton(text="Y")
        yAxisRadioBtn.setObjectName("axis")
        bothAxisRadioBtn = QRadioButton(text="Both")
        bothAxisRadioBtn.setObjectName("axis")
        bothAxisRadioBtn.setChecked(True)

        axisLayout.addWidget(xAxisRadioBtn)
        axisLayout.addWidget(yAxisRadioBtn)
        axisLayout.addWidget(bothAxisRadioBtn)

        axisGroup.setLayout(axisLayout)

        gridColorDialog = QColorDialog()
        gridColorDialog.setCurrentColor(QtGui.QColor(self.gridSettings["color"]))
        gridColorBtn = QPushButton()
        gridColorBtn.setStyleSheet(f"margin: 5px; background-color: {self.gridSettings['color']};")

        formLayout.addRow(QLabel("Gridline Options:"), gridlineGroup)
        formLayout.addRow(QLabel("Axis Options:"), axisGroup)
        formLayout.addRow(QLabel("Gridline Color:"), gridColorBtn)

        buttonBox = QDialogButtonBox()

        onResetBtn = buttonBox.addButton(QDialogButtonBox.Reset)
        onAcceptBtn = buttonBox.addButton(QDialogButtonBox.Apply)
        onCancelBtn = buttonBox.addButton(QDialogButtonBox.Cancel)

        mainLayout.addLayout(formLayout)
        mainLayout.addWidget(buttonBox)

        optionsWindowDialog.setLayout(mainLayout)

        # map(lambda radio: radio.g.connect(lambda: onRadioCheck("axis", radio)),
        #     getLayoutWidgets(axisLayout, QRadioButton))
        # map(lambda radio: radio.clicked.connect(lambda: onRadioCheck("gridline", radio)),
        #     getLayoutWidgets(gridlineLayout, QRadioButton))

        # def onRadioCheck(group: str, radio: QRadioButton):
        #     radioBtns = getLayoutWidgets(QRadioButton)
        #     map(lambda radio: radio.setChecked(False),
        #         [radio for radio in radioBtns if radio.objectName() == group])
        #     radio.setChecked(True)

        def openColorDialog():
            optionsWindowDialog.blockSignals(True)
            gridColorDialog.setModal(True)
            gridColorDialog.show()
        gridColorBtn.clicked.connect(openColorDialog)

        def onColorPick():
            optionsWindowDialog.blockSignals(False)
            gridColorBtn.setStyleSheet(
                f"margin: 5px; background-color: {str(gridColorDialog.selectedColor().name())};")
        gridColorDialog.colorSelected.connect(onColorPick)

        def onReset():
            map(lambda btn: btn.setChecked(False),
                getLayoutWidgets(mainLayout, QRadioButton))
            majorRadioBtn.setChecked(True)
            bothAxisRadioBtn.setChecked(True)
            gridColorDialog.setCurrentColor(QtGui.QColor(68, 68, 68))
            self.toggleGridlines(self.gridCheck.isChecked(), *self.gridSettings.values())
        onResetBtn.clicked.connect(onReset)

        def onAccept():
            self.gridSettings = {"which": [radio.text().lower()
                                           for radio in getLayoutWidgets(gridlineLayout) if radio.isChecked()][0],
                                 "axis": [radio.text().lower()
                                          for radio in getLayoutWidgets(axisLayout) if radio.isChecked()][0],
                                 "color": gridColorDialog.currentColor().name()}
            self.toggleGridlines(self.gridCheck.isChecked(), *self.gridSettings.values())
        onAcceptBtn.clicked.connect(onAccept)

        def onCancel():
            optionsWindowDialog.close()
        onCancelBtn.clicked.connect(onCancel)

        optionsWindowDialog.setModal(False)
        optionsWindowDialog.setUpdatesEnabled(True)
        optionsWindowDialog.blockSignals(True)
        optionsWindowDialog.show()
        optionsWindowDialog.blockSignals(False)

    def editMaxPeaks(self) -> None:
        """
        ``editMaxPeaks`` Creates a GUI element for inputting the max peak label quanitity for a selected graph, drawing
        the relevant annotations.
        """
        if self.elementData == {}:
            return

        optionsWindow = InputElementsDialog(self, self.styleSheet())
        elements = optionsWindow.elements

        elements.addItems(self.elementData.keys())

        inputMaxPeaks = QLineEdit()
        inputMaxPeaks.setPlaceholderText(str(self.elementData[elements.currentText()].numPeaks))
        inputMaxPeaks.setValidator(QRegExpValidator(QRegExp("[0-9]{0,4}")))

        optionsWindow.inputForm.addRow(QLabel("Peak Quantity:"), inputMaxPeaks)

        applyBtn = optionsWindow.buttonBox.addButton(QDialogButtonBox.Apply)
        cancelBtn = optionsWindow.buttonBox.addButton(QDialogButtonBox.Cancel)

        optionsWindow.setWindowTitle("Displayed Peaks Quantity")
        optionsWindow.mainLayout.insertItem(1, optionsWindow.inputForm)
        optionsWindow.setLayout(optionsWindow.mainLayout)

        def closeWindow():
            optionsWindow.close()
        cancelBtn.clicked.connect(closeWindow)

        def changePeaksText():
            inputMaxPeaks.setPlaceholderText(str(self.elementData[elements.currentText()].numPeaks))
        elements.activated.connect(changePeaksText)

        def onAccept():
            substance_name = elements.currentText()
            if inputMaxPeaks.text() == '':
                return
            maxPeaks = int(inputMaxPeaks.text())
            self.elementData[substance_name].maxPeaks = maxPeaks
            self.drawAnnotations(self.elementData[substance_name])
        applyBtn.clicked.connect(onAccept)

        optionsWindow.setModal(False)
        optionsWindow.show()

    def createCompound(self) -> None:
        """
        ``createCompound`` Opens a dialog for users to create compounds from weighted combinations of varying elements,
        this calculates and saves the graph data to a file for reuse.
        """

        optionsWindow = InputElementsDialog(self, self.styleSheet())

        elements = optionsWindow.elements

        elements.lineEdit().setPlaceholderText("Select an Isotope / Element")
        elements.addItems([self.combobox.itemText(i)
                           for i in range(self.combobox.count())])
        # elements.addItems([self.combobox.itemText(i)
        #                    for i in range(self.combobox.count()) if 'element' in self.combobox.itemText(i)])

        totalLabel = QLabel("Total: 0")

        applyBtn = optionsWindow.buttonBox.addButton(QDialogButtonBox.Apply)
        applyBtn.setText("Create")
        applyBtn.setEnabled(False)

        addBtn = optionsWindow.buttonBox.addButton(QDialogButtonBox.Yes)
        addBtn.setText("Add")
        addBtn.setEnabled(False)

        resetBtn = optionsWindow.buttonBox.addButton(QDialogButtonBox.Reset)
        cancelBtn = optionsWindow.buttonBox.addButton(QDialogButtonBox.Cancel)

        optionsWindow.mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        optionsWindow.setWindowTitle("Compound Creater")
        optionsWindow.setLayout(optionsWindow.mainLayout)

        optionsWindow.mainLayout.insertWidget(len(optionsWindow.children()) - 2, totalLabel)

        compoundElements = {}
        compoundMode = []

        def onAccept():
            applyBtn.setEnabled(False)
            compoundDist = {
                widget.findChild(QLabel).text()[:-1]: float(widget.findChild(QLineEdit).text())
                for widget in getLayoutWidgets(optionsWindow.mainLayout, QWidget)
            }
            name = f"""compound_{'-'.join([f'{name.split("-", 1)[1].split("_")[0]}[{str(dist)}]'
                                            for name, dist in compoundDist.items()])}_{compoundMode[0]}"""
            weightedGraphData = {name: pd.read_csv(f"{self.dataFilepath}{name}.csv",
                                                   names=['x', 'y'],
                                                   header=None) * [1, dist]
                                 for name, dist in compoundDist.items() if dist != 0}
            newElement = ElementData(name, None, None, None, None, None, None, None, True)
            newElement.setGraphDataFromDist(weightedGraphData.values())
            newElement.graphData.to_csv(f"{self.filepath}data\\Graph Data\\Compound Data\\{name}.csv",
                                        index=False,
                                        header=False)
            pd.DataFrame(compoundDist.items()).to_csv(
                f"{self.filepath}data\\Distribution Information\\{name}.csv", index=False, header=False)

            self.compoundNames.append(name)
            self.compoundCombobox.clear()
            self.compoundCombobox.addItems(self.compoundNames)
            self.defaultDistributions[name] = compoundDist
            self.elementDistributions[name] = deepcopy(compoundDist)
        applyBtn.clicked.connect(onAccept)
        cancelBtn.clicked.connect(optionsWindow.reject)

        def onReset():
            elements.lineEdit().clear()
            elements.clear()
            elements.addItems([self.combobox.itemText(i)
                               for i in range(self.combobox.count()) if 'element' in self.combobox.itemText(i)])
            totalLabel.setText("Total: 0")
            onRemove()
        resetBtn.clicked.connect(onReset)

        def onElementChange(index):

            elementName = elements.itemText(index)
            if elementName == '':
                addBtn.setEnabled(False)
                return
            if elementName in compoundElements.keys():
                addBtn.setEnabled(False)
                return
            addBtn.setEnabled(True)
        elements.editTextChanged.connect(lambda: onElementChange(elements.currentIndex()))

        def onAddRow(index=None):

            elementName = elements.itemText(elements.currentIndex() or 0)
            if elementName == '':
                elements.setCurrentIndex(0)
                return
            if compoundElements == {}:
                compoundMode.append(elementName.split('_')[-1])

                elements.currentIndexChanged.disconnect()
                elementNames = elements.getAllItemText()
                elements.clear()
                elements.addItems([name for name in elementNames if compoundMode[0] in name])
                elements.editTextChanged.connect(lambda: onElementChange(elements.currentIndex()))

            totalLabel.setStyleSheet("color: #FFF;")

            sublayout = QHBoxLayout()
            proxyWidget = QWidget()
            newQLineEdit = QLineEdit()
            newQLineEdit.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

            newQLineEdit.setValidator(QRegExpValidator(
                QRegExp("(0?(\\.[0-9]{1,6})?|1(\\.0{1,6})?)")))
            newQLineEdit.setPlaceholderText("0")
            title = QLabel(f"{elementName}:")
            removeBtn = QPushButton()
            removeBtn.setIcon(QIcon(".\\src\\img\\delete-component.svg"))
            removeBtn.setObjectName("compoundDelBtn")
            removeBtn.clicked.connect(lambda: onRemove(elementName))
            index = len(optionsWindow.children())
            sublayout.addWidget(title)
            sublayout.addWidget(newQLineEdit)
            sublayout.addWidget(removeBtn)
            sublayout.setSpacing(1)
            proxyWidget.setLayout(sublayout)
            proxyWidget.setFixedHeight(38)
            proxyWidget.setObjectName(f"{elementName}-RowWidget")
            newQLineEdit.textChanged.connect(onDistributionChange)
            optionsWindow.mainLayout.insertWidget(index - 3, proxyWidget)
            optionsWindow.updateGeometry()

            compoundElements[elementName] = 0
            onDistributionChange()
            addBtn.setEnabled(False)
        addBtn.clicked.connect(onAddRow)

        def onRemove(name: str = None):

            if name is None:
                for widget in getLayoutWidgets(optionsWindow.mainLayout, QWidget):
                    if "RowWidget" in widget.objectName():
                        optionsWindow.mainLayout.removeWidget(widget)
                        widget.deleteLater()
                compoundMode.clear()
                compoundElements.clear()
                applyBtn.setEnabled(False)
                return
            for widget in getLayoutWidgets(optionsWindow.mainLayout, QWidget):
                if widget.objectName() == f"{name}-RowWidget":
                    optionsWindow.mainLayout.removeWidget(widget)
                    widget.deleteLater()
                compoundElements.pop(name, None)
            onDistributionChange()

            if elements.itemText(elements.currentIndex() or 0) not in compoundElements.keys():
                addBtn.setEnabled(True)

        def onDistributionChange():

            total = 0
            for widget in getLayoutWidgets(optionsWindow.mainLayout, QWidget):
                lineEdit = widget.findChild(QLineEdit)
                distribution = lineEdit.placeholderText() if lineEdit.text() == '' else lineEdit.text()
                if distribution == ".":
                    continue
                total += float(distribution)

            total = round(total, 6)
            totalLabel.setText(f"Total: {total}")
            applyBtn.setEnabled(False)
            if total < 1:
                totalLabel.setStyleSheet("color: #FFF;")
            elif total > 1:
                totalLabel.setStyleSheet("color: #F00;")
            else:
                totalLabel.setStyleSheet("color: #0F0;")
                applyBtn.setEnabled(True)

            compoundDist = {
                widget.findChild(QLabel).text()[:-1]: float(widget.findChild(QLineEdit).text()) if widget.findChild(
                    QLineEdit).text() != '' else float(widget.findChild(QLineEdit).placeholderText())
                for widget in getLayoutWidgets(optionsWindow.mainLayout, QWidget)
            }
            name = f"""compound_{'-'.join([f'{name.split("-", 1)[1].split("_")[0]}[{str(dist)}]'
                                            for name, dist in compoundDist.items()])}"""
            if name in self.compoundNames:
                applyBtn.setEnabled(False)
                applyBtn.setToolTip("Compound Already Exists")
            else:
                applyBtn.setEnabled(True)
                applyBtn.setToolTip(None)

        elements.setFocus()
        onElementChange()
        optionsWindow.setModal(False)
        optionsWindow.show()

    def viewDarkStyle(self) -> None:
        """
        ``viewDarkStyle`` Applies the dark theme to the GUI.
        """
        self.setStyleSheet(self.styleMain.format(bg_color="#202020", text_color="#FFF"))

    def viewLightStyle(self) -> None:
        """
        ``viewLightStyle`` Applies the light theme to the GUI.
        """
        self.setStyleSheet(self.styleMain.format(bg_color="#968C80", text_color="#FFF"))

    def viewHighContrastStyle(self) -> None:
        """
        ``viewHighContrastStyle`` Applies the high contrast theme to the GUI.
        """
        self.setStyleSheet(self.styleMain.format(bg_color="#000", text_color="#FFF"))

    def toggleBtnControls(self, enableAll: bool = False, plotEnergyBtn: bool = False,
                          plotToFBtn: bool = False, clearBtn: bool = False, pdBtn: bool = False) -> None:
        """
        ``toggleBtnControls`` enables and disables the buttons controls, thus only allowing its
        use when required. enableAll is done before any kwargs have an effect on the buttons.
        enableAll defaults to False, True will enable all buttons regardless of other kwargs.
        This way you can disable all buttons then make changes to specific buttons.

        Args:
            ``enableAll`` (bool): Boolean to enable/disable (True/False) all the buttons controls.

            ``plotEnergyBtn`` (bool): Boolean to enable/disable (True/False) Plot Energy button.

            ``plotToFBtn`` (bool): Boolean to enable/disable (True/False) Plot ToF button.

            ``plotEnergyBtn`` (bool): Boolean to enable/disable (True/False) Plot Energy button.

            ``clearBtn`` (bool): Boolean to enable/disable (True/False) Plot Energy button.

            ``pdBtn`` (bool): Boolean to enable/disable (True/False) Peak Detection button.
        """

        for btn in getLayoutWidgets(self.btnLayout):
            btn.setEnabled(enableAll)

        if enableAll:
            return

        for btn in getLayoutWidgets(self.btnLayout):
            if btn.__name__ == 'plotEnergyBtn':
                btn.setEnabled(plotEnergyBtn)
            if btn.__name__ == 'plotToFBtn':
                btn.setEnabled(plotToFBtn)
            if btn.__name__ == 'clearBtn':
                btn.setEnabled(clearBtn)
            if btn.__name__ == 'pdBtn':
                btn.setEnabled(pdBtn)

    def toggleCheckboxControls(self, enableAll: bool, gridlines: bool = False,
                               peakLimit: bool = False, hidePeakLabels: bool = False) -> None:
        """
        ``toggleCheckboxControls`` enables and disables the checkboxes controls, thus only allowing its
        use when required. enableAll is done before any kwargs have an effect on the checkboxes.
        enableAll defaults to False, True will enable all checkboxes regardless of other kwargs.
        This way you can disable all checkboxes then make changes to specific checkboxes.

        Args:
            ``enableAll`` (bool): Boolean to enable/disable (True/False) all the buttons controls.

            ``gridlines`` (bool): Boolean to enable/disable (True/False) Plot Energy button.

            ``peakLimit`` (bool): Boolean to enable/disable (True/False) Plot ToF button.

            ``hidePeakLabels`` (bool): Boolean to enable/disable (True/False) Plot Energy button.

        """

        for btn in getLayoutWidgets(self.toggleLayout):
            if enableAll:  # Enable All then return
                btn.setEnabled(True)

            else:  # Otherwise disable all and apply kwargs
                btn.setEnabled(False)
                btn.setChecked(False)

        if enableAll:
            return

        for btn in getLayoutWidgets(self.toggleLayout):
            if btn.__name__ == 'gridCheck':
                btn.setEnabled(gridlines)
            if btn.__name__ == 'peakCheck':
                btn.setEnabled(hidePeakLabels)
            if btn.__name__ == 'pdCheck':
                btn.setEnabled(peakLimit)

    def plotSelectionProxy(self, index, comboboxName):
        """
        ``plotSelectionProxy`` Handles whether to selection made is from the compound list or not.

        Args:
            index (int): Index of selection given from PyQtSignal
            comboboxName (str): Identifier of combobox which made the signal.
        """

        self.combobox.blockSignals(True)
        self.compoundCombobox.blockSignals(True)

        if comboboxName == "compoundComboBox":
            self.combobox.setCurrentIndex(0)
            self.isCompound = True
            combobox = self.compoundCombobox
        if comboboxName == "combobox":
            self.compoundCombobox.setCurrentIndex(0)
            self.isCompound = False
            combobox = self.combobox

        self.combobox.blockSignals(False)
        self.compoundCombobox.blockSignals(False)
        self.resetTableProxy(combobox)

    def resetTableProxy(self, combobox) -> None:
        """
        ``resetTableProxy`` Handles setting the data in the table, either displaying the data from a single selection,
        or returning to the previous state of the table.

        Args:
            combobox (QComboBox): The Combobox from which the selection was made.
        """
        substanceNames = combobox.getAllItemText()
        try:
            if combobox.currentText() == '' and self.table_model is not None:
                self.table.setSortingEnabled(False)
                proxy = CustomSortingProxy()
                proxy.setSourceModel(self.table_model)

                self.table.setModel(proxy)
                self.table_model.titleRows = self.titleRows
                self.table.setModel(self.table_model)
                self.table.clearSpans()
                for row in self.titleRows[:-1]:
                    self.table.setSpan(row, 0, 1, 10)
                    self.table.setItemDelegateForRow(row, ButtonDelegate(self, self.table, self.table_model))
                    self.table.openPersistentEditor(self.table_model.index(row, 0))
                self.table.setSortingEnabled(True)

            elif combobox.currentText() in substanceNames:
                self.data = combobox.currentText()
                self.displayData()
        except AttributeError:
            self.table.setModel(None)

    def displayData(self) -> None:
        """
        ``displayData`` Will display relevant peak information in the table for the selection made (self.data).
        Once a select is made, the relevant controls are enabled.
        """
        if self.data == "" and self.plotCount > -1:  # Null selection and graphs shown
            self.toggleBtnControls(clearBtn=True)
            return
        elif self.data == "" and self.plotCount == -1:  # Null selection and no graphs shown
            self.toggleBtnControls(enableAll=False)
            self.toggleCheckboxControls(enableAll=False)
            return
        elif self.plotCount != -1:  # Named Selection and graphs shown
            self.toggleBtnControls(enableAll=True)
            self.toggleCheckboxControls(enableAll=True)
        else:  # Named selection and no graphs shown
            self.toggleBtnControls(plotEnergyBtn=True, plotToFBtn=True, clearBtn=True)
            self.toggleCheckboxControls(enableAll=False)

        # Getting symbol from element
        split = self.data.split("-")
        if self.data.startswith("e"):
            dataSymbolSort = split[1]
            dataSymbol = dataSymbolSort[:-2]
        else:
            dataSymbol = split[1]

        self.showTableData()

        self.threshold = self.thresholds.get(dataSymbol, 100)
        # Setting label information based on threshold value
        if self.threshold == 100:
            labelInfo = (
                "Threshold for peak detection for n-tot mode: 100"
            )

        else:
            labelInfo = (
                "Threshold for peak detection (n-tot mode, n-g mode): " + f"({self.threshold[0]},{self.threshold[1]})"
            )
            if self.data[-1] == 't':
                self.threshold = self.thresholds[dataSymbol][0]
            else:
                self.threshold = self.thresholds[dataSymbol][1]
        self.thresholdLabel.setText(str(labelInfo))
        # Changing the peak label text
        labelInfo = "Number of peaks: " + str(self.numRows)
        self.peaklabel.setText(str(labelInfo))

    def showTableData(self):
        """
        ``showTableData`` Read and display the selected substances data within the table.
        """
        # Finding relevant file for peak information
        peakInfoDir = self.filepath + "data/Peak information/"
        filepath = None
        for file in os.listdir(peakInfoDir):
            if self.data == file.split(".")[0]:
                filepath = peakInfoDir + file
                break
        try:
            for row in self.table_model.titleRows:
                self.table.setItemDelegateForRow(row, None)
        except AttributeError:
            pass
        try:
            self.table.blockSignals(True)
            file = pd.read_csv(filepath, header=0)
            # Reset any changes to spans before displaying selection data.
            self.table.clearSpans()

            if self.data not in self.plottedSubstances:
                self.numRows = file.shape[0]
            print("Number of peaks: ", self.numRows)
            # Fill Table with data
            tempTableModel = ExtendedQTableModel(file)
            proxy = CustomSortingProxy()
            proxy.setSourceModel(tempTableModel)

            self.table.setModel(proxy)
            self.table.setSortingEnabled(True)
            self.table.sortByColumn(0, Qt.SortOrder.AscendingOrder)
            self.peakInfoIsNull = False
            # if self.table_model is not None:

            # peak_plotEnergyBtn = QPushButton(self.table)      # If wanting a button to plot peak
            # peak_plotEnergyBtn.setText('Plot')         # Not sure how to get cell-clicked though
            # peak_plotEnergyBtn.clicked.connect(self.PlotPeak)
            # self.table.setCellWidget(row_count,10,peak_plotEnergyBtn)

        except ValueError:

            self.table.setModel(None)
            self.peakInfoIsNull = True
            self.numRows = None

    def addTableData(self, reset=False):
        # Amending the table for more than one plot.
        self.table.reset()
        self.table.sortByColumn(-1, Qt.SortOrder.AscendingOrder)

        table_data = pd.DataFrame()
        try:
            self.table_model.beginResetModel()
            self.table_model.endResetModel()
        except AttributeError:
            pass
        self.table.setModel(None)
        self.table_model = None
        self.table.setSortingEnabled(False)
        self.titleRows = [0]
        # ! ---------------------------------------------------------------------------------
        # ? Maybe sort the order in which they are plotted and added to the table.
        for element in self.elementData.values():
            if element.name not in self.elementDataNames:
                table_data = pd.concat([table_data, element.tableData], ignore_index=True)
                self.titleRows.append(self.titleRows[-1] + element.tableData.shape[0])
                self.elementDataNames.append(element.name)

        self.table_model = ExtendedQTableModel(table_data)

        proxy = CustomSortingProxy()
        proxy.setSourceModel(self.table_model)

        self.table.setModel(proxy)
        self.table.setSortingEnabled(True)
        self.table_model.titleRows = self.titleRows
        self.table.setModel(self.table_model)
        self.table.setSortingEnabled(True)
        self.table.clearSpans()
        for row in self.titleRows[:-1]:
            self.table.setSpan(row, 0, 1, 10)
            self.table.setItemDelegateForRow(row, ButtonDelegate(self, self.table, self.table_model))
            self.table.openPersistentEditor(self.table_model.index(row, 0))
        self.table.blockSignals(False)

    def updateGuiData(self, tof: bool = False, filepath: str = None, imported: bool = False, name: str = None,
                      distAltered: bool = False) -> None:
        """
        ``updateGuiData`` Will initialise the new element with its peak and graph data, updating the table and plot.
        Handles updates to isotopic distribution.
        Args:
            ``tof`` (bool, optional): Whether to graph for tof or not. Defaults to False.

            ``filepath`` (string, optional): Filepath for the selection to graph . Defaults to None.

            ``imported`` (bool, optional): Whether the selection imported. Defaults to False.

            ``name`` (string, optional): The name of the imported selection. Defaults to None.

            ``distAltered`` (bool, optional): Whether or not the function is plotted for altered isotope distributions.
            Defaults to False.

        """

        # Enable Checkboxes on plotting graphs
        self.toggleCheckboxControls(enableAll=True)
        self.toggleBtnControls(enableAll=True)

        if self.data is None and not imported:
            QMessageBox.warning(self, "Error", "You have not selected anything to plot")
            return
        if imported:
            self.data = name
            self.threshold = 100
        # Checks for adding mutliple graphs for the same selection, energy/tof types.
        if (self.data, tof) in self.plottedSubstances and not distAltered:
            QMessageBox.warning(self, "Warning", "Graph is already plotted")
            return

        # Establishing the number of peaks on the graph at one time, and their type
        if not imported and self.numRows != 0:
            if self.data not in self.plottedSubstances:
                self.numTotPeaks.append(self.numRows)

        if (self.data, tof) not in self.plottedSubstances:
            self.plottedSubstances.append((self.data, tof))
        # Handles number_totpeaks when plotting energy and tof of the same graph
        self.numTotPeaks.append(self.numRows)

        # # Finds the mode for L0 (length) parameter
        if self.data[-1] == "t":
            length = 23.404
        else:
            length = 22.804

        self.titleRows = [0]
        for (element, tof) in self.plottedSubstances:
            title = f"{element}-{'ToF' if tof else 'Energy'}"
            # ¦ -----------------------------------

            if title in self.elementData.keys():
                if self.elementData[title].isGraphDrawn:
                    continue
            if self.isCompound:
                self.plotFilepath = f"{self.filepath}data\\Graph Data\\Compound Data\\{element}.csv"
            else:
                self.plotFilepath = f"{self.filepath}data\\Graph Data\\{element}.csv" if filepath is None else filepath
            peakInfoDir = f"{self.filepath}data\\Peak information\\" if filepath is None else None

            try:
                graphData = pd.read_csv(self.plotFilepath, header=None)

            except pd.errors.EmptyDataError:
                QMessageBox.warning(self, "Warning", "Selection has Empty Graph Data")
                self.plottedSubstances.remove((self.data, tof))
                if self.plotCount == -1:
                    self.toggleCheckboxControls(enableAll=False)
                    self.toggleBtnControls(plotEnergyBtn=True, plotToFBtn=True, clearBtn=True, pdBtn=False)
                return
            except FileNotFoundError:
                if self.elementData.get(element, False):
                    self.elementData[element].graphData.to_csv(self.plotFilepath, index=False, header=False)
                    graphData = self.compoundData[element].graphData

            if tof and not graphData.empty:
                graphData[0] = self.energyToTOF(graphData[0], length=length)

            try:
                elementTableData = pd.read_csv(f"{peakInfoDir}{element}.csv")
            except FileNotFoundError:
                elementTableData = pd.DataFrame(
                    columns=[
                        "Rank by Integral",
                        "Energy (eV)",
                        "Rank by Energy",
                        "TOF (us)",
                        "Integral",
                        "Peak Width",
                        "Rank by Peak Width",
                        "Peak Height",
                        "Rank by Peak Height",
                        "Relevant Isotope"
                    ])
            # Title Rows
            if elementTableData.empty:
                elementTableData.loc[-1] = [f"No Peak Data for {element}", *[""] * 9]

            else:
                elementTableData.loc[-1] = [element, *[""] * 9]
            elementTableData.index += 1
            elementTableData.sort_index(inplace=True)

            if self.elementData.get(title, False):
                for point in self.elementData[title].annotations:
                    point.remove()

            newElement = ElementData(name=element,
                                     numPeaks=self.numRows,
                                     tableData=elementTableData,
                                     graphData=graphData,
                                     graphColour=getRandomColor(),
                                     isToF=tof,
                                     distributions=self.elementDistributions.get(element, None),
                                     defaultDist=self.defaultDistributions.get(element, None),
                                     isCompound=self.isCompound,
                                     isAnnotationsHidden=self.peakLabelCheck.isChecked(),
                                     threshold=float(self.threshold or 100),
                                     isImported=imported)

            self.elementData[title] = newElement

        redrawMax = False
        redrawMin = False
        if distAltered:
            for line in self.ax.get_lines():
                if newElement.name in line.get_label():
                    line.remove()
            try:
                for line in self.ax2.get_lines():
                    if 'max' in line.get_gid():
                        redrawMax = True
                    if 'min' in line.get_gid():
                        redrawMin = True
                    if newElement.name in line.get_label() or newElement.name in line.get_gid():
                        line.remove()

            except AttributeError:
                pass

        distAltered = False

        self.plot(newElement, filepath, imported, name)
        if redrawMax:
            self.PlottingPD(newElement, True)
        if redrawMin:
            self.PlottingPD(newElement, False)
        self.addTableData()

        self.canvas.draw()

    def plot(self, elementData: ElementData, filepath: str = None, imported: bool = False, name: str = None) -> None:
        if elementData is None:
            return
        # Re-setting Arrays
        self.x = []
        self.y = []
        # Establishing colours for multiple plots

        # General Plotting ---------------------------------------------------------------------------------------------
        if self.plotCount < 0:
            self.ax = self.figure.add_subplot(111)
            # Setting scale to be logarithmic
            self.ax.set_yscale("log")
            self.ax.set_xscale("log")
            self.ax.minorticks_on()
            self.ax.xaxis.set_tick_params('both', bottom=True)

        # Allows user to plot in ToF if chosen # -----------------------------------------------------------------------
        if elementData.isToF and not imported:
            # ! Convert to pandas compatible

            if self.plotCount < 0:
                self.ax.set(
                    xlabel="ToF (uS)", ylabel="Cross section (b)", title=self.data
                )
        else:
            if self.plotCount < 0:
                if elementData.isToF:
                    self.ax.set(
                        xlabel="Time of Flight (uS)",
                        ylabel="Cross section (b)",
                        title=self.data,
                    )
                else:
                    self.ax.set(
                        xlabel="Energy (eV)",
                        ylabel="Cross section (b)",
                        title=self.data,
                    )
            else:
                self.ax.set(title=None)

        # Plotting -----------------------------------------------------------------------------------------------------

        label = f"{elementData.name}-ToF" if elementData.isToF else f"{elementData.name}-Energy"

        if not elementData.graphData.empty:

            self.ax.plot(
                elementData.graphData.iloc[:, 0],
                elementData.graphData.iloc[:, 1],
                "-",
                c=elementData.graphColour,
                alpha=0.6,
                linewidth=0.8,
                label=label,
                gid=elementData.name if self.data is None else self.data,
            )
            elementData.isGraphDrawn = True
            self.updateLegend()

            # Establishing plot count
            self.plotCount += 1

            self.drawAnnotations(elementData)
            self.toggleThreshold()
            self.ax.autoscale()  # Tidying up

            self.figure.tight_layout()
        self.canvas.draw()

    def updateLegend(self):
        # Creating a legend to toggle on and off plots--------------------------------------------------------------

        legend = self.ax.legend(fancybox=True, shadow=True)

        if len(self.ax.get_lines()) == 0:
            self.clear()
            return
        # Amending dictionary of plotted lines - maps legend line to original line and allows for picking
        self.legOrigLines = {}
        for legLine in legend.get_lines():
            for origLine in self.ax.get_lines():
                if origLine.get_label() == legLine.get_label():
                    legLine.set_picker(True)
                    legLine.set_linewidth(1.5)
                    legLine.set_pickradius(7)
                    legLine.set_color(self.elementData[origLine.get_label()].graphColour)
                    legLine.set_alpha(1.0 if origLine.get_visible() else 0.2)

                    self.legOrigLines[legLine] = origLine

    def energyToTOF(self, xData: list[float], length: float) -> list[float]:
        """
        Maps all X Values from energy to TOF

        Args:
            ``xData`` (list[float]): List of the substances x-coords of its graph data

            ``length`` (float): Constant value associated to whether the element data is with repsect to n-g or n-tot


        Returns:
            list[float]: Mapped x-coords
        """
        if length is None:
            length = 22.804
        neutronMass = float(1.68e-27)
        electronCharge = float(1.60e-19)

        tofX = list(
            map(
                lambda x: length * 1e6 * (0.5 * neutronMass / (x * electronCharge)) ** 0.5,
                xData
            )
        )
        return tofX

    def hideGraph(self, event) -> None:
        """
        Function to show or hide the selected graph by clicking the legend.

        Args:
            ``event`` (pick_event): event on clicking a graphs legend
        """
        # Tells you which plot number you need to deleteLater() labels for

        legline = event.artist
        if self.ax.get_visible():
            axis, legOrigLines = self.ax, self.legOrigLines
        if self.ax2 is not None:
            if self.ax2.get_visible():
                axis, legOrigLines = self.ax2, self.legOrigLinesPD

        if legline not in legOrigLines:
            return
        origLine = legOrigLines[legline]
        orgline_name = legline.get_label()
        # Hiding relevant line
        newVisible = not origLine.get_visible()
        # Change the alpha on the line in the legend so we can see what lines
        # have been toggled.
        legline.set_alpha(1.0 if newVisible else 0.2)
        origLine.set_visible(newVisible)
        # Hiding relevant labels
        elementData = self.elementData[orgline_name]
        elementData.isGraphHidden = not newVisible
        elementData.HideAnnotations(self.peakLabelCheck.isChecked())
        for line in axis.lines:
            if line.get_gid() == f"pd_threshold-{orgline_name}":
                line.set_visible(newVisible)
                continue
            if f"{elementData.name}-{'ToF' if elementData.isToF else 'Energy'}-max" in line.get_gid():
                line.set_visible(newVisible)
                continue
            if f"{elementData.name}-{'ToF' if elementData.isToF else 'Energy'}-min" in line.get_gid():
                line.set_visible(newVisible)
                continue

        self.canvas.draw()

    def clear(self) -> None:
        """
        clear Function will empty all data from the table, all graphs from the plots,
        along with resetting all data associated the table or plot and disables relevent controls.
        """

        self.figure.clear()
        self.ax.clear()
        self.ax2 = None
        self.canvas.draw()
        self.x = []
        self.y = []
        self.plotCount = -1
        self.numTotPeaks = []
        self.annotations = []
        self.localHiddenAnnotations = []
        self.peaklabel.setText("")
        self.thresholdLabel.setText("")
        self.elementData = {}
        self.elementDataNames = []
        try:
            for row in self.table_model.titleRows:
                self.table.setItemDelegateForRow(row, None)
        except AttributeError:
            pass
        self.table.setModel(None)
        self.graphs = dict()
        self.tableLayout = dict()
        self.table_model = None
        self.arrays = dict()
        self.plottedSubstances = []
        self.elementDistributions = deepcopy(self.defaultDistributions)

        self.toggleBtnControls(plotEnergyBtn=True, plotToFBtn=True, clearBtn=True)
        self.toggleCheckboxControls(enableAll=False)

    def toggleGridlines(self, visible: bool,
                        which: Literal["major", "minor", "both"] = "major",
                        axis: Literal["both", "x", "y"] = "both",
                        color="#444") -> None:
        """
        ``toggleGridlines`` Will toggle visibility of the gridlines on the axis which is currently shown.


        Args:
            ``visible`` (bool): Whether or not gridlines should be shown.

            ``which`` (Literal["major", "minor", "both"], optional):
            Whether to show major, minor or both gridline types. Defaults to "major".

            ``axis`` (Literal["both", "x", "y"], optional):
            Whether or not to show gridlines on x, y, or both. Defaults to "both".

            ``color`` (str, optional): Gridline Color. Defaults to "#444".
        """
        try:
            # if self.gridSettings["which"] == "major":
            #     plt.minorticks_off()
            #     self.ax.minorticks_off()
            # else:
            #     plt.minorticks_on()
            #     self.ax.minorticks_on()
            self.ax.minorticks_on()

            self.ax.tick_params(which='minor', axis='x')
            self.ax.tick_params(**self.gridSettings)
            self.ax.grid(visible=False, which='both')
            if visible and self.ax.get_visible():
                self.ax.grid(visible=visible, which=which, axis=axis, color=color, alpha=0.2)
            else:
                self.ax.grid(visible=visible, which="both")
            if visible and self.ax2.get_visible():
                self.ax2.grid(visible=visible, which=which, axis=axis, color=color, alpha=0.2)
            else:
                self.ax.grid(visible=visible, which="both")
        except AttributeError:
            pass
        self.canvas.draw()

    def toggleThreshold(self) -> None:
        """
        Plots the threshold line for each plotted element at their respective limits.
        """
        checked = self.thresholdCheck.isChecked()

        for line in self.ax.get_lines():
            if line is None:
                continue
            if line.get_gid() is None:
                continue
            if "pd_threshold" in line.get_gid():
                line.remove()
        try:
            for line in self.ax2.get_lines():
                if line is None:
                    continue
                if line.get_gid() is None:
                    continue
                if "pd_threshold" in line.get_gid():
                    line.remove()
        except AttributeError:
            pass
        self.canvas.draw()
        if checked:
            for name, element in self.elementData.items():
                self.figure.add_subplot(self.ax)
                if self.ax.get_visible():
                    line = self.ax.axhline(
                        y=element.threshold,
                        linestyle="--",
                        color=element.graphColour,
                        linewidth=0.5,
                        gid=f"pd_threshold-{name}"
                    )
                try:
                    if self.ax2.get_visible() and (element.isMaxDrawn or element.isMinDrawn):
                        line = self.ax2.axhline(
                            y=element.threshold,
                            linestyle="--",
                            color=element.graphColour,
                            linewidth=0.5,
                            gid=f"pd_threshold-{name}"
                        )
                except AttributeError:
                    pass
                if element.isGraphHidden:
                    line.set_visible(False)

                self.canvas.draw()

    def onPeakOrderChange(self) -> None:
        if self.sender().objectName() == "orderByIntegral":
            self.orderByIntegral = self.byIntegralCheck.isChecked()

        if self.sender().objectName() == "orderByPeakW":
            self.orderByIntegral = self.byIntegralCheck.isChecked()

        for element in self.elementData.values():
            self.drawAnnotations(element)

    def drawAnnotations(self, element: ElementData) -> None:
        """
        ``drawAnnotations`` will plot each numbered annotation in the order of Integral or Peak Width

        Args:
            ``element`` (ElementData): The data for the element your annotating
        """
        self.elementDataNames = []

        if element.isAnnotationsDrawn:
            for anno in element.annotations:
                anno.remove()
            element.annotations.clear()

        if element.maxima.size == 0:
            return

        if element.tableData is not None:
            element.OrderAnnotations(self.orderByIntegral)

        gid = f"annotation-{element.name}-" + "ToF" if element.isToF else "Energy"
        xy = element.maxima.T if element.annotationsOrder == {} or element.isDistAltered else element.annotationsOrder
        if element.isDistAltered:
            maxDraw = len(xy)
        else:
            maxDraw = element.maxPeaks if element.maxPeaks < element.numPeaks else element.numPeaks
        element.annotations = [self.ax.annotate(text=f'{i}',
                                                xy=xy[i],
                                                xytext=xy[i],
                                                xycoords="data",
                                                textcoords="data",
                                                va="center",
                                                size=6,
                                                gid=gid,
                                                annotation_clip=True,
                                                alpha=0.8
                                                )
                               for i in
                               (range(0, maxDraw) if type(xy) is np.ndarray else xy.keys())
                               if i < maxDraw]
        if element.isGraphHidden or self.peakLabelCheck.isChecked():
            for annotation in element.annotations:
                annotation.set_visible(False)
            element.isAnnotationsHidden = True
        element.isAnnotationsDrawn = True
        self.canvas.draw()

    def toggleAnnotations(self) -> None:
        """
        Function Annotations shows & hides all peak annotations globally.
        """
        for element in self.elementData.values():
            element.HideAnnotations(self.peakLabelCheck.isChecked())
            element.isAnnotationsHidden = not element.isAnnotationsHidden

        self.canvas.draw()

    def PlotPeakWindow(self, row_clicked) -> None:

        peakWindow = QMainWindow(self)
        # Setting title and geometry
        peakWindow.setWindowTitle("Peak Plotting")
        peakWindow.setGeometry(350, 50, 850, 700)
        peakWindow.setObjectName("mainWindow")
        peakWindow.setStyleSheet(self.styleSheet())
        # Creating a second canvas for singular peak plotting
        peakFigure = plt.figure()
        self.peakCanvas = FigureCanvas(peakFigure, contextConnect=False)
        toolbar = NavigationToolbar(self.peakCanvas, self)
        canvasLayout = QVBoxLayout()

        canvasProxyWidget = QWidget()
        canvasProxyWidget.setObjectName("peakCanvasContainer")
        canvasLayout.addWidget(toolbar)
        canvasLayout.addWidget(self.peakCanvas)

        canvasProxyWidget.setLayout(canvasLayout)

        # Setting up dock for widgets to be used around canvas
        dock = QDockWidget(parent=peakWindow)
        # Creating a widget to contain peak info in dock
        peak_info_widget = QWidget()

        # Creating layout to display peak info in the widget
        layout2 = QVBoxLayout()
        toggle_layout2 = QHBoxLayout()

        # Adding checkbox to toggle the peak limits on and off
        threshold_check2 = QCheckBox("Integration Limits", peakWindow)
        threshold_check2.resize(threshold_check2.sizeHint())
        threshold_check2.setObjectName("peakCheck")
        threshold_check2.setChecked(True)
        toggle_layout2.addWidget(threshold_check2)

        # Adding checkbox to toggle the peak detection limits on and off
        threshold_check3 = QCheckBox("Peak Detection Limits", peakWindow)
        threshold_check3.setObjectName("peakCheck")
        threshold_check3.resize(threshold_check3.sizeHint())
        toggle_layout2.addWidget(threshold_check3)
        # Adding to overall layout
        layout2.addLayout(toggle_layout2)

        peakTable = QTableView()

        layout2.addWidget(peakTable)

        # Adding label which shows what scale the user picks
        scale_label = QLabel()
        scale_label.setObjectName("peakLabel")
        layout2.addWidget(scale_label)

        # Setting layout within peak info widget
        peak_info_widget.setLayout(layout2)
        dock.setWidget(peak_info_widget)  # Adding peak info widget to dock

        peakWindow.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock)
        # Setting canvas as central widget
        peakWindow.setCentralWidget(canvasProxyWidget)

        self.peakAxis = peakFigure.add_subplot(111)

        try:
            titleIndex = sorted([index for index in self.titleRows if row_clicked.row() > index])[-1]
            elementName = self.table_model.data(self.table_model.index(titleIndex, 0), 0)
            tof = False  # ! Handle Tof / Energy peaks
            elementTitle = f"{elementName}-{'ToF' if tof else 'Energy'}"
            element = self.elementData[elementTitle]
            if element.maxima.size == 0:
                return
            maximaX = nearestnumber(element.maxima[0], float(self.table_model.data(
                self.table_model.index(row_clicked.row(), 3 if tof else 1), 0)))
            maxima = [max for max in element.maxima.T if max[0] == maximaX][0]

            if element.maxPeakLimitsX == dict():
                peakLimits = pd.read_csv(f"{self.filepath}data\\Peak Limit Information\\{elementName}.csv")
                leftLimit, rightLimit = peakLimits.iloc[(peakLimits.iloc[:, 0] <= maxima[0]) & (
                    peakLimits.iloc[:, 1] >= maxima[0])]

            else:
                leftLimit, rightLimit = element.maxPeakLimitsX[maxima[0]]

        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "No peak limits for this Selection")
        except AttributeError:
            QMessageBox.warning(self, "Warning", "Plot the Graph First")

        rank = [str([ann[0] for ann in element.annotationsOrder.items() if ann[1][0] == maxima[0]][0])]
        limits = [str(element.maxPeakLimitsX[maxima[0]])]
        peakCoords = [f"({maxima[0]}, {maxima[1]})"]
        isoOrigin = [self.table_model.data(self.table_model.index(row_clicked.row(), 9), 0)]
        data = {"Peak Number (Rank)": rank,
                "Integration Limits (eV)": limits,
                "Peak Co-ordinates (eV)": peakCoords,
                "Isotopic Origin": isoOrigin}

        tableData = pd.DataFrame(data, index=None)

        peakTable.setModel(ExtendedQTableModel(tableData))

        peakTable.setObjectName('dataTable')
        peakTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        peakTable.setAlternatingRowColors(True)
        peakTable.verticalHeader().setVisible(False)
        peakTable.setMinimumHeight(200)

        graphData = element.graphData[(element.graphData[0] >= leftLimit) & (element.graphData[0] <= rightLimit)]

        def togglePeakLimits(self) -> None:
            for line in self.peakAxis.get_lines():
                if "PeakWindow-lim" in line.get_gid():
                    line.set_visible(threshold_check2.isChecked())
        threshold_check2.clicked.connect(togglePeakLimits)

        def togglePeakThreshold(self, checked, element) -> None:
            if not threshold_check3.isChecked():
                for line in self.peakAxis.get_lines():
                    if line.get_gid() == f"PeakWindow-Threshold-{element.name}":
                        line.remove()
            else:
                self.peakAxis.axhline(y=element.threshold,
                                      linestyle="--",
                                      color=element.graphColour,
                                      linewidth=0.5,
                                      gid=f"PeakWindow-Threshold-{element.name}")
        threshold_check3.clicked.connect(togglePeakThreshold)

        peakWindow.show()

        self.peakAxis.set_xscale('log')
        self.peakAxis.set_yscale('log')

        self.peakAxis.set(
            xlabel="Energy (eV)", ylabel="Cross section (b)", title=elementTitle
        )

        self.peakAxis.plot(graphData[0],
                           graphData[1],
                           color=element.graphColour,
                           linewidth=0.8,
                           label=elementTitle,
                           gid=f"{elementTitle}-PeakWindow"
                           )

        self.peakAxis.plot(maxima[0],
                           maxima[1],
                           "x",
                           color="black",
                           markersize=3,
                           alpha=0.6,
                           gid=f"{elementTitle}-PeakWindow-max"
                           )

        for i, (peakX, peakY) in enumerate(zip(element.maxPeakLimitsX[maxima[0]], element.maxPeakLimitsY[maxima[0]])):
            self.peakAxis.plot(peakX,
                               peakY,
                               marker=2,
                               color="r",
                               markersize=8,
                               gid=f"{elementTitle}-PeakWindow-lim-{i}")

        self.peakAxis.autoscale()
        peakFigure.tight_layout()
        self.peakAxis.legend(fancybox=True, shadow=True)

    def importdata(self) -> None:
        """
        Allows user to select a file on their computer to open and analyse.
        """
        filename = QFileDialog.getOpenFileName(self, "Open file", self.filepath)
        if filename[0] == '':
            return
        filepath = filename[0]
        getName = filepath.split("/")

        name = getName[-1].split('.')[0]

        if name[-1] == "f":
            self.updateGuiData(True, filepath, True, name)
        else:
            self.updateGuiData(False, filepath, True, name)

    def GetPeaks(self) -> None:
        """
        Ask the user for which function to plot the maxima or minima of which element
        then calls the respective function on that element
        """

        mainLayout = QVBoxLayout()
        inputForm = QFormLayout()
        inputForm.setObjectName('inputForm')

        elements = QComboBox()
        elements.setEditable(True)
        elements.addItems(self.elementData.keys())
        elements.setMaxVisibleItems(5)

        elements.completer().setCompletionMode(
            QCompleter.UnfilteredPopupCompletion
        )

        elements.completer().setCaseSensitivity(Qt.CaseInsensitive)
        elements.completer().setFilterMode(Qt.MatchContains)

        inputMaxPeaks = QLineEdit()
        inputMaxPeaks.setPlaceholderText(str(self.elementData[elements.currentText()].threshold))
        inputMaxPeaks.setValidator(QRegExpValidator(QRegExp("[+-]?([0-9]*[.])?[0-9]+")))

        inputForm.addRow(QLabel("Substance:"), elements)
        buttonBox = QDialogButtonBox()
        resetBtn = buttonBox.addButton(QDialogButtonBox.Reset)
        resetBtn.setText("Reset")
        maximaBtn = buttonBox.addButton(QDialogButtonBox.Yes)
        maximaBtn.setText("Maxima")
        minimaBtn = buttonBox.addButton(QDialogButtonBox.No)
        minimaBtn.setText("Minima")
        cancelBtn = buttonBox.addButton(QDialogButtonBox.Cancel)
        cancelBtn.setText("Cancel")

        inputForm.setSpacing(5)
        mainLayout.addItem(inputForm)
        mainLayout.addWidget(buttonBox)

        inputWindow = QDialog(self)
        inputWindow.setObjectName("inputWindow")
        inputWindow.setModal(True)

        inputWindow.setWindowTitle("What Should I Plot?")
        inputWindow.setLayout(mainLayout)

        def max():
            self.PlottingPD(self.elementData[elements.currentText()], True)
        maximaBtn.clicked.connect(max)

        def min():
            self.PlottingPD(self.elementData[elements.currentText()], False)
        minimaBtn.clicked.connect(min)

        def close():
            inputWindow.close()
        cancelBtn.clicked.connect(close)

        def changePeaksText():
            inputMaxPeaks.setPlaceholderText(str(self.elementData[elements.currentText()].maxPeaks))
            maxCheck = self.elementData[elements.currentText()].maxima.size != 0
            minCheck = self.elementData[elements.currentText()].minima.size != 0

            maximaBtn.setEnabled(maxCheck)
            minimaBtn.setEnabled(minCheck)

            maximaBtn.setToolTip('' if maxCheck else "No Maximas Found")
            minimaBtn.setToolTip('' if minCheck else "No Minimas Found")

        elements.activated.connect(changePeaksText)
        changePeaksText()
        inputWindow.show()

        def ResetPDPlots() -> None:
            try:
                if self.ax2 is not None:
                    self.ax2.set_visible(False)
                    self.ax2.clear()
                    self.ax2.remove()
                    self.ax2 = None

                self.ax.set_visible(True)
                for element in self.elementData.values():
                    element.isMaxDrawn = False
                    element.isMinDrawn = False
            except KeyError:
                return
            self.toggleThreshold()
            self.toggleGridlines(self.gridCheck.isChecked(), *self.gridSettings.values())
            self.toolbar.update()
            self.canvas.draw()
        resetBtn.clicked.connect(ResetPDPlots)

    def PlottingPD(self, elementData: ElementData, isMax: bool) -> None:
        """
        ``PlottingPD`` takes plots the maximas or minimas of the inputted ``elementData`` based on ``isMax``

        Args:
            ``elementData`` (ElementData): ElementData Class specifying the element

            ``isMax`` (bool): Maxima if True else Minima
        """
        if elementData.isMinDrawn and not isMax and not elementData.isGraphUpdating:
            return
        if elementData.isMaxDrawn and isMax and not elementData.isGraphUpdating:
            return
        if isMax:
            peaksX, peaksY = elementData.maxima[0], elementData.maxima[1]

        else:
            peaksX, peaksY = elementData.minima[0], elementData.minima[1]

        # ! Add element selection to Peak Detection menu
        # ! Change how points are then plotted
        # Redrawing graph and Peak Detection Limits
        self.ax.set_visible(False)

        if self.ax2 is None:
            self.ax2 = self.figure.add_subplot(111)

        self.toggleGridlines(self.gridCheck.isChecked(), **self.gridSettings)

        self.ax2.set_visible(True)

        label = f"{elementData.name}-ToF" if elementData.isToF else f"{elementData.name}-Energy"
        if not elementData.isMaxDrawn and not elementData.isMinDrawn and not elementData.isGraphUpdating:
            self.ax2.plot(
                elementData.graphData[0],
                elementData.graphData[1],
                "-",
                color=elementData.graphColour,
                alpha=0.6,
                linewidth=0.8,
                label=label,
                gid=f"{elementData.name}-PD"
            )
        self.toggleThreshold()
        self.drawAnnotations(elementData)
        self.ax2.set_xscale("log")
        self.ax2.set_yscale("log")
        self.ax2.set(xlabel="Energy (eV)", ylabel="Cross section (b)", title=str(self.data))

        if isMax:
            pdPoints = [
                a for a in self.ax2.get_lines() if "max" in a.get_gid() and elementData.name in a.get_gid()
            ]
            pdPointsXY = [(point.get_xdata()[0], point.get_ydata()[0])
                          for point in pdPoints]
            peaks = list(zip(peaksX, peaksY))
            removeIds = []
            for point in pdPoints:
                if "max-p" not in point.get_gid():
                    continue
                xy = (point.get_xdata()[0], point.get_ydata()[0])
                if xy not in peaks:
                    removeIds.append(point.get_gid().split('-')[-1])
            if removeIds != []:
                for point in pdPoints:
                    if point.get_gid().split('-')[-1] in removeIds:
                        point.remove()

            for i, (x, y) in enumerate(zip(peaksX, peaksY)):
                if (x, y) in pdPointsXY:
                    continue
                self.ax2.plot(x,
                              y,
                              "x",
                              color="black",
                              markersize=3,
                              alpha=0.6,
                              gid=f"{elementData.name}-{'ToF' if elementData.isToF else 'Energy'}-max-p-{i}")
                elementData.isMaxDrawn = True
                if elementData.maxPeakLimitsX.get(x, False):
                    limitXFirst = elementData.maxPeakLimitsX[x][0]
                    limitXSecond = elementData.maxPeakLimitsX[x][1]
                else:
                    continue
                if elementData.maxPeakLimitsY.get(x, False):
                    limitYFirst = elementData.maxPeakLimitsY[x][0]
                    limitYSecond = elementData.maxPeakLimitsY[x][1]
                else:
                    continue

                self.ax2.plot(limitXFirst,
                              limitYFirst,
                              marker=2,
                              color="r",
                              markersize=8,
                              gid=f"{elementData.name}-{'ToF' if elementData.isToF else 'Energy'}-max-limL-{i}")
                self.ax2.plot(limitXSecond,
                              limitYSecond,
                              marker=2,
                              color="r",
                              markersize=8,
                              gid=f"{elementData.name}-{'ToF' if elementData.isToF else 'Energy'}-max-limR-{i}")

        else:
            for x, y in zip(peaksX, peaksY):
                self.ax2.plot(x,
                              y,
                              "x",
                              color="black",
                              markersize=3,
                              alpha=0.6,
                              gid=f"{elementData.name}-{'ToF' if elementData.isToF else 'Energy'}-min")
                elementData.isMinDrawn = True

                # limitXFirst = elementData.minPeakLimitsX[f"{x}_first"]
                # limitYFirst = elementData.minPeakLimitsY[f"{x}_first"]
                # limitXSecond = elementData.minPeakLimitsX[f"{x}_second"]
                # limitYSecond = elementData.minPeakLimitsY[f"{x}_second"]
                # self.ax2.plot(limitXFirst, limitYFirst, 0, color="r", markersize=8)
                # self.ax2.plot(limitXSecond, limitYSecond, 0, color="r", markersize=8)
        legendPD = self.ax2.legend(fancybox=True, shadow=True)
        self.legOrigLinesPD = {}
        origlines = [line for line in self.ax2.get_lines() if not ('max' in line.get_gid() or 'min' in line.get_gid())]
        for legLine, origLine in zip(legendPD.get_lines(), origlines):
            legLine.set_picker(True)
            legLine.set_linewidth(1.5)
            legLine.set_pickradius(7)
            legLine.set_color(self.elementData[origLine.get_label()].graphColour)
            legLine.set_alpha(1.0 if origLine.get_visible() else 0.2)
            self.legOrigLinesPD[legLine] = origLine

        self.figure.tight_layout()
        self.toolbar.update()
        self.toolbar.push_current()
        elementData.isGraphUpdating = False
        self.canvas.draw()


def main() -> None:

    app = QtWidgets.QApplication(sys.argv)
    app.setObjectName('MainWindow')

    app.setStyle('Fusion')
    QtGui.QFontDatabase.addApplicationFont('src\\fonts\\RobotoMono-Thin.ttf')
    QtGui.QFontDatabase.addApplicationFont('src\\fonts\\RobotoMono-Regular.ttf')
    QtGui.QFontDatabase.addApplicationFont('src\\fonts\\RobotoMono-Medium.ttf')
    Colours = QtGui.QPalette()
    # Colours.setColor(QtGui.QPalette.Window, QtGui.QColor("#393939"))
    # Colours.setColor(QtGui.QPalette.Button, QtGui.QColor("#FFF"))

    app.setWindowIcon(QIcon("./src/img/final_logo.png"))

    _ = DatabaseGUI()
    app.setPalette(Colours)
    app.exec()


if __name__ == "__main__":
    main()