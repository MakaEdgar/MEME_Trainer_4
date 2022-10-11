# For dicts in txt files
sourcepath = "new_dicts/"
dicts = ['nl_a1_2', 'nl_a1_3']

# dutch = nl, portugese = pt, czech = cs
lang_key = "nl"
slow_speed = True


import os
import time
from gtts import gTTS
from tqdm import tqdm

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
    time.sleep(2)


for dictname in dicts:
    print("Start to download audio for", dictname, end=":\t")
    
    with open(sourcepath + dictname + ".txt", "r", encoding="UTF-8") as f:
        words = [w.split("\t")[0].strip() for w in f.read().split("\n") if w != ""]
        print("read", len(words), "words")

    dictpath = sourcepath + dictname + "/"
    audiopath = dictpath + dictname + "_audio/"
    os.mkdir(dictpath)
    os.mkdir(audiopath)
    
    for word in tqdm(words):
        load_audio(word, audiopath)
    print("Success!")