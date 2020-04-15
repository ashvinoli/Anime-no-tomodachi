# Table of Contents
- [Anime-no-tomodachi](#anime-no-tomodachi)
  * [Usage](#usage)
  * [Special Note](#special-note)
  * [Repeat first 4 commands](#repeat-first-4-commands)
  * [No-Interruption-Mode](#no-interruption-mode)
  * [Adding new anime to the list](#adding-new-anime-to-the-list)

## Anime-no-tomodachi
Your Anime Friend. It scrapes links from "gogoanime" site and provides an easy way to view animes in vlc media player. Downloading option is also available. GUI currently only allows watching animes. Again put VLC in path to be able to watch animes in VLC.

## Usage
Please use python 3.7 or higher if available. Install required libraries.
* To watch video:
Add vlc to PATH and-
```
python Anime-no-tomodachi-main.py
```
* To download video:
Just type the following
```
python download_module.py
```

## Special Note
During VLC play, the play might end after a few seconds, that is because the download is slow. Press the play button in VLC again to view the updated video. You might experience same problem while trying to forward or skip part of video. Again you will reach the end of downloaded file chunk, so wait and again click the play button. And sometimes, certain errors might occur which will go away just by re-starting the program.

## Repeat first 4 commands
To repeat the first 4 commands of last session you ran, for example: you might have said "y" to interruption question, "monster" to anime name, "5" to selection number and "1-5" to episode range, if you simply want to repeat the same sequence, you needn't retype everything simply:
```
python download_module.py -r
```
If you want you can edit the repeat.txt to simplify things. Do not enter invalid input in the text file, else the program will go into infinite loop. For example, if you open the "repeat.txt" file and manually enter "asdfasddafa" in the second row which would take the name of anime, the program will run infinitely displaying the error message. This is because, there is automatic redirection of input taken of file to the variable, so mind it before you make edits to the "repeat.txt" file and running the program with "-r" handle.
## No-Interruption-Mode
Imagine you sleep after putting a range say 2-200 for episodes to download. The program will ask for quality for episode 2, and if you set the quality to default, no further queries about the quality will be made. What if episode 150 didn't have the default quality you selected? If no-interruption-mode is not turned on, the program expects user input, asking for another quality the the video 150 has. Do you want that after you have slept? Wake up expecting all 200 downloaded episodes, but alas the program is stuck at 150. To remedy this I have added the No-interruption-mode, in this mode, even if the episode doesn't contain the default quality, it will download the quality it has. With this ammendment, you can now have a sound sleep after providing the program with a range of 2-200.


## Adding new anime to the list
* To update entire anime list,
```
python tree.py
```
This will take upto 1-2 minutes. Addition of single anime can be done as follows.
"https://www9.gogoanime.io//category/boku-no-hero-academia-4th-season" is not in the list. If you search boku-no-hero this option won't show up, because it was added after I made the list file. So simply copy and paste it at the end of "all_animes.txt" file and you are good to go. That was a simple example. If you do no find anime in the search, try japanese name, and if it fails even then then search it in gogoanime, get the link as above (You do not need "//", "/" works fine), and paste it at the end of file. Simple!
