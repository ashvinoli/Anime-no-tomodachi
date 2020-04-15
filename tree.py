import requests
from bs4 import BeautifulSoup
import re
import webbrowser
import os
import subprocess
import time

global_url = "https://www10.gogoanime.io/"
global_head_url = "https://www10.gogoanime.io/category/"
headers = {"Referrer Policy":"unsafe-url",\
                  "Origin":"https://vidstreaming.io",\
                  "Referer":"https://vidstreaming.io/",\
                  "Sec-Fetch-Mode":"cors",\
                  "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
messenger = ""

default_mode = None
log_file = open("error_log.txt","w")
log_file.close()

def open_log_file():
     global log_file
     log_file = open("error_log.txt","a")
     
def close_log_file():
     global log_file
     log_file.close()

def write_to_log_file(header,content):
     global log_file
     open_log_file()
     log_file.write(header)
     log_file.write(content)
     log_file.write("\n\n\n\n")
     close_log_file()
     
def write_to_file(link):
     my_link_opened =BeautifulSoup(requests.get(link).text,"html.parser")
     iframes = my_link_opened.findAll("iframe")
     if len(iframes) != 0:
        my_iframe = iframes[0]
        my_iframe = my_iframe.get("src")
        if my_iframe.find(link)== -1:
            final_link = link + my_iframe
        else:
            final_link = my_iframe
        file = open("master_link_file.txt","a")
        file.write(final_link + "\n")
        file.close()
        return final_link

def play_video_in_vlc(video_link):
     global messenger
     subprocess.run(["vlc",video_link])

     
def check_for_ways_to_play(video_link):
     if "redirector" in video_link:
          play_video_in_vlc(video_link)
     
     
def make_video_url_ready(highlighted_episode):
     global global_url
     url = global_url + "".join(highlighted_episode.split("\n"))
     php_url = "http://" + write_to_file(url).split("//")[-1]
     return  php_url
     
def get_anime_list(url):
    global global_url
    all_anime = []
    my_main_page = BeautifulSoup(requests.get(url).text,"html.parser")
    all_devs = my_main_page.findAll("div",{"class":"anime_list_body"})
    for dev in all_devs:
        anime_list = dev.findAll("a")
        for anime in anime_list:
            all_anime.append(global_url+anime.get("href"))
    return all_anime

def get_ALL_anime_list():
    global global_url
    url = global_url+"anime-list.html?page="
    my_dict = []
    for i in range(1,55):
        temp_dict = get_anime_list(url+str(i))
        my_dict = my_dict + temp_dict
    return my_dict

def get_all_episodes(url):
    global global_url
    episode_url_list = []
    largest = num_of_episodes(url)
    for i in range(1,largest+1):
        episode_url_list.append(global_url+url.split("/")[-1]+"-episode-"+str(i))
    return episode_url_list

def num_of_episodes(url):
    global global_url
    my_main_page = BeautifulSoup(requests.get(url).text,"html.parser")
    my_list = my_main_page.findAll("ul",{"id":"episode_page"})[0]
    my_lists = my_list.findAll("a")
    largest = 0
    for item in my_lists:
        num = int(item.get("ep_end"))
        if num > largest:
            largest = num
    return largest

def get_single_episode(url,episode_num):
    global global_url
    episode_url = global_url+url.split("/")[-1]+"-episode-"
    largest = num_of_episodes(url)
    ret_file = []
    if episode_num > largest:
        ret_file.append("Sorry, the episode is not yet available!")
    else:
        ret_file.append(episode_url+str(episode_num))
    return ret_file
       
        
def prepare_master_file():
    all_anime = get_ALL_anime_list()
    for anime in all_anime:
        print("ANIME:"+anime)
        all_episodes = get_all_episodes(anime)
        for episode in all_episodes:
            print("EPISODE:"+episode)
            write_to_file(episode)

def save_anime_list():
     all_anime = get_ALL_anime_list()
     temp_file = open("all_animes.txt","w")
     for anime in all_anime:
          temp_file.write(anime+ "\n")
     temp_file.close()

def get_playlist_m3u8(end_url):
     #returns the main m3u8
     my_main_page = BeautifulSoup(requests.get(end_url).text,"html.parser")
     try:
          m3u8 = my_main_page.findAll("script")[3].text.split(";")[0].split("=")[-1].split("'")[1]
     except:
          m3u8 = re.search("[\'].*?[\']",my_main_page.findAll("script")[3].text.split(";")[3]).group(0).split("'")[1]
     write_to_log_file("Playlist m3u8 for "+end_url+":\n",m3u8)
     return m3u8

def get_child_m3u8(playlist_m3u8):
     #returns the qualities available
     head_url = playlist_m3u8.split("/")[2]
     head_url = "https://" + head_url
     global headers
     m3u8 = []
     if head_url == "https://hls10x.cdnfile.info":
          headers_new = {  "Origin":"https://vidstreaming.io",\
                       "Referrer":"https://vidstreaming.io/",\
                       "Referrer Policy":"origin",\
                       "Sec-Fetch-Mode":"cors",\
                       "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
          temp_m3 = requests.get(playlist_m3u8,headers = headers_new)
     elif head_url=="https://hls11x.cdnfile.info":
          temp_m3 = requests.get(playlist_m3u8)
          #Parse the m3u8
          my_chunk = "/".join(playlist_m3u8.split("/")[:-1])
          lines = temp_m3.text.split("\n")
     else:
          temp_m3 = requests.get(playlist_m3u8,headers = headers)
          #print(temp_m3.text)
          #Parse the m3u8 and take bundle the qualities available with the download link
          lines = temp_m3.text.split("\n")
          for i in range(len(lines)):
               resolution = []
               if re.search("\d+x\d+",lines[i]):
                    resolution.append(re.search("\d+x\d+",lines[i]).group(0))
                    resolution.append(head_url+lines[i+1])
                    m3u8.append(resolution)
     for _ in m3u8:
          write_to_log_file("Child_m3u8:\n",'\n'.join(_))
          
     return m3u8

def provide_video_chunks(video_m3u8):
     #returns the video chunks for the quality selected
     global headers
     #print(video_m3u8)
     chunks = []
     head_url = video_m3u8.split("/")[2]
     head_url = "https://" + head_url
     temp_m3 = requests.get(video_m3u8,headers=headers)
     #print(temp_m3.text)
     all_lines = temp_m3.text.split("\n")
     bits_extracted_prev = ""
     #Parse the video_m3u8 file, to extract chunks and prevent repetition
     for line in all_lines:
        if re.match("^/",line):
             bits_extracted_new = line.split(".")[-2].split("-")[-1]
             if bits_extracted_new != bits_extracted_prev:
                  chunks.append(head_url+line)
                  bits_extracted_prev = bits_extracted_new
     
     return chunks

def provide_video_chunks_new(video_m3u8):
     #returns the video chunks for the quality selected
     global headers
     chunks = []
     head_url = video_m3u8.split("/")[2]
     head_url = "https://" + head_url
     temp_m3 = requests.get(video_m3u8,headers=headers)
     all_lines = temp_m3.text.split("\n")
     bits_extracted_prev = ""
     #Parse the video_m3u8 file, to extract chunks and prevent repetition
     for line in all_lines:
        if re.match("^https",line):
             chunks.append(line)
     return chunks
                  
def download_chunk(url):
     global headers
     return requests.get(url,headers=headers).content

def quality_selection(my_playlist):
     #This function prompts the user to select quality
     global default_mode
     index = 1
     length = len(my_playlist)
     for _ in my_playlist:
          print(str(index) + "----->"+ _[0])
          index += 1
     while True:
          resp = input("Choose the quality of video:")
          if resp.isnumeric() and int(resp) <= length and int(resp) >= 1:
               my_quality_video = provide_video_chunks(my_playlist[int(resp)-1][1])
               if len(my_quality_video) == 0:
                    my_quality_video = provide_video_chunks_new(my_playlist[int(resp)-1][1])
               ans = input("Do you want to keep it as default quality for the next videos? Type y/n:")
               if ans == "y":
                    default_mode = my_playlist[int(resp)-1][0]
               stream_video(my_quality_video)
               break
          else:
               resp = input("Bad quality!!!!!! Re-enter quality y/n?")
               if resp != "y":
                    break
    
def watch_video(end_url):
    global default_mode
    my_playlist = get_child_m3u8(get_playlist_m3u8(end_url))
    matched = False
    length = len(my_playlist)
    if length != 0:
        if default_mode == None:
            quality_selection(my_playlist)
        else:
            for _ in my_playlist:
                if _[0] == default_mode:
                    my_quality_video = provide_video_chunks(_[1])
                    if len(my_quality_video) == 0:
                         my_quality_video = provide_video_chunks_new(_[1])
                    stream_video(my_quality_video)
                    matched = True
                    break
            if not matched:
                default_mode = None
                print("Sorry, your default quality is unavailable for this video. So please select quality again.")
                quality_selection(my_playlist)         
    else:
        print("Sorry, the video you requested is currently not available! Will fix this problem soon!") #This problem is caused by the alternate hls10x site
                    
                    
def stream_video(video_chunks):
     if os.path.exists("temp_vid.mp4"):
        os.remove("temp_vid.mp4")
     index = 0
     vlc_opened = False
     my_program = None
     for chunk in video_chunks:
          #print(chunk)
          with requests.get(chunk, stream=True,headers = headers) as r:
               r.raise_for_status()
               for piece in r.iter_content(chunk_size=8192):
                    if my_program != None:
                         poll = my_program.poll()
                         if poll != None: #if poll is none then my program is still running
                              if os.path.exists("temp_vid.mp4"):
                                    os.remove("temp_vid.mp4")
                              return
                    f = open("temp_vid.mp4","ab")
                    if piece:
                         f.write(piece)
                         f.close()
                         if not vlc_opened:
                              my_program = subprocess.Popen(["vlc","temp_vid.mp4"])
                              vlc_opened = True
def format_search_query(search_query):
     formatted_anime_name  = "-".join(search_query.split(" "))
     return formatted_anime_name

def search_for_anime(formatted_anime_name):
     anime_list_file = open("all_animes.txt","r")
     matched_items = [line for line in anime_list_file if formatted_anime_name in line]
     return matched_items

                              
def command_line_watch():
     while True:
         os.system("cls")
         print("NOTE: IF YOU WANT TO SKIP ANY TYPING OR QUESTION JUST PRESS \"ENTER\" KEY.\nBUT DONOT PRESS ENTER FOR THIS FIRST QUESTION!\n")
         anime_name = input("Please enter the anime name (example:one-piece). Mind the dash(-) sign:")
         match_dict=[]
         f=open("all_animes.txt","r")
         found = False
         for line in f:
             if anime_name in line:
                 match_dict.append(line)
                 found = True
         f.close()
         if found:
             for i in range(len(match_dict)):
                 print(str(i+1) + "--->" + match_dict[i])
             while True:
                  selection = input("Please select your option among the SEARCHED RESULTS:")
                  if selection.isnumeric():
                       selection = int(selection)-1
                       if selection > len(match_dict)-1 or selection < 0:
                            resp = input("Your selection is not available! Make reselection? Type y/n:")
                            if resp != "y":
                                 break
                       else:
                            num = str(num_of_episodes(match_dict[selection]))
                            while True:
                                choice = input("There are "  + num + " episodes for "+ match_dict[selection] +"Please type the episode number:")
                                if choice.isnumeric():
                                     choice = int(choice)
                                     if choice > int(num) or choice < 1:
                                          print("Sorry, the episode you requested is not available yet!")
                                          resp = input("Want to see another episode? Type y/n:")
                                          if resp != "y":
                                               break
                                     else:
                                          while True:
                                               if choice > int(num):
                                                     print("Sorry, we are now out of episodes!")
                                                     break
                                               my_episode = get_single_episode(match_dict[selection].rstrip(),choice)
                                               my_link = write_to_file(my_episode[0])
                                               final_link = my_link.split("//")[-1]
                                               final_link = "https://"+final_link
                                               #print(final_link)
                                               watch_video(final_link)
                                               #print(final_link)
                                               #webbrowser.open_new(final_link)
                                               resp = input("Want to watch next? Type y/n:")
                                               if resp != 'y':
                                                   break
                                               else:
                                                   choice += 1
                                else:
                                      resp=input("Invalid option input. Reinput? Type y/n:")
                                      if resp != "y":
                                           break
                                     
                  else:
                       resp=input("Invalid option input. Reinput? Type y/n:")
                       if resp != "y":
                            break
                                 
         else:
             print("No match found! Try researching for shorter string")

         retry = input("Research for another anime? y/n:")
         if retry != "y":
                  break
     
if __name__ == "__main__":            
     try:
          save_anime_list()
          print("The anime list has been updated successfully!")
     except:
          print("Some error occured!!!! I have no idea what type, perhaps you might want to see your internet connection")
    
