import speech_recognition as sr
import os
from set_path import setPath
import subprocess
from pydub import AudioSegment
from pydub.silence import split_on_silence
from termcolor import cprint

# -------functions--initialized----------
r=sr.Recognizer()
setPath("Easy-Captions","bin")
cprint(f"Current Working Directory Set --> {os.getcwd()}",'green')

# audo = "Sample.wav"
# audo = "LongSample.wav"

raw_text = ""
video_name = ""
step = -1

# -----------Functions--Defined-----------

def recognize_Audio():
    global raw_text
    global step
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
        step+=1
        save_Caption_File()
        os.remove(f"chunk{all_temp}.mp3")
        

def split(filepath):
    global chunks_count
    sound = AudioSegment.from_wav(filepath)
    dBFS = sound.dBFS
    chunks = split_on_silence(sound, 
        min_silence_len = 700,
        silence_thresh = dBFS-31,
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

def save_Caption_File():

    os.chdir('../Export')
    cprint(f"Saving to -> {os.getcwd()}",'green')
    
    your_file = f"{video_name[0:-4]}.srt"
    cprint(f"Name of your caption file : {video_name[:-4]}.srt",'green')
    
    Pattern = f"{step}\n00:00:00,000 --> 00:00:00,000\n{raw_text}\n\n"

    with open(your_file,"a") as ca:
        ca.writelines(Pattern)
        ca.close()

    setPath("Easy-Captions","temp")

if __name__ == "__main__" :
    extract_Audio("LongSample.mp4")
    split("con_audio.wav")
    recognize_Audio()