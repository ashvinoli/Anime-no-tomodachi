from tree import *
import pathlib
import sys
import time
import math



no_interruption_mode = False
interruption_response = None
anime_name_response = None
selection_response = None
choice_response = None

if len(sys.argv) == 2:  #First argument is file name
    lines = []
    if os.path.exists("repeat.txt"):
        if sys.argv[1] == "-r":
            repeat = open("repeat.txt","r")
            for line in repeat:
                lines.append(line.rstrip())
            if len(lines)>=4:
                interruption_response = lines[0]
                anime_name_response = lines[1]
                selection_response = lines[2]
                choice_response = lines[3]
            repeat.close()
        
def video_quality_selection(my_playlist,anime_directory,episode_name):
    #This function prompts the user to select quality
    global default_mode
    chunks = anime_directory + "\\Chunks"
    index = 1
    length = len(my_playlist)
    print("Video qualities available for "+ episode_name)
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
            quality_file = open(chunks +"\\quality.txt","w")
            quality_file.write(my_playlist[int(resp)-1][0])
            quality_file.close()
            if ans == "y":
                default_mode = my_playlist[int(resp)-1][0]
            download_chunks(my_quality_video,anime_directory,episode_name)
            break
            
        else:
            resp = input("Bad quality!!!!!! Re-enter quality y/n?")
            if resp != "y":
                break

            
def download_in_a_different_way(episode_link):
    series_name = "-".join(episode_link.split("/")[-1].split("-")[:-2])
    episode_name = episode_link.split("/")[-1]
    program_path = os.path.dirname(os.path.realpath(__file__))
    anime_directory = program_path + "\\" + series_name + "\\" + episode_name
    chunks = anime_directory + "\\Chunks"
    if os.path.exists(anime_directory + "\\" +episode_name+".mp4"):
        print(episode_name+" has already been downloaded")
        return
    if not os.path.exists(chunks):
        pathlib.Path(chunks).mkdir(parents=True, exist_ok=True)
    vid_stream_link = BeautifulSoup(requests.get(episode_link).text,"html.parser").findAll("a",{"href":re.compile(r"https://vidstreaming.io/download.*")})[0].get("href")
    #print(vid_stream_link)
    download_link = BeautifulSoup(requests.get(vid_stream_link).text,"html.parser").findAll("a",{"href":re.compile(r"https://st\dx.cdnfile.info.*")})[0].get("href")
    #print(download_link)
    size = requests.head(download_link).headers.get("Content-length")
    #print(size)
    files = requests.get(download_link,stream=True)
    files.raise_for_status
    index = 1
    print("Downloading "+episode_link)
    time_prev = time.time()
    standard_size = 1048576
    file_pieces = files.iter_content(chunk_size = standard_size)
    for piece in files.iter_content(chunk_size = standard_size):
        chunk_name = chunks+"\\"+"chunk_"+str(index)+".mp4"
        chunk_file = open(chunk_name,"wb")
        chunk_file.write(piece)
        chunk_file.close()
        time_new = time.time()
        time_difference = time_new-time_prev
        time_prev = time_new
        percentage = int(index*standard_size/int(size)*100)
        if percentage >= 100:
            percentage = 100
        average_speed = (standard_size)/(1024*time_difference)
        print("\r%d%% complete. Average net speed = %.2f KB/s" % (percentage,average_speed),end="")
        index += 1

    append_them_all(index-1,anime_directory,episode_name,chunks)
        
        
        
        
   
def download_single_video(final_link,episode_link):
    global default_mode
    global no_interruption_mode
    series_name = "-".join(episode_link.split("/")[-1].split("-")[:-2])
    episode_name = episode_link.split("/")[-1]
    program_path = os.path.dirname(os.path.realpath(__file__))
    anime_directory = program_path + "\\" + series_name + "\\" + episode_name
    chunks = anime_directory + "\\Chunks"
    if not os.path.exists(chunks):
        pathlib.Path(chunks).mkdir(parents=True, exist_ok=True)
        #default_mode = None 
    else:
        if os.path.exists(chunks +"\\quality.txt"):
            quality = chunks + "\\quality.txt"
            quality_file = open(quality,"r")
            for _ in quality_file:
                quality = _.rstrip()
                default_mode = quality #NOTE if 1-6 like range are given and 1 file has been downloaded it will tip the default_mode to quality of 1 and further videos will be downloaded wih the same quality
    if not os.path.exists(anime_directory):
            pathlib.Path(anime_directory).mkdir(parents=True, exist_ok=True)
    if not (os.path.exists(anime_directory + "\\" + episode_name + ".mp4") or os.path.exists(anime_directory + "\\" + episode_name.split("-")[-1]+ ".mp4")):
        my_playlist = get_child_m3u8(get_playlist_m3u8(final_link))
        matched = False
        length = len(my_playlist)
        if length != 0:
            if default_mode == None:
                video_quality_selection(my_playlist,anime_directory,episode_name)
            else:
                for _ in my_playlist:
                    if _[0] == default_mode:
                        quality_file = open(chunks +"\\quality.txt","w")
                        quality_file.write(default_mode)
                        quality_file.close()
                        my_quality_video = provide_video_chunks(_[1])
                        if len(my_quality_video) ==0:
                            my_quality_video = provide_video_chunks_new(_[1])
                        download_chunks(my_quality_video,anime_directory,episode_name)
                        matched = True
                        break
                if not matched:
                    if no_interruption_mode:
                        download_chunks(my_playlist[0][1],anime_directory,episode_name)
                    else:
                        default_mode = None
                        print("Sorry, your default quality is unavailable for this video. So please select quality again.")
                        video_quality_selection(my_playlist,anime_directory, episode_name)         
        else:
            print("Sorry, the video you requested is currently not available! Will fix this problem soon!") #This problem is caused by the alternate hls10x site
    else:
        print(episode_name+" has already been downloaded!")
    
