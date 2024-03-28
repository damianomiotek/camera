from pathlib import Path

import cv2
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage

from camera.utilities import get_directory_separator


class MakePhoto(QThread):
    update_image = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()

        self.cap = None

    def run(self):
        # capture from computer camera
        self.cap = cv2.VideoCapture(0)
        ret = True

        while ret:
            ret, cv_img = self.cap.read()
            if ret:
                qt_img = self.convert_cv_qt(cv_img)
                self.update_image.emit(qt_img)

    def take_photo(self):
        ret, cv_img = self.cap.read()
        resized_cv_img = cv2.resize(cv_img, (1360, 1020))
        return ret, self.convert_cv_qt(resized_cv_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QImage"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        return qt_img

    def stop(self):
        self.cap.release()
        cv2.destroyAllWindows()
