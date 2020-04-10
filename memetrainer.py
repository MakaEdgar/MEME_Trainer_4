import os
import sys
import random
import pygame
import copy
from PyQt5 import QtWidgets
import meme_gui

class Word:
    def __init__(self, record, settings=None):
        fields = [f.strip(" \t\r\n\"\'") for f in record.split("\t")]
        self.word1 = fields[0]
        self.word2 = fields[1]
        self.audiofile = audiopath + self.word1.replace(" ", "_").replace(",", "_").replace(".", "_") + ".mp3"
        if not os.path.exists(self.audiofile):
            self.audiofile = None

class WordDict:
    def __init__(self, dict_path=None, settings=None):
        if dict_path is not None:
            with open(dictpath, "r", encoding="UTF-8") as f:
                dict_records = [record for record in f.read().strip(" ;\r\n\t").split("\n") if (record.strip()[0] != "#")]
                self.container_ = [Word(record) for record in dict_records]
        else:
            self.container_ = []

    def size(self):
        return len(self.container_)

    def add_word(self, word):
        self.container_.append(word)
        
    def remove_word(self, word):
        self.container_.remove(word)
        
    def get_word(self, choose_randomly=True):
        #if self.size() == 0:
        #    return None

        if choose_randomly:
            chosen_word = random.choice(self.container_)
        else:
            chosen_word = self.container_[0]

        return chosen_word

class ContentBox:
    def __init__(self, description="default", contents={}):
        self.description = description
        self.container_ = contents
    def get_content_list(self):
        return self.container_.keys()
    def get_content(self, key):
        return self.container_.get(key, None)
        
class WordProcessor:
    def __init__(self, settings=None):
        self.settings = settings
        self.word = None
    
    def load_word(self, word):
        self.word = word
        self.is_user_answer_correct = None
    
    def get_task(self):
        task_contents = {"text" : self.word.word2}
        task_box = ContentBox(description="task",
                              contents=task_contents)
        return task_box


    def check_answer(self, user_answer_box):
        self.user_answer_box = user_answer_box
        self.is_user_answer_correct = (self.user_answer_box.get_content("text") == self.word.word1)
        return self.is_user_answer_correct

    def get_answer(self):
        answer_contents = {"text" : "",
                           "audio": self.word.audiofile}

        if self.is_user_answer_correct:
            answer_contents["text"] = "Yes!"
        else:
            answer_contents["text"] = "No! Correct is " + self.word.word1

        answer_box = ContentBox(description="answer",
                                contents=answer_contents)
        return answer_box

class Trainer:
    def __init__(self, words, processor, settings=None):
        self.words_init = words
        self.processor = processor
        self.settigns = settings

        self.words_remain = copy.deepcopy(words)
        self.words_done = WordDict()
        self.words_removed = WordDict()
        
                      
        self.stats = {"words_remain":       self.words_remain.size(),
                      "words_done":         self.words_done.size(),
                      "words_removed":      0,
 
                      "words_run":          0,
                      "words_error":        0,
                      "words_remembered":   0,
                      "mistakes":           0,
                      
                      "percent":            0,
                      "points":             0,
                     } 
        self.flags = {"last_user_ans_was_correct" : True}


    def choose_new_word(self):
        self.word = self.words_remain.get_word()
        self.processor.load_word(self.word)
        self.flags["last_user_ans_was_correct"] = True
        self.stats["words_run"] += 1
    

    def get_task(self):
        if self.flags["last_user_ans_was_correct"]:
            self.choose_new_word()
        return self.processor.get_task()
    
    def get_answer(self, user_answer_box):
        is_user_ans_correct = self.processor.check_answer(user_answer_box)
        if is_user_ans_correct:
            if self.flags["last_user_ans_was_correct"]:
                self.words_done.add_word(self.word)
                self.words_remain.remove_word(self.word)
            self.flags["last_user_ans_was_correct"] = True

        else:
            self.flags["last_user_ans_was_correct"] = False
            self.stats["mistakes"] += 1
            

        return self.processor.get_answer()
    
    
    def update_stats(self):
        self.stats["words_remain"] = self.words_remain.size()
        self.stats["words_done"] = self.words_done.size()
        self.stats["words_removed"] = self.words_removed.size()
        self.stats["points"] = (-10 * self.stats["mistakes"]
                                + 5 * self.stats["words_done"])
        
    
    def get_stats(self):
        self.update_stats()
        return self.stats

    def is_game_finished(self):
        return (False if self.words_remain.size() > 0 else True)

    def finalize(self):
        pass

    def eval_command(self, command):
        if command == "n":
            self.choose_new_word()
        if command == "r":
            self.words_removed.add_word(self.word)
            self.words_remain.remove_word(self.word)
            self.choose_new_word()
 

