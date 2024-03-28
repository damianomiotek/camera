import os
from pathlib import Path

from PyQt6.QtCore import Qt, QKeyCombination
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QFileDialog

from camera.other_widgets.screen import Screen
from camera.utilities import image_formats, get_directory_separator


class PhotoWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.base_layout = QVBoxLayout()
        self.display_width = 1170
        self.display_height = 860
        self.all_photos_in_dir = []
        self.current_index_in_table_with_photos = 0

        self.screen = Screen(self.display_width, self.display_height)
        self.choose_photo = QPushButton("Wybierz zdjęcie")
        self.choose_photo.clicked.connect(self.choose_photo_clicked)
        self.next_photo = QPushButton("Następne")
        self.next_photo.clicked.connect(self.next_photo_clicked)
        self.previous_photo = QPushButton("Poprzednie")
        self.previous_photo.clicked.connect(self.previous_photo_clicked)
        self.edit_widgets()

        key_sequence = QKeySequence(QKeyCombination(Qt.Key.Key_Left))
        self.left_key_shortcut = QShortcut(key_sequence, self)
        self.left_key_shortcut.activated.connect(self.previous_photo_clicked)
        self.left_key_shortcut.setEnabled(False)
        key_sequence = QKeySequence(QKeyCombination(Qt.Key.Key_Right))
        self.right_key_shortcut = QShortcut(key_sequence, self)
        self.right_key_shortcut.activated.connect(self.next_photo_clicked)
        self.right_key_shortcut.setEnabled(False)

        self.control_panel = QHBoxLayout()
        self.edit_layouts()
        self.setLayout(self.base_layout)

    def edit_widgets(self):
        self.choose_photo.setStyleSheet("font-size : 11pt")
        self.choose_photo.setMaximumSize(230, 40)

        self.previous_photo.setStyleSheet("font-size : 11pt")
        self.previous_photo.setMaximumSize(120, 40)
        self.previous_photo.setEnabled(False)

        self.next_photo.setStyleSheet("font-size : 11pt")
        self.next_photo.setMaximumSize(120, 40)
        self.next_photo.setEnabled(False)

    def edit_layouts(self):
        self.control_panel.addWidget(self.choose_photo)
        self.control_panel.addWidget(self.previous_photo)
        self.control_panel.addWidget(self.next_photo)

        self.base_layout.addSpacing(5)
        self.base_layout.addWidget(self.screen, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.base_layout.addLayout(self.control_panel)
        self.base_layout.addSpacing(15)

    def get_all_photos_in_dir(self, dir):
        files = os.listdir(dir)
        photos = []

        for file in files:
            if file.endswith(tuple(image_formats)):
                photos.append(f"{dir}{get_directory_separator()}{file}")

        return photos

    def set_up_index_in_table_with_photos(self, photo_path):
        photo_path = photo_path.replace("/", "\\")
        for i in range(len(self.all_photos_in_dir)):
            if self.all_photos_in_dir[i] == photo_path:
                self.current_index_in_table_with_photos = i

    def choose_photo_clicked(self):
        file_filter = "Zdjęcia (*.jpg *.png *.bmp *.svg);; Wszystkie pliki (*.*)"
        photo_path, _ = QFileDialog.getOpenFileName(caption="Wybierz miejsce zapisu i nazwę pliku",
                                                    directory=str(Path.home()),
                                                    options=QFileDialog.Option.DontResolveSymlinks.DontResolveSymlinks,
                                                    filter=file_filter)

        if photo_path != "":
            self.screen.display_photo(photo_path)
            dir_path = photo_path[: photo_path.rfind("/")]
            self.all_photos_in_dir = self.get_all_photos_in_dir(dir_path)
            self.set_up_index_in_table_with_photos(photo_path)
            self.previous_photo.setEnabled(True)
            self.left_key_shortcut.setEnabled(True)
            self.next_photo.setEnabled(True)
            self.right_key_shortcut.setEnabled(True)

    def next_photo_clicked(self):
        if self.current_index_in_table_with_photos + 1 < len(self.all_photos_in_dir):
            self.current_index_in_table_with_photos += 1
            img_to_display = self.all_photos_in_dir[self.current_index_in_table_with_photos]
            self.screen.display_photo(img_to_display)
            if self.current_index_in_table_with_photos == len(self.all_photos_in_dir) - 1:
                self.next_photo.setEnabled(False)
                self.right_key_shortcut.setEnabled(False)
            elif self.current_index_in_table_with_photos == 1:
                self.previous_photo.setEnabled(True)
                self.left_key_shortcut.setEnabled(True)

    def previous_photo_clicked(self):
        if self.current_index_in_table_with_photos > 0:
            self.current_index_in_table_with_photos -= 1
            img_to_display = self.all_photos_in_dir[self.current_index_in_table_with_photos]
            self.screen.display_photo(img_to_display)
            if self.current_index_in_table_with_photos == 0:
                self.previous_photo.setEnabled(False)
                self.left_key_shortcut.setEnabled(False)
            elif self.current_index_in_table_with_photos == len(self.all_photos_in_dir) - 2:
                self.next_photo.setEnabled(True)
                self.right_key_shortcut.setEnabled(True)

