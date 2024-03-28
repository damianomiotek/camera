from PyQt6.QtWidgets import QMainWindow
from camera.tabs import Tabs


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tabs = Tabs()
        self.setCentralWidget(self.tabs)

        self.setMinimumSize(1350, 1000)
        self.setWindowTitle("Kamera")
