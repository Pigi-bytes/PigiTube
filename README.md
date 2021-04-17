Youtube Download.

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

**WARNING If the title contains characters which are not supported, the file will be renamed ("title_encoding_not_supported.mp3") so that the conversion algorithm can work.**  
Note that this only affects if you choose to just download the audio track.

Then you have to choose the place where it should be downloaded.

Normally it should have the name of your video, but if the character present in it does not support the video to audio conversion algorithm it will have the following name : "title_encoding_not_supported.mp3".

# What are the video recording formats ?

The application allows you to download videos in :

- Audio format (.mp3)

- Video format (.mp4)

This app uses FFMPEG to convert .mp4 files to .mp3.

# Dependency.

this app is based on PyQt5 , FFMPEG and Pytube.
