from pathlib import Path
import time
from datetime import datetime

import cv2
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage

from camera.utilities import get_directory_separator


class CameraWhichDetectsPeople(QThread):
    update_image = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()

        self.cap = None
        self.out = None

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        self.detection = False
        self.detection_stopped_time = None
        self.timer_started = False
        self.seconds_to_record_after_detection = 3

        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.out_frame_size = None
        self.frame_size_for_processing = (384, 288)

        self.directory_with_recordings = f"{Path.home()}{get_directory_separator()}"

    def run(self):
        # capture from web cam
        self.cap = cv2.VideoCapture(0)
        self.out_frame_size = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                               int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.detection = False

        while self.cap.isOpened():
            ret, cv_img = self.cap.read()
            if ret:
                # Reduce size of image to have fewer computations while detection and classification
                # The smaller image is, the faster it will be to process
                cv_img = cv2.resize(cv_img, self.frame_size_for_processing)
                gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4)
                bodies, _ = self.hog.detectMultiScale(cv_img, winStride=(8, 8), scale=1.05, padding=(8, 8))

                for (x, y, width, height) in faces:
                    cv2.rectangle(cv_img, (x, y), (x + width, y + height), (255, 0, 0), 3)
                for (x, y, width, height) in bodies:
                    cv2.rectangle(cv_img, (x, y), (x + width, y + height), (0, 255, 0), 3)
                cv_img = cv2.resize(cv_img, self.out_frame_size)
                qt_img = self.convert_cv_qt(cv_img)
                self.update_image.emit(qt_img)

                if len(faces) + len(bodies) > 0:
                    if self.detection:
                        self.timer_started = False
                    else:
                        self.detection = True
                        current_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
                        self.out = cv2.VideoWriter(
                            f"{self.directory_with_recordings}{current_time}.mp4", self.fourcc, 13, self.out_frame_size)
                elif self.detection:
                    if self.timer_started:
                        if time.time() - self.detection_stopped_time >= self.seconds_to_record_after_detection:
                            self.detection = False
                            self.timer_started = False
                            self.out.release()
                    else:
                        self.timer_started = True
                        self.detection_stopped_time = time.time()

                if self.detection:
                    # Resize image to be readable by computer
                    self.out.write(cv_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QImage"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        return qt_img

    def stop(self):
        """Shut down capture system"""
        # self.detection = False
        self.cap.release()
        if self.out is not None:
            self.out.release()
        cv2.destroyAllWindows()
