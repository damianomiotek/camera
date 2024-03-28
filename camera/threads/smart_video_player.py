import time

from ultralytics import YOLO
import cv2
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage


class SmartVideoPlayer(QThread):
    update_image = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()

        self.file = None
        self.cap = None
        self.model = None
        self.hold_flag = False

        self.class_names = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                            "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat","dog",
                            "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                            "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
                            "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle",
                            "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich",
                            "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa",
                            "pottedplant", "bed", "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote",
                            "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book",
                            "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]
        self.classes_to_detect = [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                                  26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 41, 42, 43, 45, 46, 47, 48,
                                  49, 52, 53, 55, 56, 63, 64, 66, 67, 69, 72, 73, 74]

    def run(self):
        self.model = YOLO("yolo-Weights/yolov8n.pt")
        # capture from file on hard disk
        self.cap = cv2.VideoCapture(self.file)
        ret = True

        while ret:
            ret, cv_img = self.cap.read()
            if ret:
                results = self.model.predict(cv_img, stream=True, classes=self.classes_to_detect, imgsz=(160,256),
                                             vid_stride=5, max_det=13)

                # coordinates
                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        # bounding box
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values

                        # put box in cam
                        cv2.rectangle(cv_img, (x1, y1), (x2, y2), (255, 0, 0), 3)

                        # class name
                        cls = int(box.cls[0])
                        # object details
                        org = [x1, y1]
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        font_scale = 1
                        color = (0, 255, 0)
                        thickness = 2

                        cv2.putText(cv_img, self.class_names[cls], org, font, font_scale, color, thickness)
                qt_img = self.convert_cv_qt(cv_img)
                self.update_image.emit(qt_img)

            while self.hold_flag:
                time.sleep(0.5)


    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QImage"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        return qt_img

    def hold(self):
        self.hold_flag = True

    def play_continue(self):
        self.hold_flag = False

    def stop(self):
        self.hold_flag = False
        self.cap.release()
        cv2.destroyAllWindows()
