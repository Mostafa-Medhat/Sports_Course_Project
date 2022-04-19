import matplotlib.pyplot as plt
import numpy as np

#define x and y values
x = np.arange(0,10,0.1)
y = x**4

#create plot of values
plt.plot(x,y)

#fill in area between the two lines
plt.fill_between(x, y, np.max(y), color='red', alpha=.5)

plt.show()