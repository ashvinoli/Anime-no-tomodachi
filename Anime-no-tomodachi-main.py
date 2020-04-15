from tkinter import *
from windows_class import *
import threading
import tree
import webbrowser

class window_main(windows):
    def __init__(self,title="My window",geometry="800x800"):
        super().__init__(title,geometry)
        self.current_video_url=""
        self.current_php_url = ""
        
        
    def define_frames(self):
        self.matched_frame = LabelFrame(self.window,text = "Matched Results",padx=5,pady=2)
        self.episodes_list_frame = LabelFrame(self.window,text = "Episodes List",padx = 5,pady=2)
        self.buttons_bundle_frame = LabelFrame(self.window,text = "Download/Watch",padx=5,pady=5)
        self.start_end_frame = LabelFrame(self.buttons_bundle_frame,padx=2)
        
    def pack_frames(self):
        self.matched_frame.grid(row=2,column=1)
        self.episodes_list_frame.grid(row=2,column=2)
        self.buttons_bundle_frame.grid(row=2,column=3,sticky=NW)
        self.start_end_frame.pack()
        
    
    def define_labels(self):
        self.label_search_for_anime = Label(self.window,text = "Search for Anime:")
        self.label_TO = Label(self.start_end_frame,text = "To")
        self.label_status = Label(self.buttons_bundle_frame,text ="No Work In Progress." ,fg="green")
        
    def pack_labels(self):
        self.label_search_for_anime.grid(row = 1,column=1,sticky=E)
        self.label_TO.grid(row=1,column=2)
        self.label_status.pack()
        
    def define_buttons(self):
        width = 27
        self.download_selected_episode_button = Button(self.buttons_bundle_frame,text = "Download Selected Episode",width = width)
        self.watch_in_browser_button = Button(self.window,text = "Watch In Browser",width=width,command = self.watch_in_browser_buffer)
        self.watch_in_browser_button["state"] = "disabled"
        self.watch_in_vlc_button = Button(self.window,text = "Watch In VLC",width=width,command = self.watch_in_vlc_buffer)
        self.watch_in_vlc_button["state"] = "disabled"
        self.download_all_episodes_button = Button(self.buttons_bundle_frame,text = "Download All Episodes",width = width)
        self.download_range = Button(self.start_end_frame,text = "Download Range")
        
    def pack_buttons(self):
        self.download_selected_episode_button.pack()
        self.download_all_episodes_button.pack()
        self.watch_in_browser_button.grid(row=3,column=3)
        self.watch_in_vlc_button.grid(row=4,column=3)
        self.download_range.grid(row=1,column=4)

        
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
    #All associated functions

    
    def watch_in_vlc_buffer(self):
        self.threads["Watch_In_VLC"]=threading.Thread(target=self.watch_in_vlc)
        self.threads["Watch_In_VLC"].start()
        self.label_status["text"]="Opening the selected\nepisode in VLC..."
    
    def watch_in_browser_buffer(self):
        self.threads["Watch_In_Browser"] = threading.Thread(target = self.watch_in_browser)
        self.threads["Watch_In_Browser"].start()
        self.label_status["text"] = "Opening the selected\nepisode in broswer..."
    
    def fire_episodes_list_box_selected_buffer(self,event):
        self.threads["Episodes_Box_Clicked"] = threading.Thread(target=self.fire_episodes_list_box_selected,args = (event,))
        self.threads["Episodes_Box_Clicked"].start()
        self.label_status["text"] = "Fetching Video URL..."
        self.watch_in_browser_button["state"]= "disabled"
        self.watch_in_vlc_button["state"] = "disabled"

        
    def fire_list_box_selected_buffer(self,event):
        self.threads["List_Box_Clicked"] = threading.Thread(target = self.fire_list_box_selected,args=(event,))
        self.threads["List_Box_Clicked"].start()
        self.label_status["text"]="Fetching Episodes' List..."


    def watch_in_browser(self):
        if self.current_php_url != "":
            webbrowser.open(self.current_php_url, new=0)
            self.label_status["text"] = "Video will now play\nin your default browser."

    def watch_in_vlc(self):
        if self.current_video_url !="":
            self.label_status["text"] = "Video will now play\n in VLC media player."
            tree.play_video_in_vlc(self.current_video_url)
            self.label_status["text"]="Media Playing Terminated."
            
    def search_button_clicked(self,button):
        self.matched_list.delete(0,'end')
        formatted_anime_name = tree.format_search_query(self.anime_entry.get())
        all_matched_results = tree.search_for_anime(formatted_anime_name)
        matched_results_formatted = [line.split("/")[-1] for line in all_matched_results]
        for _ in matched_results_formatted:
            self.matched_list.insert(END,_)

        
    def fire_list_box_selected(self,event):
        self.episodes_list.delete(0,'end')
        url = tree.global_head_url + self.matched_list.get(ANCHOR)
        all_episodes = tree.get_all_episodes(url)
        episodes_list = [line.split("/")[-1] for line in all_episodes]
        episodes_list.reverse()
        for _ in episodes_list:
            self.episodes_list.insert(END,_)
        self.label_status["text"]="Fetched All Episodes Successfully!"
        
    def fire_episodes_list_box_selected(self,event):
        php_url = tree.make_video_url_ready(self.episodes_list.get(ANCHOR))
        self.current_php_url = php_url
        self.php_link_entry.delete(0,END)
        self.php_link_entry.insert(0,php_url)
        video_url = tree.get_playlist_m3u8(php_url)
        self.current_video_url = video_url
        self.video_link_entry.delete(0,END)
        self.video_link_entry.insert(0,video_url)
        self.label_status["text"]="Fetched Video Url Successfully!"
        self.watch_in_browser_button["state"]= "normal"
        self.watch_in_vlc_button["state"] = "normal" 
        
    def see_if_the_video_can_be_played(self):
        if self.current_video_url != "":
            tree.check_for_ways_to_play(self.current_video_url)
            
if __name__ == "__main__":
    my_main_window = window_main("Anime-no-tomodachi","885x260")
        
 