def download_chunks(video_chunks,anime_directory, episode_name):
    chunks = anime_directory + "\\Chunks"
    index = 1
    average_speed = math.inf
    global headers
    if not os.path.exists(chunks):
            pathlib.Path(chunks).mkdir(parents=True, exist_ok=True)
    print("Downloading "+episode_name+"...")
    length = len(video_chunks)
    file_count = len([name for name in os.listdir(chunks)])
    #Code below had to be written to ensure that no incomeplete files exists. I resorted to it after  requests.head().headers.get() failed. Code below fails to check the last file chunk. File count also counts the quality file
    if file_count >=2 and file_count <= length+1: #length + 1 because of the quality file
        os.remove(chunks+"\\"+"chunk_"+str(file_count-1)+".mp4")
    for chunk in video_chunks:
        tries = 1
        chunk_name = chunks+"\\"+"chunk_"+str(index)+".mp4"
        while True:
            if not os.path.exists(chunk_name):
                chunk_file = open(chunk_name,"wb")
                try:
                    begin_time = time.time()
                    current_chunk = requests.get(chunk).content #the headers for file request have been removed
                    end_time = time.time()
                    time_difference = end_time-begin_time
                    chunk_file.write(current_chunk)
                    chunk_file.close()
                    size = os.path.getsize(chunk_name)
                    average_speed = size/(1024*time_difference)
                    break
                except:
                    chunk_file.close()
                    if tries <= 5:
                        print("\nError on chunk "+str(index)+". Retrying.... Attempt:"+str(tries))
                        os.remove(chunk_name)
                        tries += 1
                    else:
                        print("Error on chunk "+str(index)+". " + str(tries-1) +" downloading attempt failed! Continuing download for another episode. Please redownload " + episode_name)
                        #os.remove(chunk_name)
                        return
            else:
                break
            
        percentage = int((index/length) * 100)
        #print(percentage,end="")
        #print("% complete.")
        print("\r%d%% complete. Average net speed = %.2f KB/s" % (percentage,average_speed),end="")
        index += 1
    append_them_all(length,anime_directory, episode_name,chunks)

def append_them_all(length,anime_directory,episode_name, chunks):
    print("\nAppending Pieces together......")
    big_episode = anime_directory + "\\" + episode_name + ".mp4"
    if len(big_episode) >= 250:
        big_episode = anime_directory + "\\" + episode_name.split("-")[-1]+ ".mp4"
    big_file = open(big_episode,"wb")
    for i in range (1,length+1):
        chunk_name = chunks+"\\"+"chunk_"+str(i)+".mp4"
        chunk_file = open(chunk_name,"rb")
        big_file.write(chunk_file.read())
        chunk_file.close()
        os.remove(chunk_name)
    big_file.close()
    print("Done appending. "+episode_name+" has been successfully downloaded!")
    print("\n")
    

