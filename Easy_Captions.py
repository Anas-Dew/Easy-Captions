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
audo = "LongSample.wav"
# -----------Functions--Defined-----------

def recognize_Audio():
    print(os.getcwd())
    os.chdir("../temp")
    for all_temp in range(2):

        with sr.AudioFile(f"chunk{all_temp}.mp3") as source:
                audio_data = r.record(source)
                try:
                    text = r.recognize_google(audio_data)
                    print("Captured data : " ,text)
                except:
                    print("No internet connection.")

def split(filepath):
    sound = AudioSegment.from_wav(filepath)
    dBFS = sound.dBFS
    chunks = split_on_silence(sound, 
        min_silence_len = 800,
        silence_thresh = dBFS-30,
    )
    os.chdir("../temp")
    for i in range(len(chunks)):

        print(chunks[i])

        print("Exporting chunk{0}.mp3.".format(i))
        chunks[i].export(
            ".//chunk{0}.mp3".format(i),
            bitrate = "192k",
            format = "wav"
        )
    os.remove("../bin/con_audio.wav")
    # os.chdir("../")

def extract_Audio(video):
    print("Working in -> ",os.getcwd())
    command = f"ffmpeg -i {video} -ab 160k -ac 2 -ar 44100 -vn con_audio.wav"
    subprocess.call(command, shell=True)

def save_Caption_File():
    os.chdir('../Export')
    print("Saving to -> ",os.getcwd())

    your_file = input("Name your caption file : ")

    with open(your_file,"a") as ca:
        ca.writelines("Caption\n")
        ca.close()
    setPath("Easy-Captions","bin")



if __name__ == "__main__" :
    extract_Audio("LongSample.mp4")
    split("con_audio.wav")
    recognize_Audio()

