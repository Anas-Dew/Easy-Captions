import speech_recognition as sr
import os
from set_path import setPath
import subprocess
from pydub import AudioSegment
from pydub.silence import split_on_silence
from termcolor import cprint

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

        # raw_text_length = len(raw_text.split(" "))
        # if 4 <= raw_text_length <= 10:
        #     secs+=7
        
        # save_Caption_File_old()
        os.remove(f"chunk{all_temp}.mp3")

    cprint(f"Name of your caption file : {video_name[:-4]}.srt",'green')
    cprint(f"Saving to -> {os.getcwd()}",'green')      

def split(filepath):
    global chunks_count
    sound = AudioSegment.from_wav(filepath)
    dBFS = sound.dBFS
    chunks = split_on_silence(sound, 
        min_silence_len = 560,
        silence_thresh = dBFS-38,
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

def extract_Audio(video):
    global video_name
    cprint(f"Working in -> {os.getcwd()}",'green')
    command = f"ffmpeg -i {video} -ab 160k -ac 2 -ar 44100 -vn con_audio.wav"
    subprocess.call(command, shell=True)
    video_name = video

# def save_Caption_File_old():
#     global start_Time
#     global end_Time
#     os.chdir('../Export')
    
#     your_File = f"{video_name[0:-4]}.srt"
#     caption_Pattern = f"{step}\n{start_Time} --> {end_Time}\n{raw_text}\n\n"

#     with open(your_File,"a") as ca:
#         ca.writelines(caption_Pattern)
#         ca.close()

#     setPath("Easy-Captions","temp")

def save_Caption_File():
    
    global step
    os.chdir('../Export')
    # --------Caption-Specific-Variables--------
    hrs = 0
    mins = 0
    secs = 0
    mili_Secs = 0
    

    for i in range(len(captions)):

        start_Time = f"{hrs}:{mins}:{secs},{mili_Secs+350}"
        end_Time = f"{hrs}:{mins}:{secs+4},{mili_Secs}"
        step+=1
        secs+=4
        your_File = f"{video_name[0:-4]}.srt"
        caption_Pattern = f"{step}\n{start_Time} --> {end_Time}\n{captions[i]}\n\n"
        with open(your_File,"a") as ca:
            ca.writelines(caption_Pattern)

    ca.close()

    setPath("Easy-Captions","temp")

if __name__ == "__main__" :
    extract_Audio("LongSample.mp4")
    split("con_audio.wav")
    recognize_Audio()
    save_Caption_File()
    