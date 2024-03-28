from PyQt6.QtWidgets import QTabWidget

from camera.camera_widget import CameraWidget
from camera.make_photo_widget import MakePhotoWidget
from camera.photo_widget import PhotoWidget
from camera.smart_video_player_widget import SmartVideoPlayerWidget
from camera.smart_youtube_player_widget import SmartYoutubePlayerWidget
from camera.video_player_widget import VideoPlayerWidget


class Tabs(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setTabPosition(QTabWidget.TabPosition.North)
        self.setMovable(False)
        self.setStyleSheet("font-size: 12pt")

        self.camera_widget = CameraWidget()
        self.make_photo_widget = MakePhotoWidget()
        self.smart_video_player_widget = SmartVideoPlayerWidget()
        self.smart_youtube_player_widget = SmartYoutubePlayerWidget()
        self.video_player_widget = VideoPlayerWidget()
        self.photo_widget = PhotoWidget()

        self.addTab(self.camera_widget, "Kamera")
        self.addTab(self.smart_video_player_widget, "Inteligentne odtwarzanie video")
        self.addTab(self.smart_youtube_player_widget, "Odtwarzanie video z Youtube")
        self.addTab(self.make_photo_widget, "Aparat")
        self.addTab(self.video_player_widget, "Standardowe odtwarzanie video")
        self.addTab(self.photo_widget, "Zdjęcia")

        self.currentChanged.connect(self.tab_was_changed)

    def tab_was_changed(self):
        if self.camera_widget.camera_which_detects_people.isRunning():
            self.camera_widget.turn_off()
        if self.smart_video_player_widget.smart_video_player.isRunning():
            self.smart_video_player_widget.turn_off()
        if self.smart_youtube_player_widget.smart_youtube_player.isRunning():
            self.smart_youtube_player_widget.turn_off()
        if self.make_photo_widget.make_photo.isRunning():
            self.make_photo_widget.turn_off()
