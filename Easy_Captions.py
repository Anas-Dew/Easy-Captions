import speech_recognition as sr
import os
from set_path import setPath
import subprocess
from pydub import AudioSegment
from pydub.silence import split_on_silence

# -------functions--initialized----------
r=sr.Recognizer()

setPath("Easy-Captions","bin")
print("Current Working Directory Set -->",os.getcwd())

# audo = "Sample.wav"
# audo = "LongSample.wav"
raw_text =""
video_name =""
# -----------Functions--Defined-----------

def recognize_Audio():
    global raw_text
    os.chdir("../temp")
    print("Working in ->" ,os.getcwd())
    for all_temp in range(2):
        
        with sr.AudioFile(f"chunk{all_temp}.mp3") as source:
                audio_data = r.record(source)
                try:
                    raw_text = r.recognize_google(audio_data)
                    print("Captured data : " ,raw_text)
                    
                except:
                    print("Internet Error !")
                    
        save_Caption_File()
        

def split(filepath):
    global chunks_count
    sound = AudioSegment.from_wav(filepath)
    dBFS = sound.dBFS
    chunks = split_on_silence(sound, 
        min_silence_len = 800,
        silence_thresh = dBFS-30,
    )
    chunks_count = len(chunks)

    os.chdir("../temp")
    for i in range(chunks_count):

        print(chunks[i])

        print("Exporting chunk{0}.mp3.".format(i))
        chunks[i].export(
            ".//chunk{0}.mp3".format(i),
            bitrate = "192k",
            format = "wav"
        )
    os.remove("../bin/con_audio.wav")

def extract_Audio(video):
    global video_name
    print("Working in -> ",os.getcwd())
    command = f"ffmpeg -i {video} -ab 160k -ac 2 -ar 44100 -vn con_audio.wav"
    subprocess.call(command, shell=True)
    video_name = video

def save_Caption_File():

    os.chdir('../Export')
    print("Saving to -> ",os.getcwd())
    
    your_file = f"{video_name[0:-4]}.srt"
    print(f"Name of your caption file : {video_name[:-4]}.srt")
    

    Pattern = f"{None}\n00:00:00,000 --> 00:00:00,000\n{raw_text}\n\n"

    with open(your_file,"a") as ca:
        ca.writelines(Pattern)
        ca.close()


    setPath("Easy-Captions","temp")



if __name__ == "__main__" :
    extract_Audio("LongSample.mp4")
    split("con_audio.wav")
    recognize_Audio()