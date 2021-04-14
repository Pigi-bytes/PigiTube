import sys
import urllib
import pytube
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
        # We load the .ui file into the class
        uic.loadUi("Ui/youtubeDownload.ui", self)


        self.scotch = False
        # Scoth , take the error of the thread and store it 

        # we found the widgets and store it into var,
        # We also associate the button and theirs function
        # ----------------------------------------------------------------------
        self.ok_button = self.findChild(QtWidgets.QPushButton, "ok")
        self.ok_button.clicked.connect(self.startThread)

        self.download = self.findChild(QtWidgets.QPushButton, "download")
        self.download.clicked.connect(self.download_button_press)
        self.download.setEnabled(False)
        # we desactivate the button

        self.input = self.findChild(QtWidgets.QLineEdit, "input")
        self.input.returnPressed.connect(self.startThread)

        self.audio_only = self.findChild(QtWidgets.QCheckBox, "audio_only")
        self.thumbnail = self.findChild(QtWidgets.QLabel, "thumbnail")
        self.titre = self.findChild(QtWidgets.QLabel, "titre")
        # ----------------------------------------------------------------------

    def startThread(self):
        threading.Thread(target=self.button_ok).start()
        if self.scotch == True:
            QMessageBox.critical(
            self,
            "Error",
            """An error occured, did you copy your url correctly? 
            Is it valid? Is it in the right format?""",)
            # we show the user the message of error
            self.scotch = False

    def button_ok(self):
        """
        Function who is call when we click on the ok button OR Press the enter key when writing in the input bar
        Here, we watch is a url is valide, and if it is, wa update the GUI
        """
        self.youtube_url = self.input.text()
        # we store the url in a more readable name
        try:
            # If a error occure here, that mean that the url is not valide

            self.video = pytube.YouTube(self.youtube_url)
            # We create the video objet, who containe the video we want
            # we use that object for all of the downloading process

            self.titre_yt = self.video.title
            # We get the title of the video

            ID = self.youtube_url[-11:]
            thumbnail_link = f"http://img.youtube.com/vi/{ID}/hqdefault.jpg"
            # We create the url of the thumbnail.
            # first of all we take the ID of the youtube video that the last 11 character.
            # We add that in a url and we can now have the link of the picture use for the thumbnail,
            # is a 480 x 360 px, jpg. => https://yt-thumb.canbeuseful.com/en

            data = urllib.request.urlopen(thumbnail_link).read()
            # we catch the data of the image into the memory bu doing a request,
            # That is what freeze the Gui..

            image = QImage()
            image.loadFromData(data)
            self.thumbnail.setPixmap(QPixmap(image))
            # we load the image into the Gui

            self.titre.setText(self.titre_yt)
            self.download.setDisabled(False)
            # We activate the download Button
        except:
            self.scotch = True
            # if something went wrong with the url

    def download_button_press(self):
        """
        Function that is called when the download button is clicked,
        it is deactivated if the url is not valid
        """
        folderpath = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")
        # We get the Path where the user want to download is file
        if folderpath != '':
            # We Check if the user dosen't have close the window 
    
            self.loadbar = ProgressBar(100, title=f"{self.titre_yt} download in progress ")
            # We create a instance of the class ProgressBar. It is for showing the user how many time left
            self.video.register_on_progress_callback(self.progress_func)
            # We say that, for each chunk of data retrived,when downloading,we call that function
            self.lastprogress = 0
            # last purcentage of the download => ssee below, that act like a reset
            if self.audio_only.isChecked():
                # if the checkbox "audio only" is check
                self.video.streams.filter(
                    only_audio=True).first().download(folderpath)
                # We download the video by filtering all of the track, and we only keep the audio.
                # That save the file in a .mp4 format
            else:
                self.video = (
                    self.video.streams.filter(
                    progressive=True, file_extension="mp4")
                    .order_by("resolution")
                    .desc()
                    .first()
                    .download(folderpath)
                            )
                # We save the video by filtering the best quality video with the .mp4 format and download it.
                # that save the file in a .mp4 format

            MessageBeep(-1)
            # do a bip 

    def progress_func(self, stream, chunk, bytes_remaining):
        """
        Function call eatch time we retrive data from the download
        """
        total_size = stream.filesize
        # we get the size of the video we want to download
        bytes_downloaded = total_size - bytes_remaining
        # we get the total of bytes downloaded
        liveprogress = int(bytes_downloaded / total_size * 100)
        # we make a purcentage of that
        if liveprogress > self.lastprogress:
            # if the pourcentage is greater that the last purcentage,
            # is for making it less buggy and more smooth
            self.loadbar.setValue(liveprogress)
            # we update the progress bar
        self.lastprogress = liveprogress
        # we add lastprogress in a var
       
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
    # Show the calculator's GUI
    window = Ui()
    window.show()
    # Execute the calculator's main loop
    sys.exit(app.exec_())




