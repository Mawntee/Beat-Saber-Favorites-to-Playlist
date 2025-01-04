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
    image: Optional[str] = Field(default='base64,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')

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
