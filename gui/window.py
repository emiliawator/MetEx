from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtGui import *

import backend.images
import backend.audio
import backend.pdf
import backend.docx
import backend.xlsx
import backend.pptx
import gui.support


datatypes = []
readonly = [] # read-only metadata keys for current file

class MainWindow(QMainWindow):
    
    file_type = gui.support.Filetype.NONE
    file_path = None

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("MetEx")
        self.resize(800, 600)

        self._createActions()
        self._createMenuBar()
        self._createWelcomePage()
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
                errors = backend.images.save(self.file_path, metadata, self.readonly)
            case gui.support.Filetype.AUDIO:
                errors = backend.audio.save(self.file_path, metadata)
            case gui.support.Filetype.PDF:
                errors = backend.pdf.save(self.file_path, metadata)
            case gui.support.Filetype.WORD:
                errors = backend.docx.save(metadata, self.file_path, self.file_path, self.datatypes)
            case gui.support.Filetype.EXCEL:
                errors = backend.xlsx.save(metadata, self.file_path, self.file_path, self.datatypes)
            case gui.support.Filetype.PPTX:
                errors = backend.pptx.save(metadata, self.file_path, self.file_path, self.datatypes)

        if errors:
            message = "The following metadata could not be saved:\n"
            for error in errors:
                message += "• " + error + "\n"
            QMessageBox.warning(self, "Error", message)

    def about(self):
        text = "" \
            "<h3>About MetEx</h3>" \
            "<p>MetEx is a metadata extraction and edition tool. It works with images, audio files and PDFs, as well as some of the Microsoft Office files.</p>" \
            "<p>Currently supported file types are:</p>" \
            "<ul>" \
            "<li>Images: JPG, JPEG, TIF, TIFF</li>" \
            "<li>Audio: MP3</li>" \
            "<li>PDF</li>" \
            "<li>Microsoft Word: DOCX</li>" \
            "<li>Microsoft Excel: XLSX</li>" \
            "<li>Microsoft PowerPoint: PPTX</li>" \
            "</ul>" \
            "<p>MetEx is free and open source software. It is distributed under the MIT license. For more information, visit <a href=https://github.com/emiliawator/METEX>MetEx GitHub</a>.</p>" \
            "&#8291;"
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
        self.setWindowIcon(QIcon("icons/logo.png"))

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

    def _createWelcomePage(self):
        self.welcomeSite = QWidget()
        self.welcomeSiteLayout = QVBoxLayout()
        self.welcomeSite.setLayout(self.welcomeSiteLayout)
        self.welcomeSite.setFixedHeight(500)

        empty = QLabel()
        empty.setFixedHeight(10)
        self.welcomeSiteLayout.addWidget(empty)

        text1 = QLabel("Welcome to MetEx!")
        text1.setAlignment(Qt.AlignCenter)
        text1.setFixedHeight(120)
        font1 = QFont("Cascadia Code", 40, QFont.Bold)
        text1.setFont(font1)
        self.welcomeSiteLayout.addWidget(text1)
        
        image = QLabel(self)
        pixmap = QPixmap("icons/logo.png")
        pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image.setPixmap(pixmap)
        image.setFixedSize(pixmap.width(), pixmap.height())
        self.welcomeSiteLayout.addWidget(image, alignment=Qt.AlignCenter)
        
        text2 = QLabel("Please open a file to start editing metadata.")
        text2.setAlignment(Qt.AlignCenter)
        text2.setFixedHeight(80)
        font2 = QFont("Cascadia Code", 20)
        text2.setFont(font2)
        self.welcomeSiteLayout.addWidget(text2, alignment=Qt.AlignCenter)

        button = QPushButton("Open file")
        button.clicked.connect(self.open)
        button.setFixedSize(300, 40)
        self.welcomeSiteLayout.addWidget(button, alignment=Qt.AlignCenter)

        self.setCentralWidget(self.welcomeSite)

    def _createTable(self): # filled with test data
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(["Key", "Value"])

        self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #d9e6cf; }")
        self.tableWidget.verticalHeader().setStyleSheet("QHeaderView::section { background-color: #d9e6cf; }")
   
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
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
        elif extension == 'pptx':
            self.file_type = gui.support.Filetype.PPTX
        else:
            self.file_type = gui.support.Filetype.NONE

    def _loadTable(self):
        self._createTable()
        self.setCentralWidget(self.tableWidget)
        match self.file_type:
            case gui.support.Filetype.IMAGE:
                metadata, readonly = backend.images.read(self.file_path)
                self.readonly = readonly
            case gui.support.Filetype.AUDIO:
                metadata = backend.audio.read(self.file_path)
                self.readonly = []
            case gui.support.Filetype.PDF:
                metadata = backend.pdf.read(self.file_path)
                self.readonly = []
            case gui.support.Filetype.WORD:
                metadata, datatypes = backend.docx.read(self.file_path)
                self.readonly = []
                self.datatypes = datatypes
            case gui.support.Filetype.EXCEL:
                metadata = backend.xlsx.read(self.file_path)
                self.readonly = []
                datatypes = None
                self.datatypes = datatypes
            case gui.support.Filetype.PPTX:
                metadata = backend.pptx.read(self.file_path)
                self.readonly = []
                datatypes = None
                self.datatypes = datatypes
            case gui.support.Filetype.NONE:
                self.statusBar.showMessage("File format not supported", 5000)
                return

        self.tableWidget.setRowCount(len(metadata))
        self.tableWidget.setColumnCount(2)

        for i, (key, value) in enumerate(metadata):
            k = QTableWidgetItem(str(key))
            k.setFlags(k.flags() & Qt.ItemIsEditable)
            k.setForeground(Qt.black)
            self.tableWidget.setItem(i, 0, k)

            v = QTableWidgetItem(str(value))
            if key in self.readonly:
                v.setFlags(v.flags() & Qt.ItemIsEditable)
                v.setForeground(Qt.black)
                v.setBackground(QColor(235, 235, 235)) #ebebeb
                k.setBackground(QColor(235, 235, 235)) #ebebeb
            else:
                v.setFlags(v.flags() | Qt.ItemIsEditable)
            self.tableWidget.setItem(i, 1, v)  

        self.statusBar.showMessage("File loaded", 5000)

