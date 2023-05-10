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


readonly = [] # read-only metadata keys for current file
metadata = []
original_file_metadata = []

class MainWindow(QMainWindow):
    
    file_type = gui.support.Filetype.NONE
    file_path = None
    mode = "light"

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("MetEx")
        self.resize(800, 600)

        self._createActions()
        self._createMenuBar()
        self._createWelcomePage()
        self._createStatusBar()
        self.statusBar.hide()

    # opens file dialog and loads file
    def open(self):
        self.file_path = QFileDialog.getOpenFileName(self, "Open")[0]
        if not self.file_path:
            return
        self._checkFileType()
        self._loadTable()
        self.original_file_metadata = self.metadata

    # saves metadata from self.tableWidget to self.metadata
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
                errors = backend.docx.save(metadata, self.file_path, self.file_path)
            case gui.support.Filetype.EXCEL:
                errors = backend.xlsx.save(metadata, self.file_path, self.file_path)
            case gui.support.Filetype.PPTX:
                errors = backend.pptx.save(metadata, self.file_path, self.file_path)
        if errors:
            message = "The following metadata could not be saved.\n"
            for error in errors:
                message += "• " + error + "\n"
            QMessageBox.warning(self, "Error", message)
        self.metadata = metadata

    # loads metadata from self.metadata to self.tableWidget
    def load_metadata(self):
        for i, (key, value) in enumerate(self.metadata):
            k = QTableWidgetItem(str(key))
            v = QTableWidgetItem(str(value))
            self.tableWidget.setItem(i, 0, k)
            self.tableWidget.setItem(i, 1, v)  
            if key in self.readonly:
                if self.mode == "light":
                    v.setForeground(Qt.black)
                    k.setForeground(Qt.black)
                    v.setBackground(QColor(235, 235, 235))
                    k.setBackground(QColor(235, 235, 235))
                elif self.mode == "dark":
                    v.setForeground(Qt.white)
                    k.setForeground(Qt.white)
                    v.setBackground(QColor(66, 66, 66))
                    k.setBackground(QColor(66, 66, 66))

    # discards changes made to metadata
    def discard(self):
        self.metadata = self.original_file_metadata
        self.load_metadata()
        self.load_mode()
        self.statusBar.showMessage("Changes discarded", 5000)

    # erases all metadata from file
    def erase(self):
        for i, (key, value) in enumerate(self.metadata):
            k = QTableWidgetItem(str(key))
            v = QTableWidgetItem("")
            self.tableWidget.setItem(i, 0, k)
            self.tableWidget.setItem(i, 1, v)  
            if key in self.readonly:
                if self.mode == "light":
                    v.setForeground(Qt.black)
                    k.setForeground(Qt.black)
                    v.setBackground(QColor(235, 235, 235))
                    k.setBackground(QColor(235, 235, 235))
                elif self.mode == "dark":
                    v.setForeground(Qt.white)
                    k.setForeground(Qt.white)
                    v.setBackground(QColor(66, 66, 66))
                    k.setBackground(QColor(66, 66, 66))
        self.statusBar.showMessage("Metadata erased", 5000)

    # changes mode between light and dark
    def change_mode(self):
        if self.mode == "light":
            self.mode = "dark"
        elif self.mode == "dark":
            self.mode = "light"
        self.load_mode()

    # loads color scheme
    def load_mode(self):
        if self.mode == "dark":
            self.setStyleSheet("background-color: #424242; color: #ffffff;")
            self.statusBar.setStyleSheet("background-color: #424242; color: #ffffff;")
            if self.centralWidget() == self.welcomeSite:
                self.welcomeSite.setStyleSheet("background-color: #424242; color: #ffffff;")
                self.welcomeSite.layout().itemAt(4).widget().setStyleSheet("background-color: #ffffff; color: #000000;")
            elif self.centralWidget() == self.tableWidget:
                self.tableWidget.setStyleSheet("background-color: #424242; color: #ffffff;")
                self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #262626; }")
                self.tableWidget.verticalHeader().setStyleSheet("QHeaderView::section { background-color: #262626; }")
                # readonly cells style
                for i, (key, value) in enumerate(self.metadata):
                    k = QTableWidgetItem(str(key))
                    v = QTableWidgetItem(str(value))
                    self.tableWidget.setItem(i, 0, k)
                    self.tableWidget.setItem(i, 1, v)  
                    if key in self.readonly:
                        v.setForeground(Qt.white)
                        k.setForeground(Qt.white)
                        v.setBackground(QColor(38, 38, 38))
                        k.setBackground(QColor(38, 38, 38))
            self.mode = "dark"

        elif self.mode == "light":
            self.setStyleSheet("background-color: #f0f0f0; color: #000000;")
            self.statusBar.setStyleSheet("background-color: #ffffff; color: #000000;")
            if self.centralWidget() == self.welcomeSite:
                self.welcomeSite.setStyleSheet("background-color: #f0f0f0; color: #000000;")
                self.welcomeSite.layout().itemAt(4).widget().setStyleSheet("background-color: #e1e1e1; color: #000000;")
            elif self.centralWidget() == self.tableWidget:
                self.tableWidget.setStyleSheet("background-color: #ffffff; color: #000000;")
                self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #d9e6cf; }")
                self.tableWidget.verticalHeader().setStyleSheet("QHeaderView::section { background-color: #d9e6cf; }")
                # readonly cells style
                for i, (key, value) in enumerate(self.metadata):
                    k = QTableWidgetItem(str(key))
                    v = QTableWidgetItem(str(value))
                    self.tableWidget.setItem(i, 0, k)
                    self.tableWidget.setItem(i, 1, v)  
                    if key in self.readonly:
                        v.setForeground(Qt.black)
                        k.setForeground(Qt.black)
                        v.setBackground(QColor(235, 235, 235))
                        k.setBackground(QColor(235, 235, 235))
            self.mode = "light"

    # shows about dialog
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
        self.discardButton.clicked.connect(self.discard)
        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.save)
        self.exitButton = QPushButton("Exit")
        self.exitButton.clicked.connect(self.close)

        self.statusBar.addAction(self.exitAction)
        self.statusBar.addPermanentWidget(self.saveButton)
        self.statusBar.addPermanentWidget(self.discardButton)
        self.statusBar.addPermanentWidget(self.exitButton)

    def _createMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.discardAction)
        fileMenu.addAction(self.eraseAction)
        fileMenu.addAction(self.exitAction)
        optionsMenu = menuBar.addMenu("&View")
        optionsMenu.addAction(self.modeAction)
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
        self.discardAction = QAction("&Discard", self)
        self.discardAction.setShortcut("Ctrl+D")
        self.discardAction.triggered.connect(self.discard)

        self.eraseAction = QAction("&Erase metadata", self)
        self.eraseAction.setShortcut("Ctrl+E")
        self.eraseAction.triggered.connect(self.erase)

        self.exitAction = QAction("&Exit", self)
        self.exitAction.setShortcut("Ctrl+Q")
        self.exitAction.triggered.connect(self.close)

        self.modeAction = QAction("&Change mode", self)
        self.modeAction.setShortcut("Ctrl+M")
        self.modeAction.triggered.connect(self.change_mode)

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

        openButton = QPushButton("Open file")
        openButton.clicked.connect(self.open)
        openButton.setFixedSize(300, 40)
        self.welcomeSiteLayout.addWidget(openButton, alignment=Qt.AlignCenter)

        self.setCentralWidget(self.welcomeSite)

    def _createTable(self):
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
        self.statusBar.show()

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
                metadata = backend.docx.read(self.file_path)
                self.readonly = []
            case gui.support.Filetype.EXCEL:
                metadata = backend.xlsx.read(self.file_path)
                self.readonly = []
            case gui.support.Filetype.PPTX:
                metadata = backend.pptx.read(self.file_path)
                self.readonly = []
            case gui.support.Filetype.NONE:
                self.statusBar.showMessage("File format not supported", 5000)
                return

        self.tableWidget.setRowCount(len(metadata))
        self.tableWidget.setColumnCount(2)

        for i, (key, value) in enumerate(metadata):
            k = QTableWidgetItem(str(key))
            k.setFlags(k.flags() & Qt.ItemIsEditable)
            self.tableWidget.setItem(i, 0, k)

            v = QTableWidgetItem(str(value))
            if key in self.readonly:
                v.setFlags(v.flags() & Qt.ItemIsEditable)
                if self.mode == "light":
                    v.setForeground(Qt.black)
                    k.setForeground(Qt.black)
                    v.setBackground(QColor(235, 235, 235)) #ebebeb
                    k.setBackground(QColor(235, 235, 235)) #ebebeb
                elif self.mode == "dark":
                    v.setForeground(Qt.white)
                    k.setForeground(Qt.white)
                    v.setBackground(QColor(66, 66, 66))
                    k.setBackground(QColor(66, 66, 66))
            else:
                v.setFlags(v.flags() | Qt.ItemIsEditable)
            self.tableWidget.setItem(i, 1, v)  

        self.metadata = metadata
        self.load_mode()
        self.statusBar.showMessage("File loaded", 5000)

