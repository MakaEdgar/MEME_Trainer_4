dictpath = "./dicts/cz1/cz1.txt"
audiopath = "./dicts/cz1/cz1_audio/"


import os
import sys
import pygame
import random
def play(word):
    if word.audiofile is not None:
        pygame.mixer.init()
        pygame.mixer.music.load(word.audiofile)
        pygame.mixer.music.play()


    

with open(dictpath, "r", encoding="UTF-8") as f:
    dict_records = [record for record in f.read().strip(" ;\n\t").split("\n") if (record.strip()[0] != "#")]
    dict_words = [Word(record) for record in dict_records]


words_remain, words_done  = dict_words, []
def get_word_index():
    if len(words_remain) >= 1:
        word_index = random.randint(0, len(words_remain)-1)
    else:
        word_index = -1
    return word_index

def get_word_by_index(word_index):
    word = words_remain[word_index]
    return word
def remove_finished_word(word_index):
    words_done.append(words_remain.pop(word_index))



class Word:
    def __init__(self, record):
        #print(record)
        fields = [f.strip(" \t\r\n\"\'") for f in record.split("\t")]
        self.item = fields[0]
        self.value = fields[1]
        self.audiofile = audiopath + self.item.replace(" ", "_") + "___" + "thx" + ".mp3"
        if not os.path.exists(self.audiofile):
            self.audiofile = None
    def get_item(self):
        return self.item
    def get_value(self):
        return self.value


class WordDict:
    def __init__(self):
        pass
    
    def size(self):
        pass

    def add_word(self, word):
        pass
    def remove_word(self, word):
        pass
    def pop_word(self, word):
        pass
    def get_word(self, randomly=True):
        pass

    def remove_word_by_index(self, word_index):
        pass
    def pop_word_by_index(self, word_index):
        pass
    def get_word_by_index(self, word_index):
        pass



class Card:
    def __init__(self):
        self.card_type = "text"
    def get_text(self):
        pass
    def get_audio(self):

class CardTask(Card):
    def __init__(self):
        self.card_purpose = "task"

class CardUserAnswer(Card):
    def __init__(self):
        self.card_purpose = "user_answer"

class CardAnswer(Card):
    def __init__(self):
        self.card_purpose = "answer"
        self.card_type = "text_audio"



class WordProcessor:
    def __init__(self, word):
        self.word = word
        pass

    def get_task(self):
        pass
    def check_answer(self, user_answer_text):
        pass
    def get_answer(self):
        pass




class Trainer:
    def __init__(self, words : "WordDict"):
        self.words_remain = None
        self.words_done = None
        self.words_removed = None
        
        self.stats = {}
        self.flags_ = {"last_try_was_success" : True}

    def get_task(self):
        return "I'm task"
    
    def check_answer(self, user_answer_text):
        pass

    def get_answer(self):
        return "Yes, I'm answer"
    
    def get_stats(self):
        return self.stats

    def is_game_finished(self):
        return False

    def finalize(self):
        pass
    

















