import math
import sys
from PyQt5 import QtWidgets, uic


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('task2_gui.ui', self)
        self.show()  # Show the GUI

        self.pushButton_calculate.clicked.connect(lambda: self.calculateHeights())

    def calculateHeights(self):
        distance = self.horizontalSlider_distance.value()
        initial_velocity = self.horizontalSlider_velocity.value()
        angle = self.dial_angle.value()

        time_at_maxheight = (initial_velocity * math.sin(math.radians(angle))) / (9.8)

        max_height = initial_velocity * time_at_maxheight * math.sin(math.radians(angle)) - 0.5 * 9.8 * (
                    time_at_maxheight ** 2)

        time_at_goal = distance / (initial_velocity * math.cos(math.radians(angle)))

        height_at_goal = initial_velocity * time_at_goal * math.sin(math.radians(angle)) - 0.5 * 9.8 * (time_at_goal ** 2)

        if height_at_goal <= 0:
            height_at_goal = 0


        self.label_maximum_height_value.setText("%.3f" %(max_height))
        self.label_goal_ball_height_value.setText("%.3f" %(height_at_goal))


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()
