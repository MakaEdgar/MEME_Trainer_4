words = """
toho kvalitního kolegu
žít, žiju
"""
words = [x.strip() for x in words.split("\n") if x.strip() != ""]


# portugese = pt, czech = cs
lang_key = "pt"
slow_speed = True


import os
import time
from gtts import gTTS
import tqdm

def get_audiofile_name(word):
    symbols_to_replace = " .,?!\"\'"
    audiofile_name = ""
    for w in word:
        audiofile_name = audiofile_name + (w if w not in symbols_to_replace else "_")
    return audiofile_name + ".mp3"

def load_audio(word, audiopath="./", slow=slow_speed, lang_key=lang_key):
    myobj = gTTS(text=word, lang=lang_key, slow=slow)
    
    filename = get_audiofile_name(word)
    myobj.save(audiopath + filename)

    time.sleep(1)
        
for word in tqdm.tqdm(words):
    load_audio(word)
