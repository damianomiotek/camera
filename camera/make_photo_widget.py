import time
from pathlib import Path

from PyQt6.QtCore import Qt, QKeyCombination
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog, QMessageBox

from camera.other_widgets.screen import Screen
from camera.threads.make_photo import MakePhoto


class MakePhotoWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.base_layout = QVBoxLayout()
        self.display_width = 1170
        self.display_height = 860

        # Create thread to read camera and take photos
        self.make_photo = MakePhoto()
        self.make_photo.update_image.connect(self.update_image)

        # Create a space keyboard shortcut for taking photos
        key_sequence = QKeySequence(QKeyCombination(Qt.Key.Key_Space))
        self.shortcut = QShortcut(key_sequence, self)
        self.shortcut.activated.connect(self.take_photo_clicked)
        self.shortcut.setEnabled(False)

        # create the label that holds the image
        self.screen = Screen(self.display_width, self.display_height)
        self.start = QPushButton("Start")
        self.start.clicked.connect(self.start_clicked)
        self.stop = QPushButton("Stop")
        self.stop.clicked.connect(self.turn_off)
        self.take_photo = QPushButton("Zrób zdjęcie")
        self.take_photo.clicked.connect(self.take_photo_clicked)
        self.edit_widgets()

        self.control_panel = QHBoxLayout()
        self.edit_layouts()
        self.setLayout(self.base_layout)

    def edit_widgets(self):
        self.start.setStyleSheet("font-size : 11pt")
        self.start.setMaximumSize(120, 40)

        self.stop.setStyleSheet("font-size : 11pt")
        self.stop.setMaximumSize(120, 40)
        self.stop.setEnabled(False)

        self.take_photo.setStyleSheet("font-size : 11pt")
        self.take_photo.setMaximumSize(120, 40)
        self.take_photo.setEnabled(False)

    def edit_layouts(self):
        self.control_panel.addWidget(self.start)
        self.control_panel.addWidget(self.stop)
        self.control_panel.addWidget(self.take_photo)

        self.base_layout.addSpacing(5)
        self.base_layout.addWidget(self.screen, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.base_layout.addLayout(self.control_panel)
        self.base_layout.addSpacing(15)

    def start_clicked(self):
        self.start.setEnabled(False)
        self.stop.setEnabled(True)
        self.take_photo.setEnabled(True)
        self.shortcut.setEnabled(True)
        # start the thread
        self.make_photo.start()

    def update_image(self, qt_img):
        """Updates the screen label with a new image"""
        scaled_img = qt_img.scaled(self.display_width, self.display_height)
        self.screen.set_frame(scaled_img)

    def turn_off(self):
        self.make_photo.stop()
        self.make_photo.quit()
        time.sleep(1)

        self.screen.set_black_background()
        self.start.setEnabled(True)
        self.stop.setEnabled(False)
        self.take_photo.setEnabled(False)
        self.shortcut.setEnabled(False)

    def take_photo_clicked(self):
        success, photo = self.make_photo.take_photo()
        if success:
            QMessageBox.information(self, "Zdjęcie", "Zdjęcie zostało zrobione. Klinknij OK a następnie wybierz"
                                                     " nazwę i gdzie zapisać zdjęcie.",
                                    buttons=QMessageBox.StandardButton.Ok)
        file_filter = "Zdjęcia (*.jpg *.png *.bmp *.svg);; Wszystkie pliki (*.*)"
        selected_filename = QFileDialog.getSaveFileName(caption="Wybierz miejsce zapisu i nazwę pliku",
                                                    directory=str(Path.home()),
                                                    options=QFileDialog.Option.DontResolveSymlinks.DontResolveSymlinks,
                                                    filter=file_filter)
        photo.save(selected_filename[0])
