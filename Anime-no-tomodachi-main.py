from tkinter import *
from tkinter import ttk
from windows_class import *
import threading
import tree
import webbrowser
import os
import subprocess
from datetime import date

class window_main(windows):
    def __init__(self,title="My window",geometry="800x800"):
        self.current_video_url=""
        self.current_php_url = ""
        self.episodes_list_length = 0
        self.anime_link_buffer = {}
        super().__init__(title,geometry)

    def update_anime_list(self):
        last_updated = "Last_Updated.txt"
        if os.path.exists(last_updated):
            with open(last_updated,"r") as f:
                last_date = f.readline().rstrip().split("-")
                last_date = [int(i) for i in last_date]
                year,month,day = last_date
                last_date = date(year,month,day)
                today = date.today()
                gap = today-last_date
                
                #update in five days
                if gap.days > 5:
                    tree.save_anime_list()
            f = open(last_updated,"w")
            f.write(today.__str__())
            f.close()
        else:           
            tree.save_anime_list()
            today = date.today()
            f = open(last_updated,"w")
            f.write(today.__str__())
            f.close()
        
    def define_frames(self):
        self.matched_frame = LabelFrame(self.window,text = "Matched Results",padx=5,pady=2)
        self.episodes_list_frame = LabelFrame(self.window,text = "Episodes List",padx = 5,pady=2)
        self.buttons_bundle_frame = LabelFrame(self.window,text = "Download/Watch",padx=5,pady=5)
        self.start_end_frame = LabelFrame(self.buttons_bundle_frame,padx=2)
        self.resume_anime_frame = LabelFrame(self.window,text = "Resume Watching",padx=5,pady=5)

        #Run update routine after frames are packed
        self.threads["Update_anime"] = threading.Thread(target = self.update_anime_list)
        self.threads["Update_anime"].start()
  
    def pack_frames(self):
        self.matched_frame.grid(row=2,column=1)
        self.episodes_list_frame.grid(row=2,column=2)
        self.buttons_bundle_frame.grid(row=2,column=3,sticky=NW)
        self.resume_anime_frame.grid(row=5,column=1,columnspan = 4,sticky =W)
        self.start_end_frame.pack()

        
    def define_combo_boxes(self):
        animes = self.get_watched_animes()
        self.my_anime_list_combo = ttk.Combobox(self.resume_anime_frame,width = 90,values = sorted(animes))

        #put last watched anime in the combo box
        if len(animes)!=0:
            self.my_anime_list_combo.set(animes[-1])
            
    def get_watched_animes(self):
        if os.path.exists("Anime_progress.txt"):
            with open("Anime_progress.txt","r") as f:
                all_animes = [i.strip() for i in f if i.strip()!=""]
        else:
            file = open("Anime_progress.txt","w")
            file.close()
            all_animes = []      
        return all_animes
    
    def pack_combo_boxes(self):
        self.my_anime_list_combo.grid(row=1,column=1)
        
    def define_labels(self):
        self.label_search_for_anime = Label(self.window,text = "Search for Anime:")
        self.label_TO = Label(self.start_end_frame,text = "To")
        self.label_status = Label(self.buttons_bundle_frame,text ="No Work In Progress." ,fg="green")
        self.label_download_status = Label(self.buttons_bundle_frame,text ="No Download In Progress." ,fg="red")
        self.label_download_status["wraplength"] = 200
        self.label_status["wraplength"] = 200
        
    def pack_labels(self):
        self.label_search_for_anime.grid(row = 1,column=1,sticky=E)
        self.label_TO.grid(row=1,column=2)
        self.label_status.pack()
        self.label_download_status.pack()
        
    def define_buttons(self):
        width = 27
        self.download_selected_episode_button = Button(self.buttons_bundle_frame,text = "Download Selected Episode",width = width,command = self.download_episode_idman_buffer)
        self.download_selected_episode_button["state"]="disabled"
        self.watch_in_browser_button = Button(self.window,text = "Watch In Browser",width=width,command = self.watch_in_browser_buffer)
        self.watch_in_browser_button["state"] = "disabled"
        self.watch_in_vlc_button = Button(self.window,text = "Watch In VLC",width=width,command = self.watch_in_vlc_buffer)
        self.watch_in_vlc_button["state"] = "disabled"
        self.download_all_episodes_button = Button(self.buttons_bundle_frame,text = "Download All Episodes",width = width,command =lambda: self.download_range_buffer(True))
        self.download_all_episodes_button["state"] = "disabled"
        self.download_range_button = Button(self.start_end_frame,text = "Download Range",command = self.download_range_buffer)
        self.download_range_button["state"] = "disabled"
        self.previous_button = Button(self.resume_anime_frame,text = "Previous",width = width-20,command = lambda:self.previous_next_episode(-1))
        self.next_button = Button(self.resume_anime_frame,text = "Next",width = width-20,command =lambda:self.previous_next_episode(1))
        self.resume_button = Button(self.resume_anime_frame,text = "Resume",width = width-20,command =lambda:self.previous_next_episode(0))
    def pack_buttons(self):
        self.download_selected_episode_button.pack()
        self.download_all_episodes_button.pack()
        self.watch_in_browser_button.grid(row=3,column=3)
        self.watch_in_vlc_button.grid(row=4,column=3)
        self.download_range_button.grid(row=1,column=4)
        self.previous_button.grid(row=1,column=2)
        self.resume_button.grid(row=1,column=3)
        self.next_button.grid(row=1,column=4)
        
    def define_entries(self):
        self.anime_entry = Entry(self.window,width=82)
        self.anime_entry.focus_set()
        self.video_link_entry = Entry(self.window,width=90)
        self.start_episode_number_entry = Entry(self.start_end_frame,width=5)
        self.end_episode_number_entry = Entry(self.start_end_frame,width=5)
        self.php_link_entry = Entry(self.window,width=90)
        
    def pack_entries(self):
        self.anime_entry.grid(row=1,column=2,columnspan=2,sticky=EW)
        self.start_episode_number_entry.grid(row=1,column=1,sticky=W)
        self.end_episode_number_entry.grid(row=1,column=3,sticky=E)
        self.php_link_entry.grid(row=3,column=1,columnspan=2,sticky=EW)
        self.video_link_entry.grid(row=4,column=1,columnspan=2,sticky=EW)
         
    def define_list_boxes(self):
        self.matched_list = Listbox(self.matched_frame,width = 40,selectmode=SINGLE)
        self.episodes_list = Listbox(self.episodes_list_frame,width = 60,selectmode=SINGLE)
        
    def pack_list_boxes(self):
        self.matched_list.grid(row=1,column=1)
        self.episodes_list.grid(row=1,column=1)


    def define_scroll_bars(self):
        self.scroll_bar_for_anime_list =Scrollbar(self.matched_frame, orient = "vertical")
        self.scroll_bar_for_episode_list = Scrollbar(self.episodes_list_frame,orient = "vertical")
        
    def pack_scroll_bars(self):
        self.scroll_bar_for_anime_list.grid(row=1,column=2,sticky = "ns")
        self.scroll_bar_for_episode_list.grid(row=1,column=2,sticky = "ns")
    #Functions assignement And Bindings
    def assign_functions(self):
        #To send arguments with the calling funciton use Lambda. It will send two arguments. First is self and the second and others are give by you
        #In the case of function below two arguments are passed even though it looks zero arguments were passed. "Self" and "Event" were passed in case below. The Enter below signifies mouse entering the region of button
        self.matched_list.bind("<ButtonRelease-1>",self.fire_list_box_selected_buffer)
        self.matched_list.bind("<Return>",self.fire_list_box_selected)
        self.anime_entry.bind("<Return>",self.search_button_clicked)
        self.episodes_list.bind("<ButtonRelease-1>",self.fire_episodes_list_box_selected_buffer)
        self.matched_list.config(yscrollcommand=self.scroll_bar_for_anime_list.set)
        self.scroll_bar_for_anime_list.config(command=self.matched_list.yview)
        self.episodes_list.config(yscrollcommand=self.scroll_bar_for_episode_list.set)
        self.scroll_bar_for_episode_list.config(command=self.episodes_list.yview)
        self.my_anime_list_combo.bind("<<ComboboxSelected>>", self.fire_my_anime_list_combo_selected)
    #All associated functions

    def fire_my_anime_list_combo_selected(self,event):
        current_value = self.my_anime_list_combo.get()
        self.threads["Resume_Watching"] = threading.Thread(target = self.fire_episodes_list_box_selected,args=("",current_value,))
        self.threads["Resume_Watching"].start()
        self.label_status["text"] = "Fetching links..."
        self.threads["Fire_match_box_selected"] = threading.Thread(target = self.fire_list_box_selected,args=("",tree.get_anime_name_only(current_value),))
        self.threads["Fire_match_box_selected"].start()
    
    def download_range_buffer(self,all_of_them = None):
        #Multiple ranges downloaded in one session will cause the Range thread to be over-written but the task will be completed
        self.threads["Range"] = threading.Thread(target=self.download_range,args=(all_of_them,))
        self.threads["Range"].start()
        if all_of_them is None:
            self.label_download_status["text"]="Downloading given range of episodes will begin in a moment\n Fetching List..."
        else:
            self.label_download_status["text"]="Downloading ALL of episodes will begin in a moment\nFetching List..."
    
    def download_range(self,all_of_them):
        if all_of_them is None:
            start = self.start_episode_number_entry.get()
            end = self.end_episode_number_entry.get()
            if start.isnumeric() and end.isnumeric():
                start = int(start)
                end = int(end)
                if start >=1 and end<=self.episodes_list_length:
                    episodes_list = self.get_episodes(start,end)
                else:
                    self.label_download_status["text"]="Given download range invalid. See episodes list."
                    return None
            else:
                self.label_download_status["text"]="Given download range invalid. See episodes list."
                return None
        else:
            episodes_list = self.get_episodes()
        self.label_download_status["text"]="Download Episodes List Fetched! Will Download Now..."
        for episode in episodes_list:
            self.download_using_idm_single_episode(episode)
    
    def download_episode_idman_buffer(self):
        thread_name = self.episodes_list.get(ANCHOR)
        self.threads[thread_name]=threading.Thread(target=self.download_using_idm_single_episode)
        self.threads[thread_name].start()
        if os.name=="nt":
            self.label_download_status["text"]="Downloading in IDman.."
        elif os.name=="posix":
            self.label_download_status["text"]="Downloading in Wget.."
        
    
    def watch_in_vlc_buffer(self):
        self.threads["Watch_In_VLC"]=threading.Thread(target=self.watch_in_vlc)
        self.threads["Watch_In_VLC"].start()
        self.label_status["text"]="Opening the selected\nepisode in VLC..."
    
    def watch_in_browser_buffer(self):
        self.threads["Watch_In_Browser"] = threading.Thread(target = self.watch_in_browser)
        self.threads["Watch_In_Browser"].start()
        self.label_status["text"] = "Opening the selected\nepisode in broswer..."
    
    def fire_episodes_list_box_selected_buffer(self,event):
        self.download_selected_episode_button["state"]="normal"
        self.threads["Episodes_Box_Clicked"] = threading.Thread(target=self.fire_episodes_list_box_selected,args = (event,))
        self.threads["Episodes_Box_Clicked"].start()
        self.label_status["text"] = "Fetching Video URL..."
        self.watch_in_browser_button["state"]= "disabled"
        self.watch_in_vlc_button["state"] = "disabled"

        
    def fire_list_box_selected_buffer(self,event):
        self.download_range_button["state"]="normal"
        self.download_all_episodes_button["state"] = "normal"
        self.threads["List_Box_Clicked"] = threading.Thread(target = self.fire_list_box_selected,args=(event,))
        self.threads["List_Box_Clicked"].start()
        self.label_status["text"]="Fetching Episodes' List..."

    def download_using_idm_single_episode(self,episode_name = None):
        if episode_name is None:
            episode_name = self.episodes_list.get(ANCHOR)
        php_url = tree.make_video_url_ready(episode_name)
        video_url = tree.get_playlist_m3u8(php_url)
        if ("redirector" in video_url) or ("vidstreaming" in video_url) or video_url.endswith(".mp4"):
            program_path = os.path.dirname(os.path.realpath(__file__))
            series_name = "-".join(episode_name.split("-")[:-2])
            save_location = os.path.join(program_path,series_name)
            episode = episode_name+".mp4"
            if os.name=="nt":
                idman_path = os.path.join(os.environ.get('PROGRAMFILES(x86)'),'Internet Download Manager','idman.exe')
                if os.path.exists(idman_path):
                    idman_param_list = [idman_path,"/n","/d",video_url,"/p",save_location,"/f",episode]
                    self.label_download_status["text"] = episode_name+" sent to IDM."
                    call_idm = subprocess.Popen(idman_param_list)
                else:
                    self.label_download_status["text"] = "IDM not found installed please install IDM"
            elif os.name=="posix":
                subprocess.run(["mkdir","-p",series_name])
                wget_param_list = ["wget","-O","./"+series_name+"/"+episode,"-c",video_url]
                self.label_download_status["text"] = episode_name+" sent to Wget."
                call_wget = subprocess.run(wget_param_list)
                return_code=call_wget.returncode
                if return_code==0:
                    success_string = episode_name+" successfully downloaded!.\n"
                    self.label_download_status["text"]=success_string
                    with open("downloaded_episodes_list.txt","a") as download_file:
                        download_file.write(success_string)
                else:
                    failed_string = episode_name+" failed to download!.\n"
                    self.label_download_status["text"]=failed_string
                    with open("downloaded_episodes_list.txt","a") as download_file:
                        download_file.write(failed_string)
        else:
            self.label_download_status["text"]="The selected episode\ncannot be downloaded"

    def watch_in_browser(self):
        if self.current_php_url != "":
            webbrowser.open(self.current_php_url, new=0)
            self.label_status["text"] = "Video will now play\nin your default browser."

    def watch_in_vlc(self):
        if self.current_video_url !="":
            self.label_status["text"] = "Video will now play\n in VLC media player."
            result = tree.play_video_in_vlc(self.current_video_url)
            if result:
                self.label_status["text"]="Media Playing Terminated."
            else:
                self.label_status["text"]="VLC media player not found. Please install it."
            
    def search_button_clicked(self,button):
        self.matched_list.delete(0,'end')
        formatted_anime_name = tree.format_search_query(self.anime_entry.get())
        all_matched_results = tree.search_for_anime(formatted_anime_name)
        if len(all_matched_results)==0:
            matched_from_server = tree.let_server_search(formatted_anime_name)
            matched_results_formatted = [line.split("/")[-1] for line in matched_from_server]
        else:   
            matched_results_formatted = [line.split("/")[-1] for line in all_matched_results]
        if len(matched_results_formatted)==0:
            self.label_status["text"]="No match found."
        else:
            self.label_status["text"]=str(len(matched_results_formatted))+" matches found."
        for _ in matched_results_formatted:
            self.matched_list.insert(END,_)


    
    def fire_list_box_selected(self,event,anime_name = None):
        if anime_name is None:
            anime_name = self.matched_list.get(ANCHOR)
        episodes_list = self.get_episodes(anime_name)
        self.episodes_list_length = len(episodes_list)
        episodes_list.reverse()
        self.episodes_list.delete(0,'end')
        for _ in episodes_list:
            self.episodes_list.insert(END,_)
        self.label_status["text"]="Fetched All Episodes Successfully!"

    def get_episodes(self,anime_name,start=None,end=None):
        url = tree.global_head_url + anime_name
        all_episodes = tree.get_all_episodes(url,start,end)
        episodes_list = [line.split("/")[-1] for line in all_episodes]
        return episodes_list
    
    def get_episodes_count(self,anime_name):
        url = tree.global_head_url + anime_name
        return tree.num_of_episodes(url)
    
    def fire_episodes_list_box_selected(self,event,anime_name_episode = None):
        if anime_name_episode is None:
            anime_name_episode = self.episodes_list.get(ANCHOR)
            self.my_anime_list_combo.set(anime_name_episode)
        #Save progress to file
        tree.save_anime_progress(anime_name_episode)
        
        #Reload combo box with updated list after new episode has been added to list
        self.my_anime_list_combo["values"] = sorted(self.get_watched_animes())
        
        if anime_name_episode in self.anime_link_buffer:
            self.php_link_entry.delete(0,END)
            self.php_link_entry.insert(0,self.anime_link_buffer[anime_name_episode][0])
            self.watch_in_browser_button["state"]= "normal"
            self.video_link_entry.delete(0,END)
            self.video_link_entry.insert(0,self.anime_link_buffer[anime_name_episode][1])
            self.label_status["text"]="Fetched Video Url Successfully!"
            self.watch_in_vlc_button["state"] = "normal"
            self.current_video_url = self.anime_link_buffer[anime_name_episode][1]
            self.current_php_url = self.anime_link_buffer[anime_name_episode][0]

            #play vlc before fetching next
            self.watch_in_vlc_buffer()
            self.get_one_plus(anime_name_episode)            
        else:
            self.prepare_anime(anime_name_episode)


            
    def prepare_anime(self,anime_name_episode):
        php_url = self.get_php_url(anime_name_episode)
        video_url = self.get_video_url(php_url)
        self.current_php_url = php_url
        self.current_video_url = video_url
        self.anime_link_buffer[anime_name_episode] = []
        self.anime_link_buffer[anime_name_episode].extend([php_url,video_url])

        #play vlc before fetching next
        self.watch_in_vlc_buffer()
        self.get_one_plus(anime_name_episode)
        
    def get_one_plus(self,anime_name_episode):
        #Save +1 anime so that next time we don't need to wait for link fetching
        new_one = tree.get_anime_plus_one(anime_name_episode)
        if new_one not in self.anime_link_buffer:
            episode_number = tree.get_anime_episode_only(new_one)
            if int(episode_number) <= self.get_episodes_count(tree.get_anime_name_only(new_one)):
                php_url = self.get_php_url(new_one,show=False)
                video_url = self.get_video_url(php_url,show=False)
                self.anime_link_buffer[new_one] = []
                self.anime_link_buffer[new_one].extend([php_url,video_url])
                self.label_status["text"]="Next episodes link also fetched!"
            else:
                self.label_status["text"]="Anime list exceeded while fetching next episode link!"

    def get_php_url(self,anime_name_episode,show = True):
        php_url = tree.make_video_url_ready(anime_name_episode)

        if show:
            self.php_link_entry.delete(0,END)
            self.php_link_entry.insert(0,php_url)
            self.watch_in_browser_button["state"]= "normal"
        return php_url
    
    def get_video_url(self,php_url,show=True):
        video_url = tree.get_playlist_m3u8(php_url)

        if show:
            self.video_link_entry.delete(0,END)
            self.video_link_entry.insert(0,video_url)
            self.label_status["text"]="Fetched Video Url Successfully!"
            self.watch_in_vlc_button["state"] = "normal"
        return video_url
        
    def see_if_the_video_can_be_played(self):
        if self.current_video_url != "":
            tree.check_for_ways_to_play(self.current_video_url)

    def previous_next_episode(self,inc):
        anime = self.my_anime_list_combo.get()
        if anime != "":
            anime_name = tree.get_anime_name_only(anime)
            episode_number = tree.get_anime_episode_only(anime)                
            next_episode_number = int(episode_number)+inc
            if next_episode_number > 0:
                if inc==0:
                    self.label_status["text"]="Resuming. Please wait..."
                elif inc==1:
                    self.label_status["text"]="Next episode playing in a moment. Please wait..."
                else:
                    self.label_status["text"]="Previous episode playing in a moment. Please wait..."
                    
                next_one = anime_name + "-episode-" + str(next_episode_number)
                self.my_anime_list_combo.set(next_one)
                self.threads["Next_or_prev"] = threading.Thread(target=self.fire_episodes_list_box_selected,args = ("",next_one))
                self.threads["Next_or_prev"].start()

            
if __name__ == "__main__":
    my_main_window = window_main("Anime-no-tomodachi","885x320")
        
 
