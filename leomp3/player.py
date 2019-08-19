import vlc
import time
import os
import random
import sys

from vlc import State, Instance
from PyQt5.QtWidgets import QApplication
from leomp3.youtube_wrapper import *


class Music_Player():

    def __init__(self):
        self.player = None
        self.playing = False
        self.song_dictionary= {}
        self.current_playlist = []
        self.music_dirs = []
        self.current_song_index = 0
        self.is_online = False
        self.muted = False
        self.current_volume = 100

    def start(self, music_dirs):
        self.music_dirs = music_dirs
        self.create_playlist()
        self.vlcInstance = Instance('--novideo')
        self.player = self.vlcInstance.media_player_new()

    def create_playlist(self):
        self.current_playlist = []
        path_list = []

        for music_dir in self.music_dirs:
            path_list = self.get_songs_in_folder(music_dir, path_list)

        for song_path in path_list:
            song_name = self.get_song_name(song_path)
            self.song_dictionary[song_name] = song_path
            self.current_playlist.append(song_name)

        self.current_song_index = 0
        self.is_online = False

    def set_custom_playlist(self, list):
        self.current_playlist = list
        self.current_song_index = 0

    def create_online_dictionary(self, song_name):
        self.song_dictionary = yt_search(song_name)
        self.current_playlist = []

        for song in self.song_dictionary.keys():
            self.current_playlist.append(song)

        self.current_song_index = 0
        self.is_online = True

    def shuffle_playlist(self):
        random.shuffle(self.current_playlist)
        self.current_song_index = 0

    def next(self):
        if len(self.current_playlist) > 0:
            self.current_song_index = (self.current_song_index + 1) % len(self.current_playlist)

            if self.playing:
                self.stop()
                self.play()

    def skip_to_song(self, index):
        self.current_song_index = index % len(self.current_playlist)

    def previous(self):
        if len(self.current_playlist) > 0:
            self.current_song_index = (self.current_song_index - 1) % len(self.current_playlist)

            if self.playing:
                self.stop()
                self.play()

    def stop(self):
        self.player.stop()
        self.playing = False

    def play(self):

        if self.current_playlist:
            if self.playing == False:
                song_name = self.current_playlist[self.current_song_index]
                song = self.song_dictionary[song_name]

                if self.is_online == True:
                    song = yt_stream(song)

                media = self.vlcInstance.media_new(song)
                media.get_mrl()
                self.player.set_media(media)
                self.player.play()
                self.playing = True
                time.sleep(1)

            else:
                self.player.pause()

    def get_duration(self):
        song_duration = self.player.get_length()/1000
        return time.strftime('%H:%M:%S', time.gmtime(song_duration))

    def get_time(self):
        song_time = self.player.get_time()/1000
        return time.strftime('%H:%M:%S', time.gmtime(song_time))

    def pause(self):
        self.player.pause()

    def get_state(self):
        return self.player.get_state()

    def get_songs_in_folder(self, path, song_list):

        for file in os.listdir(path):
            file_path = os.path.join(path, file)

            if (os.path.isdir(file_path)):
                self.get_songs_in_folder(file_path, song_list)
            elif(file_path.endswith('.mp3')):
                song_list.append(file_path)

        song_list = list(dict.fromkeys(song_list))

        return song_list

    def get_current_playlist(self):
        return self.current_playlist

    def get_song_name(self, song):
        # if (song.startswith('https://www.youtube.com/watch')):
        #     return yt_get_title(song)
        return song.split('/')[-1][:-4]

    def get_current_song_name(self):
        if not self.current_playlist:
            return ""
        return self.current_playlist[self.current_song_index]

    def get_current_song_path(self):
        if not self.current_playlist:
            return ""

        song_name = self.current_playlist[self.current_song_index]
        song = self.song_dictionary[song_name]
        return song

    def get_elapsed_percentage(self):
        percentage = self.player.get_position() * 100
        return percentage

    def get_volume(self):
        return self.player.audio_get_volume()

    def set_volume(self, volume):
        self.current_volume = volume
        if self.muted == False:
            self.player.audio_set_volume(self.current_volume)

    def mute(self):

        if self.muted == True:
            self.player.audio_set_volume(self.current_volume)
            self.muted = False
        else:
            self.player.audio_set_volume(0)
            self.muted = True

    def seek(self, position):
        self.player.set_position(position)
