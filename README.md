# Anime-no-tomodachi
Your Anime Friend. It scrapes links from "gogoanime" site and provides an easy way to view animes in vlc media player. Downloading option is also available. Everything is command line now. GUI will be made in future.
## Special Note
During VLC play, the play might end after a few seconds, that is because the download is slow. Press the play button in VLC again to view the updated video. You might experience same problem while trying to forward or skip part of video. Again you will reach the end of downloaded file chunk, so wait and again click the play button. And sometimes, certain errors might occur which will go away just by re-starting the program.
## Usage
Please used python 3.7 or higher if available. Install required libraries.
To watch video:
* Add vlc to PATH and-
```
python tree.py
```
To download video:
* Just type the following
```
python download_module.py
```

## No-Interruption-Mode
Imagine you sleep after putting a range say 2-200 for episodes to download. The program will ask for quality for episode 2, and if you set the quality to default, no further queries about the quality will be made. What if episode 150 didn't have the default quality you selected? If no-interruption-mode is not turned on, the program expects user input, asking for another quality the the video 150 has. Do you want that after you have slept? Wake up expecting all 200 downloaded episodes, but alas the program is stuck at 150. To remedy this I have added the No-interruption-mode, in this mode, even if the episode doesn't contain the default quality, it will download the quality it has. With this ammendment, you can now have a sound sleep after providing the program with a range of 2-200.

## Common Error messages
```
PermissionError: [Errno 13] Permission denied: 'temp_vid.mp4'
```
This error occurs because VLC media player started slower in your system. Restart the program and it will disappear as VLC will only start slowly at the first instance. I will fix it as soon as possible 