from PyQt5 import QtWidgets
import meme_gui
class ExampleApp(QtWidgets.QMainWindow, meme_gui.Ui_MainWindow):
    def __init__(self, trainer : Trainer):
        super().__init__()  # Это здесь нужно для доступа к переменным, методам в файле design.py
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.btn_start_stop.clicked.connect(self.btn_start_stop_clicked)  
        self.btn_ok.clicked.connect(self.btn_ok_clicked)  # Выполнить функцию при нажатии кнопки
        self.le_userans.returnPressed.connect(self.btn_ok.click)
        self.btn_exit.clicked.connect(self.btn_exit_clicked)
        

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
            task_text = self.trainer.get_task()
            self.display_task(task_text)
            self.next_btnOK_action_descr = "check_and_display_answer"
        elif self.next_btnOK_action_descr == "check_and_display_answer":
            user_answer_text = self.le_userans.text()
            self.trainer.check_answer(user_answer_text)
            answer_text = self.trainer.get_answer() 
            self.display_answer(answer_text)

            stats = self.trainer.get_stats()
            self.display_stats(stats)
            
            if not self.trainer.is_game_finished():
                self.next_btnOK_action_descr = "display_task"
            else:
                self.next_btnOK_action_descr = "pass"
                self.finalize()
        else:
            return

    def btn_exit_clicked(self):
        self.trainer.finalize()
        self.close()


    def display_task(self, task_text):
        self.lb_task.setText(task_text)
        self.le_userans.setText("")      
        self.lb_result.setText("")
        

    def display_answer(self, answer_text):
        self.lb_result.setText(answer_text)


    def display_stats(self, stats : dict):
        num_words_remain = stats.get("words_remain", "-")
        num_words_done = stats.get("words_done", "-")
        num_mistakes = stats.get("words_remain", "-")
        num_rights = stats.get("words_remain", "-")
        num_percent = stats.get("words_remain", "-")

        self.statusbar.showMessage(  "Rights: "   + str(num_rights) + " "
                                   + "Mistakes: " + str(num_mistakes) + " "
                                   + "Percent: "  + str(num_percent) + " " 
                                   + "\t" 
                                   + "Remain: "   + str(num_words_remain) + " "
                                   + "Done: "     + str(num_words_done) + " "
                                  )


    def finalize(self):
        self.lb_result.setText("")
        self.le_userans.setText("Thank you!")
        #self.lb_task.setText("You made mistakes: " + str(self.num_mistakes))
        self.le_userans.setReadOnly(True)
        self.btn_ok.setEnabled(False)
        self.btn_start_stop.setEnabled(False)
        





    # def btn_ok_clicked(self):
    #     userans = self.le_userans.text()
    #     elif self.game_status == "wait_new_word":
    #         self.game_status = "wait_userans"
    #         self.curr_word_index = get_word_index()
    #         self.curr_word = get_word_by_index(self.curr_word_index)
    #         self.update_labels()
    #     elif self.game_status == "checking":
    #         if len(userans)>=2 and userans[0] == "!":
    #             self.run_checking_command(userans.lower()[1])
    #         else:
    #             self.game_status = "wait_userans"
    #             if self.last_attempt_status == "success":
    #                 remove_finished_word(self.curr_word_index)
    #                 self.curr_word_index = get_word_index()
    #                 self.update_labels()
    #                 if self.curr_word_index != -1:
    #                     self.curr_word = get_word_by_index(self.curr_word_index)
    #                 else:
    #                     self.finalize()
    #             else:
    #                 self.last_attempt_status = "failure"
    #                 self.update_labels()
    #     elif self.game_status == "wait_userans":
    #         if len(userans)>=2 and userans[0] == "!":
    #             self.run_waiting_command(userans.lower()[1])
    #         else:
    #             self.game_status = "checking"
    #             play(self.curr_word)
    #             if userans == self.curr_word.get_item():
    #                 self.lb_result.setText("Yes!")
    #                 self.last_attempt_status = "success"
    #             else:
    #                 self.lb_result.setText("No! Correct is " + self.curr_word.get_item())
    #                 self.last_attempt_status = "failure"           
    #                 self.num_mistakes += 1
 
    # def run_checking_command(self, command_letter):
    #     if command_letter == "p":
    #         play(self.curr_word)
    #     else:
    #         self.le_userans.setText("")

    # def run_waiting_command(self, command_letter):
    #     if command_letter == "p":
    #         play(self.curr_word)
    #         self.le_userans.setText("")
    #     elif command_letter == "e":
    #         self.btn_exit_clicked()
    #     elif command_letter == "n":
    #         self.game_status = "wait_new_word"
    #         self.btn_ok_clicked()
    #     else:
    #         self.le_userans.setText("")
        

def main():

    # create Trainer with words
    trainer = Trainer(words=None)





    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp(trainer)  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
main()