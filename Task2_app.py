from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QFileDialog, QGraphicsView
from PyQt5.uic.properties import QtCore
import sys
from math import *
import math


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('Simulator3.ui', self)
        self.show()
        self.calcbotton.clicked.connect(self.calc)

    def calc(self):
        self.maxhightbox.clear()
        self.hightatgoalbox.clear()

        distance = int(self.distancebox.toPlainText())
        angle = int(self.anglebox.toPlainText())

        initial_velocity = int(self.velocitybox.toPlainText())

        time_at_maxheight = (initial_velocity * math.sin(math.radians(angle))) / (9.8)

        max_height = initial_velocity * time_at_maxheight * math.sin(math.radians(angle)) - 0.5 * 9.8 * (time_at_maxheight ** 2)

        time_at_goal = distance / (initial_velocity * math.cos(math.radians(angle)))

        height_at_goal = initial_velocity * time_at_goal * math.sin(math.radians(angle)) - 0.5 * 9.8 * (time_at_goal ** 2)

        if height_at_goal <= 0:
            height_at_goal = 0

        print("max hight", str(round(max_height, 3)))
        print("hight at gool ", str(round(height_at_goal, 3)))

        self.maxhightbox.append(str(round(max_height, 3)))
        self.hightatgoalbox.append(str(round(height_at_goal, 3)))


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()