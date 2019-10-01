import requests
from bs4 import BeautifulSoup
import re
import webbrowser
import os
import subprocess
import time

global_url = "https://www9.gogoanime.io/"
headers = {"Referrer Policy":"unsafe-url",\
                  "Origin":"https://vidstreaming.io",\
                  "Referer":"https://vidstreaming.io/",\
                  "Sec-Fetch-Mode":"cors",\
                  "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}

default_mode = None

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
    for i in range(1,52):
        temp_dict = get_anime_list(url+str(i))
        my_dict = my_dict + temp_dict
    return my_dict

def get_all_episodes(url):
    global global_url
    largest = num_of_episodes(url)
    for i in range(1,largest+1):
        episode_url_list.append(get_single_episode(url,i)[0])
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
    for anime in all_anime:
        temp_file = open("all_animes.txt","a")
        temp_file.write(anime+ "\n")
        temp_file.close()

def get_playlist_m3u8(end_url):
     #returns the main m3u8
     my_main_page = BeautifulSoup(requests.get(end_url).text,"html.parser")
     try:
          m3u8 = my_main_page.findAll("script")[3].text.split(";")[0].split("=")[-1].split("'")[1]
     except:
          m3u8 = re.search("[\'].*?[\']",my_main_page.findAll("script")[3].text.split(";")[3]).group(0).split("'")[1]
     return m3u8

def get_child_m3u8(playlist_m3u8):
     #returns the qualities available
     head_url = playlist_m3u8.split("/")[2]
     head_url = "https://" + head_url
     global headers
     if head_url == "https://hls10x.cdnfile.info":
          headers_new = {  "Origin":"https://vidstreaming.io",\
                       "Referrer":"https://vidstreaming.io/",\
                       "Referrer Policy":"origin",\
                       "Sec-Fetch-Mode":"cors",\
                       "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
          temp_m3 = requests.get(playlist_m3u8,headers = headers_new)
     else:
          temp_m3 = requests.get(playlist_m3u8,headers = headers)
     m3u8 = []
     #print(temp_m3.text)
     lines = temp_m3.text.split("\n")
     for i in range(len(lines)):
          resolution = []
          if re.search("\d+x\d+",lines[i]):
               resolution.append(re.search("\d+x\d+",lines[i]).group(0))
               resolution.append(head_url+lines[i+1])
               m3u8.append(resolution)      
     return m3u8

def provide_video_chunks(video_m3u8):
     #returns the video chunks for the quality selected
     global headers
     chunks = []
     head_url = video_m3u8.split("/")[2]
     head_url = "https://" + head_url
     temp_m3 = requests.get(video_m3u8,headers=headers)
     all_lines = temp_m3.text.split("\n")
     bits_extracted_prev = ""
     for line in all_lines:
        if re.match("^/",line):
             bits_extracted_new = line.split(".")[-2].split("-")[-1]
             if bits_extracted_new != bits_extracted_prev:
                  chunks.append(head_url+line)
                  bits_extracted_prev = bits_extracted_new
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
                                               print(final_link)
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
     # connection = internet_on()
     # if connection:
     #      command_line_watch()
     #      if os.path.exists("temp_vid.mp4"):
     #           os.remove("temp_vid.mp4")
     # else:
     #      print("Please Check your internet connection and try again!")
                
    try:
        command_line_watch()
    except:
        print("Some error occured!!!! I have no idea what type, perhaps you might want to see your internet connection")
    
