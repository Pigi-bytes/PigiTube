# Youtube Download.

An application to download YouTube videos, with a GUI, provided by PyQt5

# How to use youtube downloader ?

You must enter the url of your video in the field provided for this purpose this url must be submitted in the form as :

```.md
https://www.youtube.com/watch?v=xxxxxxxxxxx
Where xxxxxxxxxxx is the ID of the video 

All other urls from youtube are not supported
```

Then you have to click on the button 'ok' next to it. Wait a few seconds, the thumbnail and the title should be displayed to confirm that the desired video is indeed the correct one.

If you only want audio, activate the small checkbox, it will only download the audio track : this will be in the form of an .mp3 file : 

**WARNING If the title contains characters which are not supported, the file will be renamed, without the problematic character.**

Then you have to choose the place where it should be downloaded, and wait...



The video will take much longer for the video :

- For the .mp3, we download an .mp4 with only audio channels and we converted it to .mp3 with post processing software (FFMPEG)

- We download the audio in .mp4, and the video in .mp4 and have them merge with post processing software (FFMPEG) together to have the best video quality

# What are the video recording formats ?

The application allows you to download videos in :

- Audio format (.mp3)

- Video format (.mp4)

This app uses FFMPEG to convert .mp4 files to .mp3.

# Dependency.

this app is based on PyQt5 , FFMPEG and Pytube.


# For installing 

## With the standAlone

just run the installation file in the folder "Standalone_Installler" and that all

## With Python

you need :
- Python (3.6+) in the PATH
- PIP (include in the installer of python)

It's better to create a virtual environment, type in the console :
- For creating the Venv :

```.powershell
py -m venv ./venv 
```
- to launch it (on window)
```.powershell
venv/scripts/activate
```

- Now our venv is operational, clone the repertory into the venv
Run this command,   its going to install all the dependencies and this will do it locally, in the virtual environment
```.powershell
pip install -r requirements.txt
```
- for launching the app, do : 
```.powershell
py youtube_download.py 
```
