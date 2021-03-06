import sys
import numpy as np
import qdarkstyle
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDesktopWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.stats import norm


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('task1_gui.ui', self)

        #### Center The Window ####
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.show()  # Show the GUI

        # make the structre of the canvas
        self.figure_distribtion = Figure(dpi=100)
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
        range = np.linspace(xmin ,xmax, int(xmax-xmin))  #range
        normal_dist = norm(mu,sigma)  # normal distribution
        pdf = normal_dist.pdf  # probability density function
        cdf = normal_dist.cdf  # cumulative distribution function

        self.horizontalSlider_above.setMinimum(xmin)
        self.horizontalSlider_above.setMaximum(xmax)

        self.horizontalSlider_below.setMinimum(xmin)
        self.horizontalSlider_below.setMaximum(xmax)



        self.horizontalSlider_above.valueChanged.connect(lambda: self.calculate_CDF())
        self.horizontalSlider_below.valueChanged.connect(lambda: self.calculate_CDF())
        self.radioButton_above.toggled.connect(lambda: self.calculate_CDF())
        self.radioButton_below.toggled.connect(lambda: self.calculate_CDF())




        ###############################################################################
        # plot of probability density function (pdf)
        ###############################################################################
        self.axes_distribution.plot(range, pdf(range))
        # self.axes_distribution.set_yticks([])
        self.axes_distribution.axvline(mu, color='C1')
        self.axes_distribution.hlines(0.012, xmin=mu-sigma, xmax=mu+sigma, color='C2')
        self.axes_distribution.legend(('Distribution', 'Mean=%d km/h' % mu, 'Sigma=%d km/h' % sigma), loc='upper right')
        self.axes_distribution.set_xlabel("Ball Hit Speed")
        self.axes_distribution.set_ylabel("Probability Density Function")
        self.canvas_distribtion.draw()

    def calculate_CDF(self):
        ###############################################################################
        # plot showing area under pdf corresponding to Pr(s1 <= m <= s2)
        ################################################################################
        self.axes_distribution.clear()
        self.axes_distribution.plot(range, pdf(range))
        # self.axes_distribution.set_yticks([])
        self.axes_distribution.axvline(mu, color='C1')
        self.axes_distribution.hlines(0.012, xmin=mu - sigma, xmax=mu + sigma, color='C2')
        self.axes_distribution.legend(('Distribution', 'Mean=%d km/h' % mu, 'Sigma=%d km/h' % sigma), loc='upper right')
        self.axes_distribution.set_xlabel("Ball Hit Speed")
        self.axes_distribution.set_ylabel("Probability Density Function")
        self.axes_distribution.axes.set_title("Gaussian Distribution")
        self.axes_distribution.axes.title.set_color('white')

        if self.radioButton_below.isChecked():
            speed_min = xmin
            speed_max = self.horizontalSlider_below.value()

        elif self.radioButton_above.isChecked():
            speed_min = self.horizontalSlider_above.value()  # lower mass limit
            speed_max = xmax  # upper mass limit

        if (speed_max == speed_min):
            Delta_m = np.linspace(speed_min, speed_max, 1)  # mass interval
        else:
            Delta_m = np.linspace(speed_min, speed_max, int(speed_max - speed_min))  # mass interval

        self.axes_distribution.fill_between(Delta_m, pdf(Delta_m), color='C3', alpha=0.2)

        if self.radioButton_below.isChecked():
            if(speed_max == speed_min):
                probability = pdf(Delta_m)
            else:
                probability = cdf(Delta_m)
            self.label_result.setText("%.4f" % (100 * probability[-1]))

        elif self.radioButton_above.isChecked():
            if (speed_min == speed_max):
                probability = pdf(Delta_m)
            else:
                probability = 1-cdf(Delta_m)
            self.label_result.setText("%.4f"%(100*probability[0]))

        # print(probability)


        self.canvas_distribtion.draw()

app = QtWidgets.QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet())
window = MainWindow()
app.exec_()