import requests
from bs4 import BeautifulSoup
import threading
import re
import webbrowser

global_url = "https://www9.gogoanime.io/"

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
    my_main_page = BeautifulSoup(requests.get(url).text,"html.parser")
    episode_url = global_url+url.split("/")[-1]+"-episode-"
    my_list = my_main_page.findAll("ul",{"id":"episode_page"})[0]
    my_lists = my_list.findAll("a")
    episode_url_list = []
    largest = 0
    for item in my_lists:
        num = int(item.get("ep_end"))
        if num > largest:
            largest = num
    for i in range(1,largest+1):
        temp_url = episode_url + str(i)
        episode_url_list.append(temp_url)
    return episode_url_list

def num_of_episodes(url):
    global global_url
    my_main_page = BeautifulSoup(requests.get(url).text,"html.parser")
    episode_url = global_url+url.split("/")[-1]+"-episode-"
    my_list = my_main_page.findAll("ul",{"id":"episode_page"})[0]
    my_lists = my_list.findAll("a")
    episode_url_list = []
    largest = 0
    for item in my_lists:
        num = int(item.get("ep_end"))
        if num > largest:
            largest = num
    return largest

def get_single_episode(url,episode_num):
    global global_url
    my_main_page = BeautifulSoup(requests.get(url).text,"html.parser")
    episode_url = global_url+url.split("/")[-1]+"-episode-"
    my_list = my_main_page.findAll("ul",{"id":"episode_page"})[0]
    my_lists = my_list.findAll("a")
    largest = 0
    ret_file = []
    for item in my_lists:
        num = int(item.get("ep_end"))
        if num > largest:
            largest = num
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
           
        
def command_line_watch():
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
        selection = int(input("Please select your option:"))-1
        num = str(num_of_episodes(match_dict[selection]))
        choice = int(input("There are "  + num + " episodes for "+ match_dict[selection] +"Please type the episode number:"))
        while True:
            my_episode = get_single_episode(match_dict[selection].rstrip(),choice)
            my_link = write_to_file(my_episode[0])
            final_link = my_link.split("//")[-1]
            print(final_link)
            webbrowser.open("https://"+final_link)
            resp = input("Want to watch next? Type y/n:")
            if resp == 'n':
                break
            else:
                choice += 1
                if choice > int(num):
                    break
            
    else:
        print("No match found! Try researching for shorter string")
    
    
    
        
if __name__ == "__main__":
    command_line_watch()
