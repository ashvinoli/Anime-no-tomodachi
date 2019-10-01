# Anime-no-tomodachi
Your Anime Friend. It scrapes links from "gogoanime" site and provides an easy way to view animes in vlc media player. Right now it can play but not downlaod (technically it plays by downloading, but deletes them). I will add downloading module and a nice GUI if I feel like it.
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
## Common Error messages
```
PermissionError: [Errno 13] Permission denied: 'temp_vid.mp4'
```
This error occurs because VLC media player started slower in your system. Restart the program and it will disappear as VLC will only start slowly at the first instance. I will fix it as soon as possible 
