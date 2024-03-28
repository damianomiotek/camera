from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog

from camera.other_widgets.screen import Screen
from camera.threads.smart_video_player import SmartVideoPlayer
from camera.utilities import video_formats


class SmartVideoPlayerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.base_layout = QVBoxLayout()
        self.display_width = 1170
        self.display_height = 860

        # Create thread for reading and analyzing video
        self.smart_video_player = SmartVideoPlayer()
        self.smart_video_player.update_image.connect(self.update_image)
        self.smart_video_player.finished.connect(self.video_finished)

        # create the label that holds the image
        self.screen = Screen(self.display_width, self.display_height)
        self.choose_video_file = QPushButton("Wybierz plik video")
        self.choose_video_file.clicked.connect(self.choose_video_file_clicked)
        self.play = QPushButton("Odtwórz")
        self.play.clicked.connect(self.play_clicked)
        self.hold = QPushButton("Wstrzymaj")
        self.hold.clicked.connect(self.hold_clicked)
        self.edit_widgets()

        self.control_panel = QHBoxLayout()
        self.edit_layouts()
        self.setLayout(self.base_layout)

    def edit_widgets(self):
        self.choose_video_file.setStyleSheet("font-size : 11pt")
        self.choose_video_file.setMaximumSize(230, 40)

        self.play.setStyleSheet("font-size : 11pt")
        self.play.setMaximumSize(120, 40)
        self.play.setEnabled(False)

        self.hold.setStyleSheet("font-size : 11pt")
        self.hold.setMaximumSize(120, 40)
        self.hold.setEnabled(False)

    def edit_layouts(self):
        self.control_panel.addWidget(self.choose_video_file)
        self.control_panel.addWidget(self.play)
        self.control_panel.addWidget(self.hold)

        self.base_layout.addSpacing(5)
        self.base_layout.addWidget(self.screen, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.base_layout.addLayout(self.control_panel)
        self.base_layout.addSpacing(15)

    def play_clicked(self):
        self.play.setEnabled(False)
        self.hold.setEnabled(True)
        self.choose_video_file.setEnabled(False)
        # start the thread
        if self.smart_video_player.isRunning():
            self.smart_video_player.play_continue()
        else:
            self.smart_video_player.start()

    def update_image(self, qt_img):
        """Updates the screen label with a new image"""
        scaled_img = qt_img.scaled(self.display_width, self.display_height)
        self.screen.set_frame(scaled_img)

    def hold_clicked(self):
        self.play.setEnabled(True)
        self.hold.setEnabled(False)
        self.choose_video_file.setEnabled(True)
        self.smart_video_player.hold()

    def choose_video_file_clicked(self):
        file_filter = 'Pliki video (*.mp4 *.mov *.wmv *.avi *.webm *.avchd *.swf);; Wszystkie pliki (*.*)'
        file_name = QFileDialog.getOpenFileName(
            caption='Wybierz plik video',
            directory=str(Path.home()),
            filter=file_filter
        )
        if file_name[0] != "" and any([file_name[0].endswith(video_format) for video_format in video_formats]):
            if self.smart_video_player.isRunning():
                self.smart_video_player.stop()
                self.smart_video_player.quit()
                self.screen.set_black_background()
            self.smart_video_player.file = file_name[0]
            self.play.setEnabled(True)
            self.hold.setEnabled(False)

    def video_finished(self):
        self.play.setEnabled(True)
        self.hold.setEnabled(False)
        self.choose_video_file.setEnabled(True)
        self.screen.set_black_background()

    def turn_off(self):
        self.play.setEnabled(True)
        self.hold.setEnabled(False)
        self.choose_video_file.setEnabled(True)
        self.smart_video_player.stop()
        self.smart_video_player.quit()
        self.screen.set_black_background()

