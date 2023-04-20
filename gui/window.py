from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 

import backend.images
import backend.audio
import backend.pdf
import backend.docx
import backend.xlsx
import gui.support


datatypes = []

class MainWindow(QMainWindow):
    
    file_type = gui.support.Filetype.NONE
    file_path = None

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("MetEx")
        self.resize(800, 600)

        self._createActions()
        self._createMenuBar()
        self._createTable()
        self._createStatusBar()

    def open(self):
        self.file_path = QFileDialog.getOpenFileName(self, "Open")[0]
        self._checkFileType()
        self._loadTable()

    def save(self):
        metadata = []
        for i in range(self.tableWidget.rowCount()):
            metadata.append((self.tableWidget.item(i, 0).text(), self.tableWidget.item(i, 1).text()))
        print(metadata)
        match self.file_type:
            case gui.support.Filetype.IMAGE:
                backend.images.save(self.file_path, metadata, self.datatypes)
            case gui.support.Filetype.AUDIO:
                backend.audio.save(self.file_path, metadata, self.datatypes)
            case gui.support.Filetype.PDF:
                backend.pdf.save(self.file_path, metadata, self.datatypes)
            case gui.support.Filetype.WORD:
                backend.docx.save(metadata, self.file_path, self.file_path, self.datatypes)
            case gui.support.Filetype.EXCEL:
                backend.xlsx.save(metadata, self.file_path, self.file_path, self.datatypes)

    def about(self):
        text = "<center>" \
            "<h3>Metadata extraction and edition tool</h3>" \
            "&#8291;" \
            "</center>"
        QMessageBox.about(self, "About MetEx", text)

    def _createStatusBar(self):
        self.statusBar = self.statusBar()

        self.discardButton = QPushButton("Discard")
        self.statusBar.addWidget(self.discardButton)

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.save)
        self.exitButton = QPushButton("Exit")
        self.exitButton.clicked.connect(self.close)
        self.statusBar.addAction(self.exitAction)
        self.statusBar.addPermanentWidget(self.saveButton)
        self.statusBar.addPermanentWidget(self.exitButton)

    def _createMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)
        optionsMenu = menuBar.addMenu("&Options")
        optionsMenu.addAction(self.undoAction)
        helpMenu = menuBar.addMenu("&Help")
        helpMenu.addAction(self.aboutAction)

    def _createActions(self):
        self.openAction = QAction("&Open", self)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.open)
        self.saveAction = QAction("&Save", self)
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)
        self.exitAction = QAction("&Exit", self)
        self.exitAction.setShortcut("Ctrl+Q")
        self.exitAction.triggered.connect(self.close)
        self.undoAction = QAction("&Undo", self)
        self.undoAction.setShortcut("Ctrl+Z")
        self.aboutAction = QAction("&About", self)
        self.aboutAction.setShortcut("Ctrl+I")
        self.aboutAction.triggered.connect(self.about)

    def _createTable(self): # filled with test data
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(2)  
  
        self.tableWidget.setItem(0,0, QTableWidgetItem("Name"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("City"))
        self.tableWidget.setItem(1,0, QTableWidgetItem("Aloysius"))
        self.tableWidget.setItem(1,1, QTableWidgetItem("Indore"))
        self.tableWidget.setItem(2,0, QTableWidgetItem("Alan"))
        self.tableWidget.setItem(2,1, QTableWidgetItem("Bhopal"))
        self.tableWidget.setItem(3,0, QTableWidgetItem("Arnavi"))
        self.tableWidget.setItem(3,1, QTableWidgetItem("Mandsaur"))
   
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.setCentralWidget(self.tableWidget)
    
    def _checkFileType(self):
        extension = self.file_path.split(".")[-1]
        if extension in ['jpg', 'jpeg', 'png', 'tiff', 'tif']:
            self.file_type = gui.support.Filetype.IMAGE
        elif extension == 'pdf':
            self.file_type = gui.support.Filetype.PDF
        elif extension == 'mp3':
            self.file_type = gui.support.Filetype.AUDIO
        elif extension == 'docx':
            self.file_type = gui.support.Filetype.WORD
        elif extension == 'xlsx':
            self.file_type = gui.support.Filetype.EXCEL
        else:
            self.file_type = gui.support.Filetype.NONE

    def _loadTable(self):
        match self.file_type:
            case gui.support.Filetype.IMAGE:
                metadata, datatypes = backend.images.read(self.file_path)
                self.datatypes = datatypes
            case gui.support.Filetype.AUDIO:
                metadata, datatypes = backend.audio.read(self.file_path)
                self.datatypes = datatypes
            case gui.support.Filetype.PDF:
                metadata, datatypes = backend.pdf.read(self.file_path)
                self.datatypes = datatypes
            case gui.support.Filetype.WORD:
                metadata, datatypes = backend.docx.read(self.file_path)
                self.datatypes = datatypes
            case gui.support.Filetype.EXCEL:
                metadata = backend.xlsx.read(self.file_path)
                datatypes = None
                self.datatypes = datatypes
            case '_':
                self.statusBar.showMessage("File format not supported", 5000)
                return
            
        print(metadata, datatypes)
        self.tableWidget.setRowCount(len(metadata))
        self.tableWidget.setColumnCount(2)
        for i, (key, value) in enumerate(metadata):
            k = QTableWidgetItem(str(key))
            k.setFlags(k.flags() & Qt.ItemIsEditable)
            k.setForeground(Qt.black)
            self.tableWidget.setItem(i, 0, k)
            v = QTableWidgetItem(str(value))
            v.setFlags(v.flags() | Qt.ItemIsEditable)
            self.tableWidget.setItem(i, 1, v)

        self.statusBar.showMessage("File loaded", 5000)

