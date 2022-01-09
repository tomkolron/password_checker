import sys
import hashlib
import os

def hash_pswrd(pswrd):
    hashed_pswrd = hashlib.sha1(pswrd.encode()).hexdigest()
    return hashed_pswrd


with open("temp.txt",'w') as f:
    pass

from PyQt5.QtWidgets import (
        QApplication, QLineEdit, QWidget, QLabel, QPushButton, QInputDialog
    )
from PyQt5.QtCore import pyqtSlot, QRect, QCoreApplication

class MainPage(QWidget):
    def __init__(self, title=" "):
        super().__init__()  # inherit init of QWidget
        self.title = title
        self.left = 250
        self.top = 250
        self.width = 200
        self.height = 150
        self.widget()

    def widget(self):
        # window setup
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        ## use above line or below
        self.resize(self.width, self.height)
        self.move(self.left, self.top)

        # add title
        self.title = QLabel(self, text='enter your password here: ')
        self.title.setGeometry(QRect(10, 5, 180, 50))
        self.title.setWordWrap(True) # allow word-wrap

        # add password input
        self.input = QLineEdit(self)
        self.input.setEchoMode(QLineEdit.Password)
        self.input.setGeometry(QRect(20, 50, 150, 20))

        #add submit button
        self.submit = QPushButton(self, text='submit')
        self.submit.setGeometry(QRect(65, 80, 60, 25))
        self.submit.clicked.connect(self.click)

        self.data = QLabel(self, text='')
        self.data.setGeometry(QRect(20, 100, 180, 50))

        self.show()

    @pyqtSlot()
    def click(self):
        self.data.setText('loading ...')
        pswrd = self.input.text()
        hashed_pswrd = hash_pswrd(pswrd)
        hash_start = hashed_pswrd[0:5]
        breaches_found = 0

        os.system('curl https://api.pwnedpasswords.com/range/' + hash_start + ' -o temp.txt')

        with open('./temp.txt') as f:
            index = 0
            for line in f:
                pswrd_from_database_with_number = hash_start + line.strip().lower()
                pswrd_from_database = line.strip().lower()[0:35]
                pswrd_from_database = hash_start + pswrd_from_database
                print(str(index) + ': ' + pswrd_from_database_with_number)
                if hashed_pswrd == pswrd_from_database:
                    breaches_found = pswrd_from_database_with_number[41:len(pswrd_from_database_with_number)]
                    break
                index += 1
        if breaches_found == 0:
            print('0 data breaches found')
        else: 
            print(str(breaches_found) + ' data breaches found')
        self.data.setText(str(breaches_found) + ' data breaches found')
        
        with open("temp.txt",'w') as f:
            pass

    @pyqtSlot()
    def exit_window(self):
        QCoreApplication.instance().quit()

def main():
    app = QApplication(sys.argv)
    w = MainPage(title="password checker")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()