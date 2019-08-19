from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
import time
import vlc
from vlc import State
from leomp3.player import Music_Player
from leomp3.youtube_wrapper import *
import threading
import os
import yaml

class Music_Player_GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.run = True

        self.music_dirs = []
        self.player_dir = os.path.join(os.environ['HOME'], 'Music/LeoMP3')
        self.download_dir = os.path.join(self.player_dir, 'Downloads')

        self.config_dir = os.path.join(self.player_dir, 'Configs')
        # self.music_dir, self.download_dir =
        self.get_config(self.config_dir)
        self.music_dirs.append(self.download_dir)

        self.title = "Leo MP3 Player"
        self.top = 100
        self.left = 100
        self.width = 600
        self.height = 450

        self.icons_dir = os.path.join(self.config_dir, 'Icons')
        self.online_search_complete = False

        # Png Files
        self.player_icon = os.path.join(self.icons_dir, 'Player.png')
        self.play_icon = os.path.join(self.icons_dir, 'Play.png')
        self.pause_icon = os.path.join(self.icons_dir, 'Pause.png')
        self.next_icon = os.path.join(self.icons_dir, 'Next.png')
        self.previous_icon = os.path.join(self.icons_dir, 'Previous.png')
        self.download_icon = os.path.join(self.icons_dir, 'Download.png')
        self.stop_icon = os.path.join(self.icons_dir, 'Stop.png')
        self.shuffle_icon = os.path.join(self.icons_dir, 'Shuffle.png')
        self.search_icon = os.path.join(self.icons_dir, 'Search.png')
        self.reload_icon = os.path.join(self.icons_dir, 'Reload.png')
        self.mute_icon = os.path.join(self.icons_dir, 'Mute.png')
        self.volume_icon = os.path.join(self.icons_dir, 'Volume.png')

        self.player = Music_Player()
        self.player.start(self.music_dirs)
        self.InitWidow()
        self.update_playlist()
        self.update_title()
        self.player_on()

    def get_config(self, config_dir):
        config_file = os.path.join(config_dir, 'configs.yml')
        if os.path.exists(config_file):
            with open(config_file, 'r') as config:
                data_loaded = yaml.safe_load(config)

            self.music_dirs = data_loaded['MUSIC_DIRS']
            self.download_dir = data_loaded['DOWNLOAD_DIR']


    def InitWidow(self):
        self.setWindowIcon(QtGui.QIcon(self.player_icon))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.size())

        self.create_title_label()
        self.create_time_label()
        self.create_duration_label()
        self.create_play_pause_button()
        self.create_next_button()
        self.create_previous_button()
        self.create_shuffle_button()
        self.create_stop_button()
        self.create_playlist_window()
        self.create_seek_bar()
        self.create_search_box()
        self.create_search_local_button()
        self.create_search_online_button()
        self.create_path_box()
        self.create_download_button()
        self.create_reload_button()
        self.create_clear_search_button()
        self.create_sound_bar()
        self.create_mute_button()

        self.show()

    #===========================================================================
    # Player buttons
    #===========================================================================

    def create_play_pause_button(self):
        self.play_button = QPushButton(self)
        self.play_button.setGeometry(QRect(410,210,80,80))
        self.play_button.setIcon(QtGui.QIcon(QPixmap(self.play_icon)))
        self.play_button.setIconSize(QtCore.QSize(70,70))
        self.play_button.setToolTip('Play/Pause')

        self.play_button.clicked.connect(self.play_pause)


    def create_next_button(self):
        button = QPushButton(self)

        button.setGeometry(QRect(490,210,80,80))
        button.setIcon(QtGui.QIcon(QPixmap(self.next_icon)))
        button.setIconSize(QtCore.QSize(50,50))
        button.setToolTip('Next')

        button.clicked.connect(self.next_song)


    def create_previous_button(self):
        button = QPushButton(self)

        button.setGeometry(QRect(330,210,80,80))
        button.setIcon(QtGui.QIcon(QPixmap(self.previous_icon)))
        button.setIconSize(QtCore.QSize(50,50))
        button.setToolTip('Previous')

        button.clicked.connect(self.previous_song)

    def create_stop_button(self):
        button = QPushButton(self)

        button.setGeometry(QRect(410,290,80,80))
        button.setIcon(QtGui.QIcon(QPixmap(self.stop_icon)))
        button.setIconSize(QtCore.QSize(50,50))
        button.setToolTip('Stop')

        button.clicked.connect(self.stop_song)


    def create_shuffle_button(self):
        button = QPushButton(self)

        button.setGeometry(QRect(410,130,80,80))
        button.setIcon(QtGui.QIcon(QPixmap(self.shuffle_icon)))
        button.setIconSize(QtCore.QSize(50,50))
        button.setToolTip('Shuffle')

        button.clicked.connect(self.shuffle_songs)

    def create_sound_bar(self):
        self.sound_bar = QSlider(Qt.Horizontal, self)
        self.sound_bar.setFocusPolicy(Qt.NoFocus)
        self.sound_bar.setGeometry(QRect(480,410,100,20))
        self.sound_bar.setValue(100)

        self.sound_bar.valueChanged[int].connect(self.volume_change)

    def create_mute_button(self):
        self.mute_button = QPushButton(self)

        self.mute_button.setGeometry(QRect(440,400,40,40))
        self.mute_button.setIcon(QtGui.QIcon(QPixmap(self.volume_icon)))
        self.mute_button.setIconSize(QtCore.QSize(30,30))
        self.mute_button.setToolTip('Mute/Unmute')

        self.mute_button.clicked.connect(self.mute_audio)

    def mute_audio(self):
        self.player.mute()

        if self.player.muted:
            self.mute_button.setIcon(QtGui.QIcon(QPixmap(self.mute_icon)))
            self.mute_button.setIconSize(QtCore.QSize(30,30))

        else:
            self.mute_button.setIcon(QtGui.QIcon(QPixmap(self.volume_icon)))
            self.mute_button.setIconSize(QtCore.QSize(30,30))

    def volume_change(self):
        new_volume = self.sound_bar.value()
        self.player.set_volume(new_volume)

    def shuffle_songs(self):
        self.player.shuffle_playlist()
        self.update_playlist()
        self.stop_song()
        self.play_pause()

    def previous_song(self):
        self.player.previous()
        self.update_title()

    def next_song(self):
        self.player.next()
        self.update_title()

    def play_pause(self):
        self.player.play()
        self.update_title()
        self.sound_bar.setValue((self.player.get_volume()))

    def stop_song(self):
        self.player.stop()
        self.seek_bar.setValue(0)

    def update_title(self):
        song_name = self.player.get_current_song_name()
        self.title_label.setText(song_name)
        self.playlist_list.setCurrentItem(self.playlist_list.findItems(song_name,
                                        Qt.MatchExactly)[0])
        path = self.player.get_current_song_path()
        self.path_box.setText(path)

    def update_playlist(self):
        playlist = self.player.get_current_playlist()

        self.playlist_list.clear()

        for id, song in enumerate(playlist):
            self.playlist_list.insertItem(id, song)


    #===========================================================================
    # Title bar and seek bar
    #===========================================================================

    def create_seek_bar(self):
        self.seek_bar = QSlider(Qt.Horizontal, self)
        self.seek_bar.setFocusPolicy(Qt.NoFocus)
        self.seek_bar.setGeometry(30, 40, 540, 30)
        self.seek_bar.setValue(0)
        self.seek_bar.setTracking(False)
        self.seek_bar.valueChanged.connect(self.seek_song)


    def create_title_label(self):
        self.title_label = QLabel(self)
        self.title_label.setGeometry(QRect(30,20,540,30))
        self.title_label.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Black))

    def create_time_label(self):
        self.time_label = QLabel(self)
        self.time_label.setGeometry(QRect(30,60,80,20))
        self.time_label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Black))

    def create_duration_label(self):
        self.duration_label = QLabel(self)
        self.duration_label.setGeometry(QRect(500,60,80,20))
        self.duration_label.setFont(QtGui.QFont("Arial", 12, QtGui.QFont.Black))

    def seek_song(self):
        new_position = self.seek_bar.value()/100
        self.player.seek(new_position)


    #===========================================================================
    # Playlist Area
    #===========================================================================

    def create_reload_button(self):
        button = QPushButton(self)
        button.setGeometry(QRect(280,340,40,40))
        button.setIcon(QtGui.QIcon(QPixmap(self.reload_icon)))
        button.setIconSize(QtCore.QSize(30,30))
        button.setToolTip('Reload Local Playlist')

        button.clicked.connect(self.reload_playlist)

    def create_playlist_window(self):
        self.playlist_list = QListWidget(self)
        self.playlist_list.setGeometry(QRect(30,180,250,200))
        self.playlist_list.itemDoubleClicked.connect(self.play_clicked_song)

    def reload_playlist(self):
        self.player.create_playlist()
        self.update_playlist()
        self.stop_song()
        self.update_title()

    def play_clicked_song(self, song):
        song_id = self.playlist_list.indexFromItem(song).row()
        self.player.skip_to_song(song_id)
        self.stop_song()
        self.play_pause()

    #===========================================================================
    # Search bar
    #===========================================================================

    def create_search_box(self):
        self.search_box = QLineEdit(self)
        self.search_box.setGeometry(QRect(30,100,220,30))

    def create_search_local_button(self):
        button = QPushButton("Search Local", self)
        button.setIcon(QtGui.QIcon(QPixmap(self.search_icon)))
        button.setGeometry(QRect(30,130,120,30))
        button.setToolTip('Search in Local Disk')

        button.clicked.connect(self.search_local)

    def create_search_online_button(self):
        self.search_button = QPushButton("Search Online", self)
        self.search_button.setIcon(QtGui.QIcon(QPixmap(self.search_icon)))
        self.search_button.setGeometry(QRect(160,130,120,30))
        self.search_button.setToolTip('Search in youtube.com')

        self.search_button.clicked.connect(self.search_online)

    def create_clear_search_button(self):
        button = QPushButton("X", self)
        button.setGeometry(QRect(250,100,30,30))
        button.setToolTip('Clear')

        button.clicked.connect(self.clear_search)

    def clear_search(self):
        self.search_box.setText("")

    def search_in_thread(self, song_name):
        self.player.create_online_dictionary(song_name)
        self.online_search_complete = True

    def finished_online_search(self):
        # self.player.create_online_dictionary(song_name)
        self.update_playlist()
        self.stop_song()
        self.update_title()
        self.online_search_complete = False
        self.search_button.setEnabled(True)
        self.search_button.setText("Search Online")

    def search_online(self):
        song_name = self.search_box.text()

        if song_name != "":
            self.search_button.setEnabled(False)
            self.search_button.setText("Searching...")
            t = threading.Thread(target=self.search_in_thread, args=(song_name,), daemon=True)
            t.start()

    def search_local(self):
        song_name = self.search_box.text()

        if song_name != "":
            self.reload_playlist()
            items = self.playlist_list.findItems(song_name, Qt.MatchContains)

            new_playlist = []
            if (len(items) > 0):
                for item in items:
                    new_playlist.append(item.text())
                self.player.set_custom_playlist(new_playlist)
                self.update_playlist()

            else:
                QMessageBox.question(self, 'No Songs Found', "No Songs Found!", QMessageBox.Ok, QMessageBox.Ok)


    #===========================================================================
    # Download area
    #===========================================================================

    def create_path_box(self):
        self.path_box = QLineEdit(self)
        self.path_box.setGeometry(QRect(30,400,250,30))

    def create_download_button(self):
        self.download_button = QPushButton(self)
        self.download_button.setText("Download")
        self.download_button.setIcon(QtGui.QIcon(QPixmap(self.download_icon)))
        self.download_button.setGeometry(QRect(280,400,120,30))
        self.download_button.setToolTip('Download and Save to Local Directory')
        self.download_button.clicked.connect(self.download_song)

    def download_in_thread(self, url):
        self.download_button.setEnabled(False)
        self.download_button.setText("Downloading...")
        yt_download(url, self.download_dir)
        self.download_button.setEnabled(True)
        self.download_button.setText("Download")


    def download_song(self):
        url = self.path_box.text()

        if (url.startswith('https://')):
            t = threading.Thread(target=self.download_in_thread, args=(url,), daemon=True)
            t.start()

        else:
            QMessageBox.question(self, 'Invalid URL', "URL is invalid!", QMessageBox.Ok, QMessageBox.Ok)


    #===========================================================================
    # Player Loop
    #===========================================================================

    def player_on(self):
        while True:

            # print("in loop:", self.player.get_state())
            QApplication.processEvents()
            time.sleep(0.05)

            if self.player.get_state() == State.Playing:
                self.play_button.setIcon(QtGui.QIcon(QPixmap(self.pause_icon)))
                self.duration_label.setText(self.player.get_duration())
                self.time_label.setText(self.player.get_time())

                self.seek_bar.blockSignals(True)
                self.seek_bar.setValue(self.player.get_elapsed_percentage())
                self.seek_bar.blockSignals(False)

            else:
                self.play_button.setIcon(QtGui.QIcon(QPixmap(self.play_icon)))

            if (self.run == False):
                sys.exit()

            if self.player.get_state() == State.Ended:
                self.next_song()

            if self.online_search_complete:
                self.finished_online_search()


    def closeEvent(self, event):

        self.run = False
        event.accept()
