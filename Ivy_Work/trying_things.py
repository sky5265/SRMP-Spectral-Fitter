import matplotlib
import matplotlib.pyplot as plt
#matplotlib.use("Agg")
matplotlib.rcParams['interactive'] == True
import numpy as np

import os
import sys

print(os.path.dirname(sys.executable))
x = np.arange(0, 1, 0.1)
y = x**2

plt.plot(x, y)
plt.show()
