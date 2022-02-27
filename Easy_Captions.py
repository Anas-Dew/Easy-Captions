from time import sleep
import speech_recognition as sr
import os
from set_path import setPath
import subprocess
from pydub import AudioSegment
from pydub.silence import split_on_silence
from termcolor import cprint
from pyfiglet import figlet_format
from clearscreen import clear


# -------functions-&-Vriables--initialized----------

r=sr.Recognizer()
setPath("Easy-Captions","bin")
cprint(f"Current Working Directory Set --> {os.getcwd()}",'green')

captions = []
raw_text = ""
video_name = ""
step = -1


# -----------Functions--Defined-----------

def recognize_Audio():
    try:
        global raw_text,step,captions
        
        os.chdir("../temp")
        cprint(f"Working in -> {os.getcwd()}",'green')

        for all_temp in range(chunks_count):
            
            with sr.AudioFile(f"chunk{all_temp}.mp3") as source:
                    audio_data = r.record(source)
                    try:
                        raw_text = r.recognize_google(audio_data)
                        cprint(f"Captured data : {raw_text}",'blue')
                        
                    except:
                        cprint("\n\t\tError !",'red')
            captions.append(raw_text)
            os.remove(f"chunk{all_temp}.mp3")

        cprint(f"Path of your caption file : {video_name[:-4]}.srt",'green')   
        
    except:
            cprint("File Not Found ! or Invalid Path","red")
def split(filepath):
    try:
        global chunks_count
        sound = AudioSegment.from_wav(filepath)
        dBFS = sound.dBFS
        chunks = split_on_silence(sound, 
            min_silence_len = 400,
            silence_thresh = dBFS-37,
        )
        chunks_count = len(chunks)

        os.chdir("../temp")
        for i in range(chunks_count):

            cprint(chunks[i],'red')
            cprint("Exporting chunk{0}.mp3.".format(i),'green')
            
            chunks[i].export(
                ".//chunk{0}.mp3".format(i),
                bitrate = "192k",
                format = "wav"
            )

            os.remove("../bin/con_audio.wav")
    except:
            cprint("File Not Found ! or Invalid Path","red")

def extract_Audio(video):
    try:
        global video_name
        cprint(f"Working in -> {os.getcwd()}",'green')
        command = f"ffmpeg -i {video} -ab 160k -ac 2 -ar 44100 -vn con_audio.wav"
        subprocess.call(command, shell=True)
        video_name = video

    except:
            cprint("File Not Found ! or Invalid Path","red")
            exit(0)

def save_Caption_File():
    global step
    os.chdir('../Export')
    # --------Caption-Specific-Variables--------
    s_hrs = 0
    s_mins = 0
    s_secs = 0
    e_hrs = 0
    e_mins = 0
    e_secs = 0
    mili_Secs = 0
    
    for i in range(len(captions)):

        length = len(captions[i].split(" "))

        start_Time = f"{s_hrs}:{s_mins}:{s_secs},{mili_Secs+350}"
        end_Time = f"{e_hrs}:{e_mins}:{e_secs+5},{mili_Secs}"
        
        if 9 < length <= 11:
            start_Time = f"{s_hrs}:{s_mins}:{s_secs},{mili_Secs+350}"
            end_Time = f"{e_hrs}:{e_mins}:{e_secs+9},{mili_Secs}"

        elif 3 <= length <= 8:
            start_Time = f"{s_hrs}:{s_mins}:{s_secs},{mili_Secs+350}"
            end_Time = f"{e_hrs}:{e_mins}:{e_secs+3},{mili_Secs}"

        elif 12 <= length <= 16:
            start_Time = f"{s_hrs}:{s_mins}:{s_secs},{mili_Secs+350}"
            end_Time = f"{e_hrs}:{e_mins}:{e_secs+5},{mili_Secs}"

        elif 1 <= length <= 2:
            start_Time = f"{s_hrs}:{s_mins}:{s_secs},{mili_Secs+350}"
            end_Time = f"{e_hrs}:{e_mins}:{e_secs+1},{mili_Secs}"
        elif 17 < length :
            start_Time = f"{s_hrs}:{s_mins}:{s_secs},{mili_Secs+350}"
            end_Time = f"{e_hrs}:{e_mins}:{e_secs+10},{mili_Secs}"

        step+=1
        e_secs+=3
        s_secs = e_secs
        try:

            your_File = f"{video_name[0:-4]}.srt"
            caption_Pattern = f"{step}\n{start_Time} --> {end_Time}\n{captions[i]}\n\n"
            with open(your_File,"a") as ca:
                ca.writelines(caption_Pattern)
            ca.close()

        except:
            cprint("File Not Found ! or Invalid Path","red")
            


    setPath("Easy-Captions","temp")
    
def controls():
        cprint(figlet_format("Easy Captions"),'blue')
        print("\n\t1 - Generate Captions")
        print("\t2 - Exit")
        try:
            usr_Choice = int(input("Type Here - "))
            if usr_Choice == 1:
                video_name = input("Enter Video Path : ")
                extract_Audio(video_name)
                split("con_audio.wav")
                recognize_Audio()
                save_Caption_File()

            elif usr_Choice == 2:
                cprint(figlet_format("Thanks You"),'green')
                sleep(2)
                exit(0)
            else:
                cprint("Choose from above options only !","red")
                clear()
                controls()

        except ValueError:    
            cprint("Choose from above options only !","red")
            clear()
            controls()
        

if __name__ == "__main__" :
    controls()
    