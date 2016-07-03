#!/usr/bin/python
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

mpl.rcParams['legend.fontsize'] = 20

fig = plt.figure()
ax = fig.gca(projection='3d')

z = [0,20,20,0,0,0,20,20]
x = [-10,-10,10,10,10,-10,-10,10]
y = [2,2,2,2,-18,-18,-18,-18]
ax.plot(x, y, z, label='parametric curve')
ax.legend()

plt.show()
