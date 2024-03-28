from PyQt6.QtCore import Qt, QUrl, QSize, QSizeF
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt6.QtWidgets import QWidget, QPushButton, QStyle, QSlider, QStatusBar, QVBoxLayout, QHBoxLayout, QFileDialog, \
    QGraphicsScene, QGraphicsView


class VideoPlayerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.media_player = QMediaPlayer()
        self.display_width = 1170
        self.display_height = 860

        screen = QGraphicsVideoItem()
        screen.setSize(QSizeF(self.display_width, self.display_height))
        scene = QGraphicsScene(self)
        graphicsView = QGraphicsView(scene)
        scene.addItem(screen)

        open_button = QPushButton("Otwórz plik video")
        open_button.setToolTip("Otwórz plik video")
        open_button.setStatusTip("Otwórz plik video")
        open_button.setStyleSheet("font-size : 11pt")
        open_button.setMaximumSize(140, 30)
        open_button.setIconSize(QSize(20, 20))
        open_button.setIcon(QIcon.fromTheme("document-open", QIcon("open.png")))
        open_button.clicked.connect(self.select_movie)

        self.play_button = QPushButton()
        self.play_button.setEnabled(False)
        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.play_button.clicked.connect(self.play)

        self.position_slider = QSlider(Qt.Orientation.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.set_position)

        self.statusBar = QStatusBar()
        self.statusBar.setFont(QFont("Noto Sans", 7))
        self.statusBar.setFixedHeight(15)

        control_panel = QHBoxLayout()
        control_panel.setContentsMargins(0, 0, 0, 0)
        control_panel.addWidget(open_button)
        control_panel.addWidget(self.play_button)
        control_panel.addWidget(self.position_slider)

        base_layout = QVBoxLayout()
        base_layout.addSpacing(4)
        base_layout.addWidget(graphicsView, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        base_layout.addLayout(control_panel)
        base_layout.addWidget(self.statusBar)
        base_layout.addSpacing(8)

        self.setLayout(base_layout)

        self.media_player.setVideoOutput(screen)
        self.media_player.playbackStateChanged.connect(self.media_state_changed)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.errorChanged.connect(self.handle_error)

    def select_movie(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Wybierz plik video do odtwarzania",
                                                  ".", "Pliki video (*.mp4 *.flv *.ts *.mts *.avi)")

        if file_name != '':
            self.media_player.setSource(QUrl.fromLocalFile(file_name))
            self.play_button.setEnabled(True)
            self.statusBar.showMessage(file_name)
            self.play()

    def play(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def media_state_changed(self, state):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        else:
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

    def position_changed(self, position):
        self.position_slider.setValue(position)

    def duration_changed(self, duration):
        self.position_slider.setRange(0, duration)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def handle_error(self):
        self.play_button.setEnabled(False)
        self.statusBar.showMessage("Error: " + self.media_player.errorString())
