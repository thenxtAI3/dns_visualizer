import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import math

#index_col treats the first column of the dataset as the id, written as a backup
df = pd.read_csv('backup.txt', index_col=0, encoding= 'unicode_escape')

#reading from a data file, cross your fingers and hope it works
#df = pd.read_csv('temp.txt', delimiter= '\s+', index_col = 1, skiprows=[0,1,2,3,17,32,33,34,35,36], encoding= 'unicode_escape')

sns.set(style="white")
#sns_plot = sns.lmplot(x='Attack', y='Defense', data=df, fit_reg=False)

serverImage = OffsetImage(plt.imread('server.png'), zoom=0.05)
x = df["Step"]
y = df["Time"]
fig, ax = plt.subplots()
ax.scatter(x, y, marker="None")
ax.plot(x, y)

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

for x0, y0 in zip(x, y):
    ab = AnnotationBbox(serverImage, (x0, y0), frameon=False)
    ax.add_artist(ab)
#    ax.annotate(s='', xy = (x0, y0), arrowprops=dict(arrowstyle="->"))
    
#formatting
ax.set_xlabel('Steps')
ax.set_ylabel('Time(ms)')
plt.ylim(0,200)
xint = range(min(x)-1, math.ceil(max(x))+2)
plt.xticks(xint)

#plt.quiver(x[:-1], y[:-1], x[1:]-x[:-1], y[1:]-y[:-1], y[1:]-x[:-1], scale_units='xy', angles='xy', scale=1)

textstr = 'IP:192.168.1.1\nType:Server\nRuntime:118ms'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.27, 0.63, textstr, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=props)

#sns_plot.savefig("output.png")
fig.savefig("output.png")
