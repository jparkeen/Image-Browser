import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QSoundEffect


class view(QWidget):
    def __init__(self, Model, width):
        super().__init__()

        # resize the width
        self.width = self.Resize(width)

        # pass the reference of model to self.model
        self.model = Model

        self.title = 'project 2.5 imge browser with sound effect and tags'
        self.mode = 1  # mode 1 is list of thumbnails, mode 2 is one large image
        self.idx = 0  # index to images for display
        self.center = 0  # index to highlight image
        self.w = self.width  # width of full screen image
        self.h = 0.75 * self.w  # height of full screen image
        self.b = 20  # border of full screen image
        self.h1 = self.h / 6.0  # height of thumbnail image
        self.w1 = self.w / 6.0  # width of thumbnail image
        self.b1 = 5  # border of thumbnail image
        self.margintop = self.w / 8.0  # margin of thumbnail to top
        self.marginleft = self.w / 8.0  # margin of thumbnail to left
        self.scaleratio = 0.75  # a parameter for scaling of full screen image

        # create a list of tags labels
        self.taglist = []
        self.tagsLeft = self.w * 0.8
        self.tagsTop = self.h * 0.1
        self.tagsW = self.w * 0.15
        self.tagsH = self.h * 0.1

        # create an editable label
        self.EditLabel = QLabel(self)
        self.EditLabel.setText("Edit the label: ")
        self.EditLabelMarginLeft = self.w * 0.2
        self.EditLabelMarginTop = self.h * 0.87

        self.line = QLineEdit(self)
        self.lineMarginLeft = self.w * 0.33
        self.lineMarginTop = self.h * 0.85
        self.lineWidth = self.w * 0.32
        self.lineHeight = self.h * 0.08

        # create a push button for add label
        self.button1 = QPushButton('Add Tag', self)
        self.button1.clicked.connect(self.Bclick1)
        self.btnTop = self.h * 0.85
        self.btnLeft = self.w * 0.7
        self.btnW = self.w * 0.1
        self.btnH = self.h * 0.08

        # create a push button for save all tags
        self.button2 = QPushButton('Save All Tags', self)
        self.button2.clicked.connect(self.Bclick2)
        self.btnTop2 = self.h * 0.85
        self.btnLeft2 = self.w * 0.82
        self.btnW2 = self.w * 0.15
        self.btnH2 = self.h * 0.08

        # create the label for full scree image
        self.fullabel = QLabel(self)
        # create a mouse click event to clear focus on input text box
        self.fullabel.mousePressEvent = self.mclickFull

        # create a list of labels for 5 thumbnails
        self.labels = []
        for i in range(5):
            self.labels.append(QLabel(self))

        # define mouse click functions to each thumbnail labels
        self.labels[0].mousePressEvent = self.mclick1
        self.labels[1].mousePressEvent = self.mclick2
        self.labels[2].mousePressEvent = self.mclick3
        self.labels[3].mousePressEvent = self.mclick4
        self.labels[4].mousePressEvent = self.mclick5

        # initialize sound effect
        self.sound1 = QSoundEffect()  # for arrow key
        self.sound2 = QSoundEffect()  # for < and >
        self.sound3 = QSoundEffect()  # for mouse click

        # begin the view
        self.initUI()

    # a function to resize the window according to user's input
    def Resize(self, width):
        if int(width) >= 1200:
            return 1200
        elif int(width) <= 600:
            return 600
        else:
            return int(width)

    # initialize the UI
    def initUI(self):
        # set up the window
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, self.w, self.h)

        # set up the full screen label
        self.fullabel.setGeometry(0, 0, self.w * 0.75, self.h * 0.75)
        self.fullabel.setStyleSheet("border: " + str(self.b) + "px solid blue;background-color:grey")

        # set up the edit label for full screen image
        self.line.move(self.lineMarginLeft, self.lineMarginTop)
        self.line.resize(self.lineWidth, self.lineHeight)
        self.EditLabel.move(self.EditLabelMarginLeft, self.EditLabelMarginTop)
        self.EditLabel.setStyleSheet("font:15px")
        self.line.clearFocus()

        # set up the push button for add tag
        self.button1.setGeometry(self.btnLeft, self.btnTop, self.btnW, self.btnH)

        # set up the push button for save all tags
        self.button2.setGeometry(self.btnLeft2, self.btnTop2, self.btnW2, self.btnH2)

        # set up the thumbnail labels
        for i in range(5):
            self.labels[i].setGeometry(self.w1 * 0.45 + self.w1 * i, self.h * 0.4, self.w1, self.h1)
            self.labels[i].setStyleSheet("border: " + str(self.b1) + "px solid green;background-color:grey")

        self.DisplayImg()


        # a function to rescale the image

    def RescaleImg(self, pixmap):
        # rescale for full screen label image
        if self.mode == 2:
            if pixmap.size().height() / float(self.h) > pixmap.size().width() / float(self.w):
                pixmap = pixmap.scaledToHeight((self.h - 2 * self.b) * self.scaleratio)  # rescale according to height
            else:
                pixmap = pixmap.scaledToWidth((self.w - 2 * self.b) * self.scaleratio)  # rescale according to width
        # rescale for thumbnail label image
        else:
            if pixmap.size().height() / float(self.h1) > pixmap.size().width() / float(self.w1):
                pixmap = pixmap.scaledToHeight(self.h1)  # rescale according to height
            else:
                pixmap = pixmap.scaledToWidth(self.w1)  # rescale according to width
        return pixmap

    # a function to display the pixmap in full size or in thumbnail list
    def DisplayImg(self):

        # determine mode
        if self.mode == 2:
            # print("show the full size image")
            # hide the thumbnail list
            for i in range(5):
                self.labels[i].hide()

            # set up the tag label list for full screen image
            for tag in self.taglist:
                tag.hide()
            self.taglist = []  # clear previous tag list

            taglen = len(self.model.tags[self.idx % len(self.model.imgs)])
            for i in range(taglen):
                self.taglist.append(QLabel(self))
                self.taglist[i].setText(self.model.tags[self.idx % len(self.model.tags)][i])
                self.taglist[i].setGeometry(self.tagsLeft, self.tagsTop + i * self.tagsH, self.tagsW, self.tagsH)
                self.taglist[i].setStyleSheet("font: 20px")
                self.taglist[i].show()  # show the tag label

            # show the full screen image
            self.fullabel.show()
            self.line.show()
            self.EditLabel.show()
            self.button1.show()
            self.button2.show()

            # rescale the image as needed
            pixmap = self.RescaleImg(self.model.imgs[self.idx % len(self.model.imgs)])

            # load image onto label
            self.fullabel.setPixmap(pixmap)

            # apply style to label
            self.fullabel.setAlignment(Qt.AlignCenter)
            self.fullabel.setStyleSheet("border: " + str(self.b) + "px solid red;background-color:grey")

            self.show()

        else:
            # hide the full screen image and other tags
            self.fullabel.hide()
            self.line.hide()
            self.EditLabel.hide()
            self.button1.hide()
            self.button2.hide()
            for tag in self.taglist:
                tag.hide()

            # show the thumbnails
            for i in range(5):
                self.labels[i].show()
                self.labels[i].setPixmap(self.RescaleImg(self.model.imgs[(self.idx + i) % len(self.model.imgs)]))
                self.labels[i].setAlignment(Qt.AlignCenter)
                #                print("idx: ", self.idx,"center: ", self.center)
                #                print((self.idx+i) % 5, self.center)
                if i == self.center:
                    self.labels[i].setStyleSheet("border: " + str(self.b1) + "px solid red;background-color:grey")
                else:
                    self.labels[i].setStyleSheet("border: " + str(self.b1) + "px solid green;background-color:grey")

            self.show()

            # add tag button click function, append user input to tag file

    def Bclick1(self, event):
        self.model.tags[self.idx % len(self.model.tags)].append(self.line.text())
        self.taglist.append(QLabel(self))
        self.taglist[len(self.taglist) - 1].setText(self.line.text())
        self.DisplayImg()

    # save tag button click function
    def Bclick2(self, event):
        fout = open(self.model.tagpath + self.model.taglist[self.idx % len(self.model.taglist)], 'w')
        #        print(self.model.tags[self.idx % len(self.model.tags)])
        for line in self.model.tags[self.idx % len(self.model.tags)]:
            fout.write(line + '\n')
        fout.close()


        # click on the full window image to clear focus on qline

    def mclickFull(self, event):
        self.line.clearFocus()

    def mclick1(self, event):
        self.ShortSound3()
        #        print("label 1 clicked!!!")
        self.mode = 2
        self.center = 0
        self.idx += self.center
        self.DisplayImg()

    def mclick2(self, event):
        #        print("label 2 clicked!!!")
        self.ShortSound3()
        self.mode = 2
        self.center = 1
        self.idx += self.center
        self.DisplayImg()

    def mclick3(self, event):
        #        print("label 3 clicked!!!")
        self.ShortSound3()
        self.mode = 2
        self.center = 2
        self.idx += self.center
        self.DisplayImg()

    def mclick4(self, event):
        #        print("label 4 clicked!!!")
        self.ShortSound3()
        self.mode = 2
        self.center = 3
        self.idx += self.center
        self.DisplayImg()

    def mclick5(self, event):
        #        print("label 5 clicked!!!")
        self.ShortSound3()
        self.mode = 2
        self.center = 4
        self.idx += self.center
        self.DisplayImg()

    def LeftArrowEvent(self):
        if self.mode == 1:
            self.center -= 1
            if self.center < 0:
                self.idx -= 5
                self.center = 4
        else:
            self.idx -= 1
        self.DisplayImg()

    def RightArrowEvent(self):
        if self.mode == 1:
            self.center += 1
            if self.center >= 5:
                self.idx += 5
                self.center = 0
        else:
            self.idx += 1
        self.DisplayImg()

    def DownArrowEvent(self):
        if self.mode == 1:
            return
        # change to thumbnail list
        self.mode = 1
        self.idx -= 2
        self.center = 2
        self.DisplayImg()

    def UpArrowEvent(self):
        if self.mode == 2:
            return
        # change to full image
        self.mode = 2
        self.idx += self.center
        self.DisplayImg()

    def SmallerThanEvent(self):
        if self.mode == 2:
            return
        self.idx -= 5
        self.center = 0
        self.DisplayImg()

    def LargerThanEvent(self):
        if self.mode == 2:
            return
        self.idx += 5
        self.center = 0
        self.DisplayImg()

        # a short for arrow keypress event

    def ShortSound1(self):
        self.sound1.setSource(QUrl.fromLocalFile(os.path.join('sounds', '191617__dwsd__jhd-bd-35.wav')))
        self.sound1.play()

        # a short sound for < and > key event

    def ShortSound2(self):
        self.sound2.setSource(QUrl.fromLocalFile(os.path.join('sounds', '195937__michimuc2__short-wind-noise.wav')))
        self.sound2.play()

        # a short sound for mouse click

    def ShortSound3(self):
        self.sound3.setSource(QUrl.fromLocalFile(os.path.join('sounds', 'keyevent2.wav')))
        self.sound3.play()

    def keyPressEvent(self, event):
        #        print(event.key())
        #        print(event)
        #        print(event.modifiers())

        if event.key() == 16777234:  # left arrow key
            self.ShortSound1()
            self.LeftArrowEvent()
        elif event.key() == 16777236:  # right arrow key
            self.ShortSound1()
            self.RightArrowEvent()
        elif event.key() == 16777237:  # down arrow key
            self.ShortSound1()
            self.DownArrowEvent()
        elif event.key() == 16777235:  # up arrow key
            self.ShortSound1()
            self.UpArrowEvent()
        elif event.modifiers():
            #            print(event.key())
            if event.key() == 60:  # less than key
                self.ShortSound2()
                self.SmallerThanEvent()
            elif event.key() == 62:  # greater than key
                self.ShortSound2()
                self.LargerThanEvent()
        else:
            print("unknown key")