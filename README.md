# MEME Trainer v4
Edgar Makarov, 2019-2022 (c)
makaed@yandex.ru

A tool for the intelligent study of words with pronunciation.
The Czech and Portugese dictionaries are included, but any language can be added.

You can read the full description of the method here (in Russian)
https://github.com/MakaEdgar/MEMEnglish

Ask me if you run into any difficulties or find bugs. 


## Installation
1. clone git repository
```
git clone https://github.com/MakaEdgar/MEME_Trainer_4
```

2. Install python3
https://www.python.org/downloads/

3. Install necessary libraries
```
pip install pygame
pip install pyqt5

# to create new dicts
pip install gTTS    
```


## Game
0. Set your name in `./users/user_settings.txt`
1. Set dictionary in settings.txt
2. execute "run.bat"
3. press Start
4. write word => +Enter
5. If you are wrong, you should write it one more time
6. Repeat until the end of the words
7. See error and game statistics in `./users/UserName`

## Adding new dicts
1. Create txt file with two column structure: "phrase"-tab-"meaning"
2. Put is into folder `./tools/new_dicts`
3. Specify target language and speed in `download_audio_for_txt.py`
4. Execute `download_audio_for_txt.bat` file and wait (~2 second per word)
5. Copy new folder into `./dicts`, see structure there