def download_command_line():
    global no_interruption_mode
    global interruption_response 
    global anime_name_response 
    global selection_response 
    global choice_response
    repeat = open("repeat.txt","w")
    if interruption_response == None:
        interruption = input("Do you want to turn no interruption mode on? Type y/n:")
    else:
        interruption = interruption_response
    repeat.write(interruption+"\n")
    if interruption == "y":
        no_interruption_mode = True
    while True:
        os.system("cls")
        print("NOTE: IF YOU WANT TO SKIP ANY TYPING OR QUESTION JUST PRESS \"ENTER\" KEY.\nBUT DONOT PRESS ENTER FOR THIS FIRST QUESTION!\n")
        if anime_name_response == None:
            anime_name = input("Please enter the anime name (example:one-piece). Mind the dash(-) sign:")
        else:
            anime_name = anime_name_response    
        match_dict=[]
        f=open("all_animes.txt","r")
        found = False
        for line in f:
            if anime_name in line:
                match_dict.append(line)
                found = True
        f.close()
        if found:
            try:
                repeat.write(anime_name+"\n")
            except:
                pass
            
            for i in range(len(match_dict)):
                print(str(i+1) + "--->" + match_dict[i])
            while True:
                if selection_response == None:
                    selection = input("Please select your option among the SEARCHED RESULTS:")
                else:
                    selection = selection_response    
                if selection.isnumeric():
                    selection = int(selection)-1
                    if selection > len(match_dict)-1 or selection < 0:
                        resp = input("Your selection is not available! Make reselection? Type y/n:")
                        if resp != "y":
                            break
                    else:
                        try:
                            repeat.write(str(selection+1)+"\n")
                        except:
                            pass
                        num = str(num_of_episodes(match_dict[selection]))
                        while True:
                            if choice_response == None:
                                choice = input("There are "  + num + " episodes for "+ match_dict[selection] +"Type single number eg: 1 or 2 to download single episode, '1-5' to download range, 'A' or 'a' to download all episodes:")
                            else:
                                choice = choice_response
                                interruption_response = None
                                anime_name_response = None
                                selection_response = None
                                choice_response = None
                                
                            if choice.isnumeric():
                                choice = int(choice)
                                if choice > int(num) or choice < 1:
                                    print("Sorry, the episode you requested is not available yet!")
                                    resp = input("Want to download another episode? Type y/n:")
                                    if resp != "y":
                                        break
                                else:
                                    try:
                                        repeat.write(str(choice)+"\n")
                                        repeat.close()
                                    except:
                                        pass
                                    while True:
                                        if choice > int(num):
                                            print("Sorry, we are now out of episodes!")
                                            break
                                        my_episode = get_single_episode(match_dict[selection].rstrip(),choice)
                                        my_link = write_to_file(my_episode[0])
                                        final_link = my_link.split("//")[-1]
                                        final_link = "https://"+final_link
                                        #print(final_link)
                                        my_m3u8 = get_playlist_m3u8(final_link)
                                        if re.match("https://hls\d\dx",my_m3u8):
                                            try:
                                                download_in_a_different_way(my_episode[0])
                                            except:
                                                print(my_episode[0] + " couldn't be download due to some errors. Please considering redownloading it.")
                                        else:
                                            download_single_video(final_link,my_episode[0])
                                        #webbrowser.open_new(final_link)
                                        resp = input("Want to download next episode? Type y/n:")
                                        if resp != 'y':
                                            break
                                        else:
                                            choice += 1
                            elif re.match("^\d+-\d+$",choice): #don't miss the ^ and $ to exact match
                                try:
                                    repeat.write(str(choice)+"\n")
                                    repeat.close()
                                except:
                                    pass
                                begin = int(choice.split("-")[0])
                                end = int(choice.split("-")[1])
                                for i in range(begin,end+1):
                                    my_episode = get_single_episode(match_dict[selection].rstrip(),i)
                                    my_link = write_to_file(my_episode[0])
                                    final_link = my_link.split("//")[-1]
                                    final_link = "https://"+final_link
                                    my_m3u8 = get_playlist_m3u8(final_link)
                                    #print(final_link)
                                    if re.match("https://hls\d\dx",my_m3u8):
                                        try:
                                            download_in_a_different_way(my_episode[0])
                                        except:
                                            print(my_episode[0] + " couldn't be download due to some errors. Please considering redownloading it.")
                                    else:
                                        download_single_video(final_link,my_episode[0])
                            elif choice == "A" or choice == "a":
                                try:
                                    repeat.write(str(choice)+"\n")
                                    repeat.close()
                                except:
                                    pass
                                episodes_num = num_of_episodes(match_dict[selection].rstrip())
                                for i in range(1,episodes_num+1):
                                    my_episode = get_single_episode(match_dict[selection].rstrip(),i)
                                    my_link = write_to_file(my_episode[0])
                                    final_link = my_link.split("//")[-1]
                                    final_link = "https://"+final_link
                                    #print(final_link)
                                    my_m3u8 = get_playlist_m3u8(final_link)
                                    if re.match("https://hls\d\dx",my_m3u8):
                                        try:
                                            download_in_a_different_way(my_episode[0])
                                        except:
                                            print(my_episode[0] + " couldn't be download due to some errors. Please considering redownloading it.")
                                    else:
                                        download_single_video(final_link,my_episode[0])
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
    download_command_line()
