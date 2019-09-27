import requests
from bs4 import BeautifulSoup
import threading
import re

global_url = "https://www9.gogoanime.io/"
class crawler:
    def __init__(self,head_link,link,critical_level,parent = None,level=0,threads=[],children=[]):
        self.parent = parent
        self.level = level
        self.threads = threads
        self.children = children
        self.link = link
        self.head_link = head_link
        self.critical_level =critical_level
        
    def navigate(self):
        global all_anime
        my_link_opened =BeautifulSoup(requests.get(self.link).text,"html.parser")
        print("SELF LINK:" + "*******"+ self.link+"SElf level"+str(self.level))
        if self.level < self.critical_level:
            if re.search("\d+$",self.link):
                write_to_file(self.link)
            else:
                all_links = my_link_opened.findAll("a")
                for my_link in all_links:
                    page_link = my_link.get("href")
                    if page_link != None:
                        if page_link.find(self.head_link)== -1:
                            page_link = self.head_link + page_link
                        if self.parent == None:
                            if page_link in all_anime:
                                child = crawler(parent=self,level=self.level+1,head_link = self.head_link,link = page_link,critical_level = self.critical_level)
                                self.children.append(child)
                        else:
                            fragment = self.link.split("/")[-1]
                            if fragment in page_link:
                                child = crawler(parent=self,level=self.level+1,head_link = self.head_link,link = page_link,critical_level = self.critical_level)
                                self.children.append(child)
                for child in self.children:
                    my_thread = threading.Thread(target=child.navigate,args=())
                    self.threads.append(my_thread)
                for thread in self.threads:
                    thread.start()
                    thread.join()


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
    
       
        
def prepare_master_file():
    all_anime = get_ALL_anime_list()
    for anime in all_anime:
        print("ANIME:"+anime)
        all_episodes = get_all_episodes(anime)
        for episode in all_episodes:
            print("EPISODE:"+episode)
            write_to_file(episode)
            
            
            
prepare_master_file()
