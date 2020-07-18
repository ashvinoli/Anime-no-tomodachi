# Table of Contents
- [Anime-no-tomodachi](#anime-no-tomodachi)
  * [Usage](#usage)
  * [Adding new anime to the list](#adding-new-anime-to-the-list)

## Anime-no-tomodachi
Your Anime Friend. It scrapes links from "gogoanime" site and provides an easy way to view animes in vlc media player. Downloading option is also available. GUI features downloading and watching anime. In windows, to download an anime you have to install Internet Download Manager and put "idman.exe" in PATH system variable.In linux "Wget" is used which is installed by default in most destros, if not install it.To watch in VLC you again have to put "vlc.exe" in the system path. Remember that when I talk about "path" its good old windows I am talking about.

## Usage
Please use python 3.7 or higher if available. Install required libraries as follows:
```
pip install -r requirements.txt
```
* Run the program as follows.
```
python Anime-no-tomodachi-main.py
```
Everything is in the screen, do as you please. Watch or download.


## Adding new anime to the list
* To update entire anime list,
```
python tree.py
```
This will take upto 1-2 minutes. Addition of single anime can be done as follows.
Suppose "https://www9.gogoanime.io//category/boku-no-hero-academia-4th-season" is not in the list. If you search boku-no-hero this option won't show up, because it was added after I made the list file. So simply copy and paste it at the end of "all_animes.txt" file and you are good to go. That was a simple example. If you do no find anime in the search, try japanese name, and if it fails even then then search it in gogoanime, get the link as above (You do not need "//", "/" works fine), and paste it at the end of file. Simple!
