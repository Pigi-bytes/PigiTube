# PigiTube :

## Dependance
This app use [PyQt5](#PyQt5) for the GUI(Grapiqual User Interface), [Pytube](#Pytube) for downloading stream from youtube, and [FFmpeg](#FFMPEG), for all the conversion and that kind of stuff.  
I only own the code from PigiTube.py, as my [Liscense](license) say.

## What is this ?
This is an application to download YouTube videos, with a simple GUI for personnal usage ONLY.
I am not responsible for your actions.

## Table of Contents of PigiTube
1.  [How to install PigiTube ?](#Install)
2.  [How to use PigiTube](#Usage)
3.  [How do PigiTube Download video ?](#Download)
4.  [What are the format / CODEC ?](#CODECS_&_Formats)
5.  [Dash Vs Progressive download](#DASH)
6.  [Post Processing software](#FFMPEG)
7.  [Graphical user interface](#PyQt5)
8.  [Api for youtube video](#Pytube)
9.  [Liscense and legal notice](#License)
10. [Source and link useful for that project](#source)
11. [Contributeur](#Contributeur)

# **Install**

## With the standAlone (only window confirmed)
Only work for window, or maybe MAC/linux with WINE but idk..
If you live at the time of the dinosaurs and you still have a pc on window 7, choose the executable addequate, same for the users of window 10, It on the StandAlone_Installer folder ( not yet D: ).

## With Python (all platform)

For that you will need Python 3.8+ and Pip in the PATH.  
First we are going to get the repertory on github and with the following command : Open the command prompt into your folder and type :
```
git clone https://github.com/Pigi-bytes/Youtube_download.git
cd  Youtube_download
```
Now, we have download the app, and we are inside...  
 This is the right time to create a venv
known as Virtual Environment Its will allow you to keep your python file clean and have specific version for your pip paquetages.  
We create a Venv with the following command :
```
py -m venv ./venv 
```
All this is good but he must be activated, so we run this command :
```
venv/scripts/activate
```
We can download the different modules that we will need in the venv:
```
pip install -r requirements.txt
```
And for launching the app you will need to type this ( when your into the venv)
```
py youtube_download.py 
```

## To sum up : 

Setup :
```
git clone https://github.com/Pigi-bytes/Youtube_download.git
cd  Youtube_download
py -m venv ./venv 
venv/scripts/activate
pip install -r requirements.txt
```
From now on you just have to execute these two commands to make it work (on the folder):
```
venv/scripts/activate
py youtube_download.py 
```

# Usage

You must enter the url of your video in the field provided for this purpose, this url must be submitted in the form as :

> https://www.youtube.com/watch?v=xxxxxxxxxxx  
> Where xxxxxxxxxxx is the ID of the video.  
>
> All other urls from youtube are not supported :  
> (mobile URL, URL with time, a video into a playlist)

Then you have to click on the button 'ok' next to it. Wait a few seconds, the thumbnail and the title should be displayed to confirm that the desired video is indeed the correct one.

If you only want audio, activate the small checkbox, it will only download the audio track : this will be in the form of an .mp3 file : otherwise it will be the video (by default) and a .mp4 file.

***WARNING : If the title contains characters which are not supported, the file will be renamed, without the problematic character. And if a file already has the name of the video in the downloading folder, a prefix will be added.***

After that you have to choose the place where it should be downloaded, and wait for the bip...

# Download

**The speed will depend on your internet connection (downward flow) and the speed of your hardware.**

It should also be noted that the download takes longer depending on the type of media to download : 

## For audio only :
---
The application will download the best audio quality of your video, in the .mp4 format ( Which just contains the codecs / channels for the audio, and no video, juste a black background ).

It will save it under a different name from the final one, to ensure compatibility with our conversion software,into a temporary folder.  
> Temp\FFMPEG_compatible.mp4

Then our post-processing conversion software [FFMPEG](#FFMPEG) will take care of converting our file into .mp3, it is for this that a console appears for a few seconds so we end up with:
> Temp\FFMPEG_compatible.mp4  
> Temp\FFMPEG_compatible.mp3

We delete the file which ends with .mp4, and we rename the one that ends with .mp3, with the right file name (without special characters and with a suffix if necessary), our temp folder now look like this:
> Temp\YourAudioWithoutSpecialChracterSuffixe.mp3  

And finally we copy it to the place you choose.

## For video :
---
The application will download the best audio quality of your video, in the .mp4 format ( Which just contains the codecs / channels for the audio, and no video, juste a black background ).

It will save it under a different name from the final one, to ensure compatibility with our conversion software, into a temporary folder.  
> Temp\audio.mp4

After the application will download to see what video quality is obtainable :  
By default it will stop at 1080p, to save bandwidth, but you can change it in the code.  
If it does not find the 1080p quality it will take the highest available (below 1080p).  
Its, its gonna take some time, (again it depends on the size of the video and your internet connection (downward flow))  
Its going to be saved, in the temporary folder, under the name 'video.mp4', because yes it is an mp4 file, but without the audio channels, because youtube uses a processor call [DASH](#DASH) (see below).

So now we end up with 2 files in the temporary folder:
> Temp\audio.mp4  
> Temp\video.mp4

The post processing software, [FFMPEG](#FFMPEG),  will then copy the audio track ON the video and render it, and TADAM we have our FullHD 1080x1920 60fps video, here name is 'final.mp4'.
The temporay folder look like this :
> Temp\audio.mp4  
> Temp\video.mp4  
> Temp\final.mp4

So we delete audio.mp4, video.mp4 and rename final.mp4 with the right file name (without special characters and with a suffix if necessary) and now we have :
> Temp\YourVideoWithoutSpecialChracterSuffixe.mp4 

We copy that were you want it to be, and it done.

# CODECS_&_Formats

## Format output 

The application allows you to download videos in :
- Audio format (.mp3)
- Video format (.mp4)

## Audio CODECS
The codecs for the audio are [AAC mpga](https://en.wikipedia.org/wiki/Advanced_Audio_Coding) 

## Video CODECS 
- Flux 0 (video)

    The codecs for the video are [AV1](https://en.wikipedia.org/wiki/AV1), this codecs is supported by [VLC](https://www.videolan.org/vlc/) thanks to their decoder [DaV1d](https://www.videolan.org/projects/dav1d.html).  

    - You are watched by bill gate: 
        - For window 7:
            - Install the codec AV1 (use google)
            - Use [VLC](https://www.videolan.org/vlc/)
        - For window 10:
            - Install the codec AV1 on the microsoft store [Beta for AV1 video codec](https://www.microsoft.com/store/productId/9MVZQVXJBQ9V)
            - Use the godam [VLC](https://www.videolan.org/vlc/)

    - if you have an apple or a penguin as an OS :
        - Use [VLC](https://www.videolan.org/vlc/)
        - There are probably other options, but I don't have the money for a mac 
        and especially never will I use this horrible OS.
        - I have too little experience with penguin OS to talk about it, I'm sure if I say something wrong about it, they'll find me and beat me up with metal pipes.

- flux 1 (audio)
    - For the audio flux we use the same audio codec as quoted recently, [AAC mpga](https://en.wikipedia.org/wiki/Advanced_Audio_Coding) 

## Warning :
I am not an expert in codecs, and I have like 45min of reading on the internet so don't take me literally, you can always convert them to other codecs with better support, but as far as i have read, AV1 is the futur

# DASH
The youtubes videos come in different streams, some containing only the audio stream, other than the video stream and some both.  
This is because YouTube supports a streaming technique called [DASH](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP) known by the sweet name of *Dynamic Adaptive Streaming over HTTP*.  
It coexists with another technique, which is called [progressive download](https://en.wikipedia.org/wiki/Progressive_download).  
While [DASH](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP) specializes in high quality streams, [progressive download](https://en.wikipedia.org/wiki/Progressive_download) deals with lower quality streams, like 720p of below, this last technique contains both audio and video stream.  
For [DASH](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP), the quality is not limited, but we need to download each stream, audio and video, before merging them with post processing software (in our case, [FFMPEG](#FFMPEG)  
![DASH vs Progressive download](https://qph.fs.quoracdn.net/main-qimg-6af96fa067d9ae06d02834af4c9bf3bd)

# FFMPEG
Shamefully steal from their website :

[FFmpeg](https://www.ffmpeg.org) is the leading multimedia framework, able to decode, encode, transcode, mux, demux, stream, filter and play pretty much anything that humans and machines have created. It supports the most obscure ancient formats up to the cutting edge. No matter if they were designed by some standards committee, the community or a corporation. It is also highly portable: [FFmpeg](https://www.ffmpeg.org) compiles, runs, and passes our testing infrastructure FATE across Linux, Mac OS X, Microsoft Windows, the BSDs, Solaris, etc. under a wide variety of build environments, machine architectures, and configurations.

To download [FFMPEG](https://www.ffmpeg.org) : [Is here](https://www.ffmpeg.org/download.html) and its a blessing from the lord, use it.  
On this project, we use it to convert .mp4 to .mp3 and to assemble 2 tracks (one withe only sound and one with only video) : see [Download](#Download)   
See [License](#License) for more information about thems.

# PyQt5
It is a module which allows you to handle the high level API [Qt](https://en.wikipedia.org/wiki/Qt_(software)), written in c ++ with python, thanks to this, we can make rather pretty graphical interfaces compared to Tkinter.  
See [License](#License) for more information about they.

# Pytube
Then Pytube, alalala~ the cornerstone, the foundation, of my application : it's a python module that takes care of fetching youtube videos.He took care of downloading the video, choosing the quality and all.  
We can find the official depot of this API masterpiece like allway on [PyPi](https://pypi.org/project/pytube/).  
Theirs [documentation](https://pytube.io/en/latest/index.html) is incredibly incredible and help me a lot.  
See [License](#License) for more information about they.

# License

## Project 

My project is under the [Gpl v3 license](https://www.gnu.org/licenses/gpl-3.0.en.html). You can therefore reuse it but in the terms of the liscense 

## Dependancy 

- **PyQt5** : This module is under the liscense [GPL v3](https://www.gnu.org/licenses/quick-guide-gplv3.en.html) (see below in the section for licenses)  
Their website is [here](https://www.riverbankcomputing.com/software/pyqt/). And the code i have used is stored [here](https://pypi.org/project/PyQt5/) as requested in the legal notice.Since I haven't touched it (to the source code of PyQt) I give the link on the python module manager, PyPi.

- **FFmpeg** : This software uses code of [FFmpeg](http://ffmpeg.org) licensed under the [GPL v3](https://www.gnu.org/licenses/quick-guide-gplv3.en.html) (see below in the part for the licenses the source from my build can be downloaded [here](https://github.com/FFmpeg/FFmpeg/commit/f68ab9de4e).  
The build setting and its readme is located into ```FFmpeg\LICENSE.md``` AND ```FFmpeg\README.txt```

- **Pytube** : Pytube uses the [unlicense](https://unlicense.org), (it is limited if the program is not in the public domain) and it accords with GPL v3. so it's a crushing victory

## WARNING

I am not a lawyer, i just know how to use google (yes i am a programmer lmao).  
I'm not an expert, if you have any questions or anything else (eg I don't respect your liscense) let me know. (I have a hard time with FFMPEG D: )

# source 
No yet

# Contributeur 
@nanimo_hakai(IG) for the name of the app