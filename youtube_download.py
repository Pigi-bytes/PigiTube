import os
import sys
import urllib
import pytube
import subprocess
import threading
from winsound import MessageBeep

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
        uic.loadUi("Ui/youtubeDownload.ui", self)
        # We load the .ui file into the class

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
        self.error_in_thread = False
        # If an error occurs in the thread we store it in this variable 
        threading.Thread(target=self.Thread_for_get_data).start()
        # We start the Thread 
        if self.error_in_thread == True:
            # if the var is set to TRUE in the thread , that means we have an error
            # and that our url is not valid 
            QMessageBox.critical(
            self,
            "Error",
            """An error occured, did you copy your url correctly? 
            Is it valid? Is it in the right format?""",)
            # we show the user the message of error

    def Thread_for_get_data(self):
        """
        Here, we watch if a url is valid, and if it is, we update the GUI, title and thumbnail 
        """
        self.youtube_url = self.input.text()
        # we store the url in a more readable name
        try:
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
            self.error_in_thread = True
            # if something went wrong with the url

    def download_button_press(self):
        """
        Function that is called when the download button is clicked,
        it is deactivated if the url is not valid
        """
        self.folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")
        # We get the Path where the user wants to download his file
        if self.folderpath != '':
            # We Check if the user hasn't closed the window for choosing his file 
            self.loadbar = ProgressBar(100, title=f"{self.titre_yt} download in progress ")
            # We create an instance of the class ProgressBar. It is for showing the user how much time is left
            self.video.register_on_progress_callback(self.progress_func)
            # We say that, for each chunk of data retrieved,when downloading,we call that function
            self.lastprogress = 0
            # last percentage of the download => see below, that acts like a reset
            if self.audio_only.isChecked():
                # if the checkbox "audio only" is checked
                self.video.streams.filter(only_audio=True).first().download(self.folderpath)
                # We download the video by filtering all of the tracks, and we only keep the audio.
                # That saves the file in a .mp4 format
                threading.Thread(target=self.Thread_for_conversion).start()
                # we call a thread for converting the video into audio, bc if the video is huge, the process 
                # while take a while and halt the GUI
            else:
                self.video = (
                    self.video.streams.filter(
                    progressive=True, file_extension="mp4")
                    .order_by("resolution")
                    .desc().first()
                    .download(self.folderpath))
                # We save the video by filtering the best quality video with the .mp4 format and download it.
                # that save the file in a .mp4 format

                MessageBeep(-1)
                # does a bip 

    def progress_func(self, stream, chunk, bytes_remaining):
        """
        Function call eatch time we retrive data from the download
        """
        total_size = stream.filesize
        # we get the size of the video we want to download
        bytes_downloaded = total_size - bytes_remaining
        # we get the total of bytes downloaded
        liveprogress = int(bytes_downloaded / total_size * 100)
        # we make a percentage of that
        if liveprogress > self.lastprogress:
            # if the pourcentage is greater that the last percentage,
            # is for making it less buggy and smoother
            self.loadbar.setValue(liveprogress)
            # we update the progress bar
        self.lastprogress = liveprogress
        # we add lastprogress in a var

    def Thread_for_conversion(self):
        """
        It the Thread that is call for doing the conversion 
        """
        ffplay_path = "./ffmpeg/ffmpeg.exe"
        # we get the path of the executable for ffmpeg 
        filePath = self.folderpath + '/' + self.titre_yt 
        # we get the path of the file
        subprocess.call([self.resource_path(ffplay_path),
                        '-i', filePath + '.mp4', filePath + '.mp3' ])
                        # we call subprocess for doing a command that will convert
                        # .mp4 audio file into .mp3 
        os.remove(filePath + '.mp4')
        # we delete the .mp4 file created in the first place
        MessageBeep(-1)
        # does a bip 

    def resource_path(self, relative_path):
        """
        Get the path for executable bin  
        """
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)    


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
