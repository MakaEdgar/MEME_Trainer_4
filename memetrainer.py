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




from PyQt5 import QtWidgets
import first_gui
class ExampleApp(QtWidgets.QMainWindow, first_gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()  # Это здесь нужно для доступа к переменным, методам в файле design.py
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self.start_status = "not_started"
        self.game_status = "wait_new_word"
        self.num_mistakes = 0
    
        self.btn_start_stop.clicked.connect(self.btn_start_stop_clicked)  
        self.btn_ok.clicked.connect(self.btn_ok_clicked)  # Выполнить функцию при нажатии кнопки
        self.btn_exit.clicked.connect(self.btn_exit_clicked)
        
        self.le_userans.returnPressed.connect(self.btn_ok.click)

    def btn_exit_clicked(self):
        self.close()

    def finalize(self):
        self.lb_result.setText("")
        self.le_userans.setText("Thank you!")
        self.lb_task.setText("You made mistakes: " + str(self.num_mistakes))
        self.le_userans.setReadOnly(True)
        self.btn_ok.setEnabled(False)
        self.btn_start_stop.setEnabled(False)
        

    def do_nothing(self):
        pass



    def update_labels(self):
        self.lb_result.setText("")
        self.le_userans.setText("")
        self.lb_task.setText(self.curr_word.get_value())
        self.update_stats()

    def update_stats(self):
        self.statusbar.showMessage("Remain: " + str(len(words_remain)) + " "
                                  +"Done: " + str(len(words_done))
                                  +"Mistakes: " + str(self.num_mistakes)
                                  )

    def btn_start_stop_clicked(self):
        if self.start_status is "not_started":
            self.start_status = "started"
            self.btn_start_stop.setText("Pause")
            self.btn_ok_clicked()
        elif self.start_status == "stopped":
            self.start_status = "started"
            self.btn_start_stop.setText("Pause")
        elif self.start_status == "started":
            self.start_status = "stopped"
            self.btn_start_stop.setText("Start")


    def btn_ok_clicked(self):
        userans = self.le_userans.text()

        if self.start_status != "started":
            pass
        
        elif self.game_status == "wait_new_word":
            self.game_status = "wait_userans"
            self.curr_word_index = get_word_index()
            self.curr_word = get_word_by_index(self.curr_word_index)
            self.update_labels()
        
        elif self.game_status == "checking":
            if len(userans)>=2 and userans[0] == "!":
                self.run_checking_command(userans.lower()[1])


            else:
                self.game_status = "wait_userans"
                
                if self.last_attempt_status == "success":
                    remove_finished_word(self.curr_word_index)
                    self.curr_word_index = get_word_index()
                    self.update_labels()
                    if self.curr_word_index != -1:
                        self.curr_word = get_word_by_index(self.curr_word_index)
                    else:
                        self.finalize()
                else:
                    self.last_attempt_status = "failure"
                    self.update_labels()

        elif self.game_status == "wait_userans":
            if len(userans)>=2 and userans[0] == "!":
                self.run_waiting_command(userans.lower()[1])


            else:
                self.game_status = "checking"
                play(self.curr_word)
                if userans == self.curr_word.get_item():
                    self.lb_result.setText("Yes!")
                    self.last_attempt_status = "success"
                else:
                    self.lb_result.setText("No! Correct is " + self.curr_word.get_item())
                    self.last_attempt_status = "failure"           
                    self.num_mistakes += 1
                



    def run_checking_command(self, command_letter):
        if command_letter == "p":
            play(self.curr_word)
        else:
            self.le_userans.setText("")

        

    def run_waiting_command(self, command_letter):
        if command_letter == "p":
            play(self.curr_word)
            self.le_userans.setText("")
        elif command_letter == "e":
            self.btn_exit_clicked()
        elif command_letter == "n":
            self.game_status = "wait_new_word"
            self.btn_ok_clicked()
        else:
            self.le_userans.setText("")
        

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение
main()