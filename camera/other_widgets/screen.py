from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtWidgets import QLabel


class Screen(QLabel):
    def __init__(self, display_width, display_height):
        super().__init__()

        self.width = display_width
        self.height = display_height
        self.resize(self.width, self.height)
        self.black_background = QPixmap(self.width, self.height)
        self.black_background.fill(QColor('black'))
        # set the screen to the black pixmap
        super().setPixmap(self.black_background)

    def set_frame(self, img):
        super().setPixmap(QPixmap.fromImage(img))

    def set_black_background(self):
        super().setPixmap(self.black_background)

    def display_photo(self, photo_path):
        photo_from_disk = QPixmap(photo_path)
        photo_from_disk = photo_from_disk.scaled(self.width, self.height)
        super().setPixmap(photo_from_disk)
