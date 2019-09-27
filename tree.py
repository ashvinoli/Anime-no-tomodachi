import requests
from bs4 import BeautifulSoup

def get_anime_list(url):
    all_anime = []
    my_main_page = BeautifulSoup(requests.get(url).text,"html.parser")
    all_devs = my_main_page.findAll("nav",{"class":"menu_series cron"})
    for dev in all_devs:
        anime_list = dev.findAll("a")
        for anime in anime_list:
            all_anime.append(url+anime.get("href"))

    return all_anime

my_anime = get_anime_list("https://www9.gogoanime.io/")
for a in my_anime:
    print(a)
        
    
    
    
    
    
