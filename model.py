import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QSoundEffect


class model():
    def __init__(self):
        #self.datapath = os.getcwd() + "/data/"
        #self.tagpath = os.getcwd() + "/tags/"
        self.imglist = os.listdir('data')
        self.taglist = os.listdir('tags')

        # create a list to hold all img models
        self.imgs = []
        self.tags = []
        for i in range(len(self.imglist)):
            self.imgs.append(QPixmap('data/' + self.imglist[i]))
            fin = open('tags/' + self.taglist[i])
            lines = fin.read().splitlines()
            fin.close()
            self.tags.append(lines)
