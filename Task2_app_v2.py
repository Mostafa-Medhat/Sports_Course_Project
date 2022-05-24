import numpy as np
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDesktopWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('task2_gui_V2.ui', self)

        ##### Center The Window ########
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.show()  # Show the GUI

        # make the structre of the canvas
        self.figure_draw = Figure(dpi=100)
        self.axes_draw = self.figure_draw.add_subplot()
        self.canvas_draw = FigureCanvas(self.figure_draw)
        self.axes_draw.axes.set_title("Projectile Motion")
        self.axes_draw.set_xlabel("Distance")
        self.axes_draw.set_ylabel("Height")
        self.figure_draw.tight_layout(pad=2.20)
        self.gridLayout_draw.addWidget(self.canvas_draw)

        self.pushButton_calculate.clicked.connect(lambda: self.calculateHeights())

    def calculateHeights(self):
        distance = self.horizontalSlider_distance.value()
        initial_velocity = self.horizontalSlider_velocity.value()
        angle = np.radians(self.dial_angle.value())
        g = 9.8


        ############ Plotting Parameters #############
        self.axes_draw.clear()
        self.axes_draw.axes.set_title("Projectile Motion")
        tmax = ((2 * initial_velocity) * np.sin(angle)) / g   # Time of Flight
        time_range = np.linspace(0, tmax, 100)  # create time range w/ 100 points
        x = ((initial_velocity * time_range) * np.cos(angle))  # distance at each time
        y = ((initial_velocity * time_range) * np.sin(angle)) - ((0.5 * g) * (time_range ** 2))   # height at each time


        ############### Caculate The Desired Heights ##############
        time_at_maxheight = (initial_velocity * np.sin(angle)) / (g)
        max_height = initial_velocity * time_at_maxheight * np.sin(angle) - 0.5 * g * (time_at_maxheight ** 2)
        horizontal_distance_of_max_height=initial_velocity * time_at_maxheight * np.cos(angle)

        time_at_goal = distance / (initial_velocity * np.cos(angle))
        height_at_goal = initial_velocity * time_at_goal * np.sin(angle) - 0.5 * g * (time_at_goal ** 2)
        if height_at_goal <= 0:
            height_at_goal = 0


        ######## Draw the Canvas #########
        self.axes_draw.plot(x, y)
        self.axes_draw.axvline(horizontal_distance_of_max_height, color='C1')
        self.axes_draw.hlines(y=max_height, xmin=0, xmax=horizontal_distance_of_max_height, color='C1')
        self.axes_draw.axvline(distance, color='C2')
        self.axes_draw.hlines(y=height_at_goal, xmin=0, xmax=distance, color='C2')
        self.axes_draw.legend(('Motion', 'Max Height= %.3f m' % max_height, 'Height at Goal= %.3f m' % height_at_goal), loc='upper right')
        self.axes_draw.set_xlabel("Distance")
        self.axes_draw.set_ylabel("Height")
        self.canvas_draw.draw()

        ########## Printing Desired Heights #############
        self.label_maximum_height_value.setText("%.3f" %(max_height))
        self.label_goal_ball_height_value.setText("%.3f" %(height_at_goal))



app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()
