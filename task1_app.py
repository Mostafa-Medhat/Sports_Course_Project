import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.pyplot as plt
from scipy.integrate import quad
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
from PIL import Image as im
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit
import sys
from PyQt5.QtGui import QPixmap
import qdarkstyle


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('task1_gui.ui', self)
        self.show()  # Show the GUI

        self.figure_distribtion = Figure( dpi=100)
        self.axes_distribution = self.figure_distribtion.add_subplot()
        self.canvas_distribtion = FigureCanvas(self.figure_distribtion)
        self.canvas_distribtion.figure.set_facecolor("#19232D")
        self.axes_distribution.xaxis.label.set_color('white')
        self.axes_distribution.yaxis.label.set_color('white')
        self.axes_distribution.axes.tick_params(axis="x", colors="white")
        self.axes_distribution.axes.tick_params(axis="y", colors="white")
        self.axes_distribution.axes.set_title("Gaussian Distribution")
        self.axes_distribution.axes.title.set_color('white')
        self.gridLayout_distribution.addWidget(self.canvas_distribtion)

        global mu
        global sigma
        mu = 160  # mean
        sigma = 20  # standard deviation
        global xmin
        global xmax
        global range
        global pdf
        global cdf
        xmin = mu-3*sigma
        xmax = mu+3*sigma
        range = np.linspace(xmin ,xmax, 100)  #range
        normal_dist = norm(mu,sigma)  # normal distribution
        pdf = normal_dist.pdf  # probability density function
        cdf = normal_dist.cdf  # cumulative distribution function

        self.horizontalSlider_above.valueChanged.connect(lambda: self.calculate_CDF())
        self.horizontalSlider_below.valueChanged.connect(lambda: self.calculate_CDF())
        self.radioButton_above.toggled.connect(lambda: self.calculate_CDF())
        self.radioButton_below.toggled.connect(lambda: self.calculate_CDF())




        ###############################################################################
        # plot of probability density function (pdf)
        ###############################################################################
        self.axes_distribution.plot(range, pdf(range))
        self.axes_distribution.set_yticks([])
        self.axes_distribution.axvline(mu, color='C1')
        self.axes_distribution.hlines(0.012, xmin=mu-sigma, xmax=mu+sigma, color='C2')
        self.axes_distribution.legend(('Distribution','Mean=%d'%mu,'Sigma=%d'%sigma), loc='upper right')
        self.axes_distribution.set_xlabel("Ball Hit Speed")
        self.axes_distribution.set_ylabel("Probability Density Function")
        self.canvas_distribtion.draw()

    def calculate_CDF(self):
        ###############################################################################
        # plot showing area under pdf corresponding to Pr(m1 <= m <= m2)
        ################################################################################
        self.axes_distribution.clear()
        self.axes_distribution.plot(range, pdf(range))
        self.axes_distribution.set_yticks([])
        self.axes_distribution.axvline(mu, color='C1')
        self.axes_distribution.hlines(0.012, xmin=mu - sigma, xmax=mu + sigma, color='C2')
        self.axes_distribution.legend(('Distribution', 'Mean=%d' % mu, 'Sigma=%d' % sigma), loc='upper right')
        self.axes_distribution.set_xlabel("Ball Hit Speed")
        self.axes_distribution.set_ylabel("Probability Density Function")
        self.axes_distribution.axes.set_title("Gaussian Distribution")
        self.axes_distribution.axes.title.set_color('white')


        if self.radioButton_above.isChecked():
            speed_min = self.horizontalSlider_above.value()  # lower mass limit
            speed_max = xmax  # upper mass limit
        elif self.radioButton_below.isChecked():
            speed_min = xmin
            speed_max = self.horizontalSlider_below.value()

        Delta_m = np.linspace(speed_min, speed_max, int(speed_max - speed_min))  # mass interval
        # print(Delta_m.size)
        # print(speed_min,"\n",speed_max,"\n",Delta_m)
        # fig = plt.figure()
        # self.axes_distribution.fill_between(Delta_m,pdf(Delta_m),color='red')
        self.axes_distribution.fill_between(Delta_m, pdf(Delta_m), color='C3', alpha=0.2)
        if self.radioButton_above.isChecked():
            probability = 1-cdf(Delta_m)
            self.label_result.setText("%.7f"%(100*probability[0]))


        elif self.radioButton_below.isChecked():
            probability = cdf(Delta_m)
            self.label_result.setText("%.7f"%(100*probability[-1]))

        # print(probability)


        self.canvas_distribtion.draw()


        ################################################################################
        # plot of cumulative distribution function and highlighting values for m1 and m2
        ################################################################################
        # fig = plt.figure()
        # plt.plot(m, P(m), lw=3)
        # plt.hlines(P(m1), min(m), m1, color='C3')        # print("Hello")
        # plt.hlines(P(m2), min(m), m2, color='C3')
        # plt.vlines(m1, 0, P(m1), color='C3')
        # plt.vlines(m2, 0, P(m2), color='C3',
        #            label="$\mathrm{Pr}(%d \le m \le %d) = P_M(%d) - P_M(%d)$ \n\n"
        #                  ".$\hphantom{\mathrm{Pr}(.5\le m\le125)} = %.3f - %.3f$ \n\n"
        #                  ".$\hphantom{\mathrm{Pr}(.5\le m\le125)} \\approx %.3f$"
        #                  % (m1, m2, m1, m2, P(m2), P(m1), P(m2) - P(m1)))
        # plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
        # plt.xlabel("$m$   $\mathrm{[g]}$ \n ice cream mass   ")
        # plt.ylabel("cumulative distribution function \n $P_M(m)$")
        # plt.show()

app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet())
window = MainWindow()
app.exec_()