# For dicts in txt files
sourcepath = "new_dicts/"
dicts = ['cz_a1_9','cz_a1_10']


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


# portugese = pt, czech = cs
def load_audio(word, audiopath="./", slow=True, lang_key="pt"):
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