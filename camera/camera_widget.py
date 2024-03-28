import time
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog

from camera.other_widgets.screen import Screen
from camera.threads.camera_which_detects_people import CameraWhichDetectsPeople


class CameraWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.base_layout = QVBoxLayout()
        self.display_width = 1170
        self.display_height = 860
        # create the camera capture thread which also detects people
        self.camera_which_detects_people = CameraWhichDetectsPeople()
        self.camera_which_detects_people.update_image.connect(self.update_image)

        # create the label that holds the image
        self.screen = Screen(self.display_width, self.display_height)
        self.start = QPushButton("Start")
        self.start.clicked.connect(self.start_clicked)
        self.stop = QPushButton("Stop")
        self.stop.clicked.connect(self.turn_off)
        self.change_directory_with_recordings = QPushButton("Zmień miejsce zapisywania nagrań")
        self.change_directory_with_recordings.clicked.connect(self.change_directory_with_recordings_clicked)
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

        self.change_directory_with_recordings.setStyleSheet("font-size : 11pt")
        self.change_directory_with_recordings.setMaximumSize(260, 40)

    def edit_layouts(self):
        self.control_panel.addWidget(self.start)
        self.control_panel.addWidget(self.stop)
        self.control_panel.addWidget(self.change_directory_with_recordings)

        self.base_layout.addSpacing(5)
        self.base_layout.addWidget(self.screen, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.base_layout.addLayout(self.control_panel)
        self.base_layout.addSpacing(15)

    def start_clicked(self):
        self.start.setEnabled(False)
        self.stop.setEnabled(True)
        # start the thread
        self.camera_which_detects_people.start()

    def update_image(self, qt_img):
        """Updates the screen label with a new image"""
        scaled_img = qt_img.scaled(self.display_width, self.display_height)
        self.screen.set_frame(scaled_img)

    def turn_off(self):
        self.start.setEnabled(True)
        self.stop.setEnabled(False)

        self.camera_which_detects_people.stop()
        time.sleep(1)
        self.camera_which_detects_people.quit()


    def change_directory_with_recordings_clicked(self):
        selected_dir = QFileDialog.getExistingDirectory(caption="Wybierz katalog gdzie zapisywać nagrania",
                                                        directory=str(Path.home()),
                                                        options=QFileDialog.Option.DontResolveSymlinks)
        if len(selected_dir) > 0:
            selected_dir += "/"
            self.camera_which_detects_people.directory_with_recordings = selected_dir
