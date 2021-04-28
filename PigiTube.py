#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import shutil
import subprocess
import re
import urllib
import threading
from pathlib import Path
try:
    from winsound import MessageBeep
except:
    ENV = 'LINUX/OSX'
import pytube

from PyQt5 import QtWidgets, uic
from PyQt5.Qt import QProgressDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QMessageBox
import ressource_rc

# import needed => pytube ; PyQt5 + PyQt5-tools


class Ui(QtWidgets.QMainWindow):
    """
    class which takes care of loading the .ui file and showing it, it is the main class
    """

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("Ui/PigiTube.ui", self)
        # We load the .ui file into the class

        self.path_temp = Path(os.getcwd(), "Temp")
        self.reset_temp_file()

        # we found the widgets and store them into var,
        # We also associate the button and their functions
        # ----------------------------------------------------------------------
        self.ok_button = self.findChild(QtWidgets.QPushButton, "ok")
        self.ok_button.clicked.connect(self.button_ok_press)

        self.input = self.findChild(QtWidgets.QLineEdit, "input")
        self.input.returnPressed.connect(self.button_ok_press)

        self.download = self.findChild(QtWidgets.QPushButton, "download")
        self.download.clicked.connect(self.download_button_press)
        self.download.setEnabled(False)
        # we desactivate the button

        self.audio_only = self.findChild(QtWidgets.QCheckBox, "audio_only")
        self.thumbnail = self.findChild(QtWidgets.QLabel, "thumbnail")
        self.titre = self.findChild(QtWidgets.QLabel, "titre")
        # ----------------------------------------------------------------------

    def button_ok_press(self):
        self.error_in_thread_ok = False
        # If an error occurs in the thread we store it in this variable
        threading.Thread(target=self.Thread_for_get_data).start()
        # We start the Thread
        if self.error_in_thread_ok == True:
            # if the var is set to TRUE in the thread , that means we have an error
            # and that our url is not valid
            error = "An error occurred with your url, Make sure it is in the right format, \
                    that it is not a video from a playlist, or have a time indicator in the url (if it ends with something like [&t=??s] )"
            QMessageBox.critical(
            self,
            "Error",
            error,)
            # we show the user the message of error

    def Thread_for_get_data(self):
        """
        Here, we watch if a url is valid, and if it is, we update the GUI, title and thumbnail
        """
        self.youtube_url = self.input.text()
        # we store the url in a more readable name
        try:
            if len(self.youtube_url) != 43:
                self.error_in_thread_ok = True
                raise('Url pas de la bonne taille')
            # If an error occurs here, that means that the url is not valide

            self.video = pytube.YouTube(self.youtube_url)
            # We create the video objet, which contains the video we want
            # we use that object for all of the downloading process

            self.titre_yt = self.video.title
            # We get the title of the video

            ID = self.youtube_url[-11:]
            thumbnail_link = f"http://img.youtube.com/vi/{ID}/hqdefault.jpg"
            # We create the url of the thumbnail.
            # first of all we take the ID of the youtube video, the last 11 character.
            # We add that in a url and we can now have the link of the picture used for the thumbnail,
            # is a 480 x 360 px, jpg. => https://yt-thumb.canbeuseful.com/en

            data = urllib.request.urlopen(thumbnail_link).read()
            # we catch the data of the image into the memory by doing a request,

            image = QImage()
            image.loadFromData(data)
            self.thumbnail.setPixmap(QPixmap(image))
            # we load the image into the Gui

            self.titre.setText(self.titre_yt)
            self.download.setDisabled(False)
            # We activate the download Button
        except:
            self.error_in_thread_ok = True
            # if something went wrong with the url

    def download_button_press(self):
        """
        Function that is called when the download button is clicked,
        it is deactivated if the url is not valid
        """
        self.folderpath = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Folder")
        # We get the Path where the user wants to download his file
        if self.folderpath != '':
            # We Check if the user hasn't closed the window for choosing his file
            if self.audio_only.isChecked():
                # if the checkbox "audio only" is checked
                self.download_mp3()
            else:
               self.download_mp4()

    def progress_func_mp3(self, stream, chunk, bytes_remaining):
        """
        Function call eatch time we retrive data from the download
        """
        total_size = stream.filesize
        # we get the size of the video we want to download
        bytes_downloaded = total_size - bytes_remaining
        # we get the total of bytes downloaded
        liveprogress = int(bytes_downloaded / total_size * 98)
        # we make a percentage of that
        self.loadbar.setValue(liveprogress)
        # we update the progress bar

    def progress_func_mp4(self, stream, chunk, bytes_remaining):
        """
        Function call eatch time we retrive data from the download
        """
        total_size = stream.filesize
        # we get the size of the video we want to download
        bytes_downloaded = total_size - bytes_remaining
        # we get the total of bytes downloaded
        liveprogress = int(bytes_downloaded / total_size * 100)
        # we make a percentage of that
        self.loadbar.setValue(liveprogress)
        # we update the progress bar

    def download_mp3(self):
        """
        Function for downloading into .mp3
        """
        self.loadbar = ProgressBar(100, title=f"{self.titre_yt} download in progress ")
        # create a instance of the class for showing progress
        # function call when we retrive a chunk of dat
        self.video.register_on_progress_callback(self.progress_func_mp3)

        # The name we will use to rename the file, witout bad characters
        titre_rename = self.character_control(self.titre_yt)
        titre_enregistrement = 'FFMPEG_compatible'  # name compatible with FFMPEG

        path_folder_and_file_name = Path(self.folderpath, titre_rename)
        path_final = self.unique_filename(path_folder_and_file_name, '.mp3')
        titre_rename = path_final.name
        # we get the final name for the file ; if on a folder they already have the file with the same name we had a number in front

        yt_str = self.video.streams.filter(only_audio=True, file_extension='mp4').first()
        yt_str.download(self.path_temp, filename=titre_enregistrement)
        # We download the video by filtering all of the tracks, and we only keep the audio.
        # That saves the file in a .mp4 format into the Temp file

        # -----------------------conversion--------------------------------------------
        filePathMp4 = Path(self.path_temp, "FFMPEG_compatible.mp4")
        filePathMp3 = Path(self.path_temp, "FFMPEG_compatible.mp3")

        # command for converting .mp4 to .mp3
        ffmpeg = subprocess.call(["./FFmpeg/bin/ffmpeg.exe", '-i', filePathMp4, filePathMp3])
        self.loadbar.setValue(99)  # the download stop at 98%

        os.remove(filePathMp4)  # we delete the .mp4 file created

        filePathMp3 = filePathMp3.rename(filePathMp3.with_name(titre_rename + ".mp3"))  # we rename the .mp3 file
        # we move the file to the good directory
        shutil.move(filePathMp3, self.folderpath)

        self.loadbar.setValue(100)  # we show that the process had finish
        if ENV != 'LINUX/OSX':
            MessageBeep(-1)

    def download_mp4(self):
        """
        Function for downloading in .mp4
        """
        self.video.register_on_progress_callback(self.progress_func_mp4)

        titre_rename = self.character_control(self.titre_yt)

        path_folder_and_file_name = Path(self.folderpath, titre_rename)
        path_final = self.unique_filename(path_folder_and_file_name, '.mp4')
        titre_rename = path_final.name

        audio_stream = self.video.streams.filter(adaptive=True, only_audio=True, file_extension='mp4').desc()
        video_stream = self.video.streams.filter(adaptive=True, res='1080p', file_extension='mp4').order_by('resolution').desc()
        if len(video_stream) == 0:  # if no 1080
            video_stream = self.video.streams.filter( adaptive=True, file_extension='mp4').order_by('resolution').desc()

        self.loadbar = ProgressBar(100, title=f"{self.titre_yt} video download in progress ")
        video_stream.first().download(self.path_temp, filename='video')
        self.loadbar = ProgressBar(100, title=f"{self.titre_yt} audio download in progress ")
        audio_stream.first().download(self.path_temp, filename='audio')

        # -----------------------merging--------------------------------------------
        filePathVideo = Path(self.path_temp, 'video.mp4')
        filePathAudio = Path(self.path_temp, 'audio.mp4')
        filePathFinal = Path(self.path_temp, 'final.mp4')

        subprocess.run(["./FFmpeg/bin/ffmpeg.exe", '-i', filePathAudio,"-i", filePathVideo, '-c', 'copy', filePathFinal])

        os.remove(filePathVideo)
        os.remove(filePathAudio)
        # we delete the .mp4 file created in the first place

        filePathFinal = filePathFinal.rename(filePathFinal.with_name(titre_rename + ".mp4"))  # we rename the .mp3 file
        # we move the file to the good directory
        shutil.move(filePathFinal, self.folderpath)
        if ENV != 'LINUX/OSX':
            MessageBeep(-1)
        # does a bip

    def unique_filename(self, output_filename, file_extension):
        """
        Return the name for the file, 
        if the name already exist, we add (n) in frontself.
        """
        n = ''
        while os.path.exists(f'{output_filename}{n}{file_extension}'):
            if isinstance(n, str):
                n = -1
            n += 1
        return Path(f'{output_filename}{n}')

    def reset_temp_file(self):
        """
        Reset the temp file
        """
        shutil.rmtree(self.path_temp)
        os.mkdir(self.path_temp)

    def character_control(self, world):
        """
        Return a title for the video without character that will broke the app
        """
        if (world.isascii() == False) or (any(c in '/\:*?"<>|' for c in world) == True):
            # if there are symbols not ascii or not compatible with window's filesystem
            titre_rename = re.sub(r'[^\x00-\x7F]+', '', world)
            # we removes non ascii characters
            for char in '/\:*?"<>|':
                titre_rename = titre_rename.replace(char, '')
                # we removes "illegal" non window characters from filenames
        else:
            titre_rename = world
        
        return titre_rename


class ProgressBar(QProgressDialog):
    """
    Class for the progressbar
    """

    def __init__(self, max, title):
        super().__init__()
        # Sets how long the loop should last before progress bar is shown (in miliseconds)
        self.setMinimumDuration(0)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setLabelText(title)
        self.setCancelButton(None)

        self.setValue(0)
        self.setMinimum(0)
        self.setMaximum(max)


if __name__ == "__main__":
    # Create an instance of QApplication
    app = QtWidgets.QApplication(sys.argv)
    # Show the downloader's GUI
    window = Ui()
    window.show()
    # Execute the downloader's main loop
    sys.exit(app.exec_())
