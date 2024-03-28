import time

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QMessageBox

from camera.other_widgets.screen import Screen
from camera.threads.smart_youtube_player import SmartYoutubePlayer
from camera.utilities import check_url_is_valid


class SmartYoutubePlayerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.started = False

        self.base_layout = QVBoxLayout()
        self.display_width = 1170
        self.display_height = 860

        self.smart_youtube_player = SmartYoutubePlayer()
        self.smart_youtube_player.update_image.connect(self.update_image)
        self.smart_youtube_player.finished.connect(self.video_finished)
        self.smart_youtube_player.started.connect(self.video_started)

        # create the label that holds the image
        self.screen = Screen(self.display_width, self.display_height)
        self.youtube_url = QLineEdit("Wpisz url filmu z Youtube")
        self.play_or_hold = QPushButton("Odtwórz")
        self.play_or_hold.clicked.connect(self.play_or_hold_clicked)
        self.edit_widgets()

        self.control_panel = QHBoxLayout()
        self.edit_layouts()
        self.setLayout(self.base_layout)

    def edit_widgets(self):
        self.youtube_url.setStyleSheet("font-size : 11pt")
        self.youtube_url.setMaximumSize(900, 40)

        self.play_or_hold.setStyleSheet("font-size : 11pt")
        self.play_or_hold.setMaximumSize(120, 40)

    def edit_layouts(self):
        self.control_panel.addWidget(self.youtube_url)
        self.control_panel.addWidget(self.play_or_hold)

        self.base_layout.addSpacing(5)
        self.base_layout.addWidget(self.screen, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.base_layout.addLayout(self.control_panel)
        self.base_layout.addSpacing(15)

    def play_or_hold_clicked(self):
        if self.started:
            self.smart_youtube_player.hold()
            self.play_or_hold.setText("Odtwórz")
            self.started = False
        else:
            youtube_url = self.youtube_url.text()
            if youtube_url != self.smart_youtube_player.url:
                if not youtube_url:
                    if self.smart_youtube_player.isRunning():
                        self.smart_youtube_player.play_continue()
                    else:
                        QMessageBox.information(self, "Brak URL", "Musisz podać adres URL do filmu na Youtube",
                                                buttons=QMessageBox.StandardButton.Ok)
                        return
                elif check_url_is_valid(youtube_url) is False:
                    QMessageBox.information(self, "Zły URL", "Zły adres do filmu na Youtube",
                                            buttons=QMessageBox.StandardButton.Ok)
                    return
                else:
                    if self.smart_youtube_player.isRunning():
                        self.smart_youtube_player.stop()
                        self.smart_youtube_player.quit()
                        self.screen.set_black_background()
                        time.sleep(1)
                    self.smart_youtube_player.url = youtube_url
                    self.smart_youtube_player.start()
            elif self.smart_youtube_player.isRunning():
                self.smart_youtube_player.play_continue()
            else:
                self.smart_youtube_player.start()

            self.play_or_hold.setText("Wstrzymaj")
            self.started = True

    def update_image(self, qt_img):
        """Updates the screen label with a new image"""
        scaled_img = qt_img.scaled(self.display_width, self.display_height)
        self.screen.set_frame(scaled_img)

    def video_finished(self):
        self.screen.set_black_background()
        self.play_or_hold.setText("Odtwórz")
        self.started = False

    def video_started(self):
        self.play_or_hold.setText("Wstrzymaj")
        self.started = True

    def turn_off(self):
        self.smart_youtube_player.stop()
        self.smart_youtube_player.quit()
        self.screen.set_black_background()
        self.youtube_url.setText("Wpisz url filmu z Youtube")
        self.play_or_hold.setText("Odtwórz")
        self.started = False
