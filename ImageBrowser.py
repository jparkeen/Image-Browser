
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QSoundEffect


# import the model class from Model.py
from model import model

# import the view class from View.py
from view import view

def Usage():
    print("Usage: Python3 ImageBrowser.py Width")
    print("If width is not provided, default width will be used.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    imgmodel = model()
    # view the models
    defaultWidth = 800
    if len(sys.argv) == 1:
        ImgView = view(imgmodel, defaultWidth)
    elif len(sys.argv) == 2:
        ImgView = view(imgmodel, sys.argv[1])
    else:
        Usage()
        exit()

    sys.exit(app.exec_())