class ExampleApp(QtWidgets.QMainWindow, meme_gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()  # Это здесь нужно для доступа к переменным, методам в файле design.py
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.btn_start_stop.clicked.connect(self.btn_start_stop_clicked)  
        self.btn_ok.clicked.connect(self.btn_ok_clicked)  
        self.le_userans.returnPressed.connect(self.btn_ok.click)
        self.btn_exit.clicked.connect(self.btn_exit_clicked)


    def init_game(self, trainer):
        self.game_status_descr = "not_started"
        self.next_btnOK_action_descr = "display_task"
        self.trainer = trainer

    def btn_start_stop_clicked(self):
        if self.game_status_descr is "not_started":
            self.game_status_descr = "started"
            self.btn_start_stop.setText("Pause")
            self.btn_ok_clicked()
        elif self.game_status_descr == "stopped":
            self.game_status_descr = "started"
            self.btn_start_stop.setText("Pause")
        elif self.game_status_descr == "started":
            self.game_status_descr = "stopped"
            self.btn_start_stop.setText("Start")

    def btn_ok_clicked(self):
        if self.game_status_descr != "started":
            return

        if self.next_btnOK_action_descr == "display_task":
            task_box = self.trainer.get_task()
            self.display_task(task_box)
            self.next_btnOK_action_descr = "check_and_display_answer"

        elif self.next_btnOK_action_descr == "check_and_display_answer":
            user_answer_text = self.le_userans.text()
            if self.is_command(user_answer_text):
                self.eval_command(user_answer_text[1])
            else:
                user_answer_contents = {"text": user_answer_text}
                user_answer_box = ContentBox(description="user_answer",
                                             contents=user_answer_contents)
                answer_box = self.trainer.get_answer(user_answer_box) 
                self.display_answer(answer_box)

            stats = self.trainer.get_stats()
            self.display_stats(stats)
            
            if not self.trainer.is_game_finished():
                self.next_btnOK_action_descr = "display_task"
            else:
                self.next_btnOK_action_descr = "pass"
                self.finalize()

            if self.is_command(user_answer_text):
                self.btn_ok_clicked()
        else:
            return


    def is_command(self,text):
        return len(text)>1 and text[0]=="!"

    def eval_command(self, command):
        if command in ["n", "r"]:
            self.trainer.eval_command(command)
        elif command == "e":
            self.btn_exit_clicked()

    def display_task(self, task_box):
        if "audio" in task_box.get_content_list():
            self.play_audio(task_box.get_content("audio"))
        if "text" in task_box.get_content_list():
            self.lb_task.setText(task_box.get_content("text"))
        self.le_userans.setText("")      
        self.lb_result.setText("")

    def display_answer(self, answer_box):
        if "audio" in answer_box.get_content_list():
            self.play_audio(answer_box.get_content("audio"))
        if "text" in answer_box.get_content_list():
            self.lb_result.setText(answer_box.get_content("text"))

    def display_stats(self, stats : dict):
        num_words_remain = stats.get("words_remain", "-")
        num_words_done = stats.get("words_done", "-")
        num_mistakes = stats.get("mistakes", "-")
        num_percent = stats.get("percent", "-")
        num_points = stats.get("points", "-")

        self.statusbar.showMessage(  "Done: "     + str(num_words_done) +  " "
                                   + "Mistakes: " + str(num_mistakes) + " "
                                   #+ "Percent: "  + str(num_percent) + " " 
                                   + "Points: "  + str(num_points) + " " 
                                   + "\t\t" 
                                   + "Remain: "   + str(num_words_remain) + " "
                                  )

    def finalize(self):
        self.lb_result.setText("")
        self.le_userans.setText("Thank you!")
        #self.lb_task.setText("You made mistakes: " + str(self.num_mistakes))
        self.le_userans.setReadOnly(True)
        self.btn_ok.setEnabled(False)
        self.btn_start_stop.setEnabled(False)

    def play_audio(self, audiofile):
        if audiofile is not None:
            pygame.mixer.init()
            pygame.mixer.music.load(audiofile)
            pygame.mixer.music.play()

    def btn_exit_clicked(self):
        self.trainer.finalize()
        self.close()


#=======================================================


def main():
    words = WordDict(dict_path=dictpath)
    processor = WordProcessor()
    trainer = Trainer(words=words, processor=processor)


    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp

    window.init_game(trainer)

    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

dictpath = "./dicts/cz1/cz1.txt"
audiopath = "./dicts/cz1/cz1_audio/"
main()