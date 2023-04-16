from PyQt5.QtWidgets import * 


class MainWindow(QMainWindow):
    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("MetEx")
        self.resize(800, 600)

        self._createActions()
        self._createMenuBar()
        self._createTable()
        self._createStatusBar()

    def open(self):
        global file_path
        path = QFileDialog.getOpenFileName(self, "Open")[0]
        self._loadTable(path)

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
        self.saveAction = QAction("&Save As", self)
        self.saveAction.setShortcut("Ctrl+S")
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
    
    def _loadTable(self, path):
        extension = path.split(".")[-1]
        if extension in ['jpg', 'jpeg', 'png', 'tiff', 'tif']:
            from backend.images import read
            metadata = read(path)
        elif extension == 'pdf':
            from backend.pdf import read
            metadata = read(path)
        elif extension == 'mp3':
            from backend.audio import read
            metadata = read(path)
        else:
            self.statusBar.showMessage("File format not supported", 5000)
            return

        metadata = [(key, str(value)) for key, value in metadata.items()]

        self.tableWidget.setRowCount(len(metadata))
        self.tableWidget.setColumnCount(2)
        for i, (key, value) in enumerate(metadata):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(key))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(value))

        self.statusBar.showMessage("File loaded", 5000)

