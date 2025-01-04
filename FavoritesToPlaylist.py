import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QMessageBox, QStatusBar
)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional

class Song(BaseModel):
    hash: str
    levelid: str

class Playlist(BaseModel):
    playlistTitle: str
    playlistAuthor: str
    songs: List[Song]
    image: Optional[str] = Field(default='base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDA...')

class BeatSaberPlaylistConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Beat Saber Playlist Converter")

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        self.setPalette(palette)

        container = QWidget()
        container.setStyleSheet("""
            QLabel {
                color: white;
            }
            QLineEdit {
                background-color: #1E1E1E;
                color: white;
                border: 1px solid #555;
            }
            QPushButton {
                background-color: #2E2E2E;
                color: white;
                border: 1px solid #555;
            }
        """)

        layout = QVBoxLayout()

        self.input_label = QLabel("No input file selected.")
        layout.addWidget(self.input_label)

        self.input_btn = QPushButton("Select input file")
        self.input_btn.clicked.connect(self.select_input_file)
        layout.addWidget(self.input_btn)

        self.output_label = QLabel("Output file name:")
        layout.addWidget(self.output_label)

        self.output_entry = QLineEdit()
        self.output_entry.setPlaceholderText("e.g. Favorites.bplist")
        self.output_entry.setToolTip("Enter the name of the output playlist file.")
        layout.addWidget(self.output_entry)

        self.playlist_title_label = QLabel("Playlist title:")
        layout.addWidget(self.playlist_title_label)

        self.playlist_title_entry = QLineEdit()
        self.playlist_title_entry.setPlaceholderText("e.g. Mawntee's Favorites")
        self.playlist_title_entry.setToolTip("Enter the title of the playlist.")
        layout.addWidget(self.playlist_title_entry)

        self.playlist_author_label = QLabel("Playlist author:")
        layout.addWidget(self.playlist_author_label)

        self.playlist_author_entry = QLineEdit()
        self.playlist_author_entry.setPlaceholderText("e.g. Mawntee")
        self.playlist_author_entry.setToolTip("Enter the author of the playlist.")
        layout.addWidget(self.playlist_author_entry)

        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self.convert)
        layout.addWidget(self.convert_btn)

        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.input_file_path = ""
        self.last_dir = f"C:/Users/{os.getlogin()}/AppData/LocalLow/Hyperbolic Magnetism/Beat Saber"

    def select_input_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select input file", self.last_dir,
            "PlayerData file (*.dat);;All files (*.*)"
        )
        if path:
            self.input_file_path = path
            self.input_label.setText(f"Input file: {path}")
            self.last_dir = os.path.dirname(path)
            if not self.playlist_title_entry.text():
                base = os.path.splitext(os.path.basename(path))[0]
                self.playlist_title_entry.setText(f"{base} Playlist")
            self.status_bar.showMessage("Input file selected.", 5000)

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)
        self.status_bar.showMessage("Error: " + message, 5000)

    def show_info(self, message):
        QMessageBox.information(self, "Info", message)
        self.status_bar.showMessage("Info: " + message, 5000)

    def convert(self):
        if not self.input_file_path:
            self.show_error("No input file selected.")
            return

        playlist_title = self.playlist_title_entry.text().strip()
        playlist_author = self.playlist_author_entry.text().strip()
        output_file = self.output_entry.text().strip()

        if not playlist_title:
            self.show_error("Playlist title cannot be empty.")
            return

        if not playlist_author:
            playlist_author = os.getlogin()

        if not output_file:
            self.show_error("Output file name cannot be empty.")
            return

        if not output_file.lower().endswith('.bplist'):
            output_file += '.bplist'

        try:
            with open(self.input_file_path, 'r', encoding='utf-8') as f:
                input_data = json.load(f)
            favs = input_data.get('localPlayers', [{}])[0].get('favoritesLevelIds', [])
        except Exception as e:
            self.show_error(f"Failed to read input file.\n{str(e)}")
            return

        new_songs = [Song(hash=i.replace('custom_level_', ''), levelid=i) for i in favs]

        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                out_data = json.load(f)
            playlist = Playlist(**out_data)
        except:
            playlist = Playlist(playlistTitle=playlist_title, playlistAuthor=playlist_author, songs=[])

        for s in new_songs:
            if not any(m.hash == s.hash for m in playlist.songs):
                playlist.songs.append(s)

        playlist.playlistTitle = playlist_title
        playlist.playlistAuthor = playlist_author

        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Playlist", os.path.join(self.last_dir, output_file),
            "Playlist (*.bplist);;All files (*.*)"
        )
        if save_path:
            try:
                with open(save_path, 'w', encoding='utf-8') as f:
                    json.dump(playlist.dict(), f, ensure_ascii=False)
                self.show_info("Playlist saved successfully.")
            except Exception as e:
                self.show_error(f"Failed to save playlist.\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BeatSaberPlaylistConverter()
    window.show()
    sys.exit(app.exec_())
