from tree import *
import pathlib
import sys
import time
import math

def video_quality_selection(my_playlist,anime_directory,episode_name):
    #This function prompts the user to select quality
    global default_mode
    chunks = anime_directory + "\\Chunks"
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

    
def download_single_video(final_link,episode_link):
    global default_mode
    series_name = "-".join(episode_link.split("/")[-1].split("-")[:-2])
    episode_name = episode_link.split("/")[-1]
    program_path = os.path.dirname(os.path.realpath(__file__))
    anime_directory = program_path + "\\" + series_name + "\\" + episode_name
    chunks = anime_directory + "\\Chunks"
    if not os.path.exists(chunks):
        pathlib.Path(chunks).mkdir(parents=True, exist_ok=True)
        #default_mode = None 
    else:
        quality = chunks + "\\quality.txt"
        quality_file = open(quality,"r")
        for _ in quality_file:
            quality = _.rstrip()
        default_mode = quality #NOTE if 1-6 like range are given and 1 file has been downloaded it will tip the default_mode to quality of 1 and further videos will be downloaded wih the same quality
    if not os.path.exists(anime_directory):
            pathlib.Path(anime_directory).mkdir(parents=True, exist_ok=True)
    if not os.path.exists(anime_directory + "\\" + episode_name + ".mp4"):
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
                        download_chunks(my_quality_video,anime_directory,episode_name)
                        matched = True
                        break
                if not matched:
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
        chunk_name = chunks+"\\"+"chunk_"+str(index)+".mp4"
        if not os.path.exists(chunk_name):
            chunk_file = open(chunk_name,"wb")
            try:
                begin_time = time.time()
                current_chunk = requests.get(chunk,headers = headers).content
                end_time = time.time()
                time_difference = end_time-begin_time
                chunk_file.write(current_chunk)
                chunk_file.close()
                size = os.path.getsize(chunk_name)
                average_speed = size/(1024*time_difference)
            except:
                print("Error on chunk "+str(index))
                chunk_file.close()
                os.remove(chunk_name)
                sys.exit() #Right now I can't think of any nice option other than terminating a program if any chunks fails to download because of some error
        percentage = int((index/length) * 100)
        #print(percentage,end="")
        #print("% complete.")
        print("\r%d %% complete. Average net speed = %.2f KB/s" % (percentage,average_speed),end="")
        index += 1
    append_them_all(length,anime_directory, episode_name,chunks)

def append_them_all(length,anime_directory,episode_name, chunks):
    print("\nAppending Pieces together......")
    big_episode = anime_directory + "\\" + episode_name + ".mp4"
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
                            choice = input("There are "  + num + " episodes for "+ match_dict[selection] +"Type single number eg: 1 or 2 to download single episode, '1-5' to download range, 'A' or 'a' to download all episodes:")
                            if choice.isnumeric():
                                choice = int(choice)
                                if choice > int(num) or choice < 1:
                                    print("Sorry, the episode you requested is not available yet!")
                                    resp = input("Want to download another episode? Type y/n:")
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
                                        download_single_video(final_link,my_episode[0])
                                        #webbrowser.open_new(final_link)
                                        resp = input("Want to download next episode? Type y/n:")
                                        if resp != 'y':
                                            break
                                        else:
                                            choice += 1
                            elif re.match("^\d+-\d+$",choice): #don't miss the ^ and $ to exact match
                                begin = int(choice.split("-")[0])
                                end = int(choice.split("-")[1])
                                for i in range(begin,end+1):
                                    my_episode = get_single_episode(match_dict[selection].rstrip(),i)
                                    my_link = write_to_file(my_episode[0])
                                    final_link = my_link.split("//")[-1]
                                    final_link = "https://"+final_link
                                    #print(final_link)
                                    download_single_video(final_link,my_episode[0])     
                            elif choice == "A" or choice == "a":
                                episodes_num = num_of_episodes(match_dict[selection].rstrip())
                                for i in range(1,episodes_num):
                                    my_episode = get_single_episode(match_dict[selection].rstrip(),i)
                                    my_link = write_to_file(my_episode[0])
                                    final_link = my_link.split("//")[-1]
                                    final_link = "https://"+final_link
                                    #print(final_link)
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
