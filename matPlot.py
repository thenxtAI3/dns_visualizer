import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="ticks")

# Create a dataset with many short random walks
rs = np.random.RandomState(4)
pos = rs.randint(-1, 2, (20, 5)).cumsum(axis=1)
pos -= pos[:, 0, np.newaxis]
step = np.tile(range(5), 20)
walk = np.repeat(range(20), 5)
df = pd.DataFrame(np.c_[pos.flat, step, walk], columns=["position", "step", "walk"])

# Initialize a grid of plots with an Axes for each walk
grid = sns.FacetGrid(df, col="walk", hue="walk", palette="tab20c", col_wrap=4, height=1.5)

# Draw a line plot to show the trajectory of each random walk
grid.map(plt.plot, "step", "position", marker="o")

# Adjust the tick positions and labels
grid.set(xticks=np.arange(5), yticks=[-3, 3], xlim=(-.5, 4.5), ylim=(-3.5, 3.5))

# Adjust the arrangement of the plots
grid.fig.tight_layout(w_pad=1)
grid.savefig("output.png")


#Simple Grid
# x axis values
# x = [1,2,3]
# corresponding y axis values
# y = [2,4,1]
# plt.plot(x,y)
#plt.savefig("output.png")

#def getImage(path):
#    return OffsetImage(plt.imread(path))
#
#paths = [
#    'server.png',
#    'host.png',]
#
#x = [0,1,2,3,4]
#y = [0,1,2,3,4]
#
#fig, ax = plt.subplots()
#ax.scatter(x, y)
#
#for x0, y0, path in zip(x, y,paths):
#    ab = AnnotationBbox(getImage(path), (x0, y0), frameon=False)
#    ax.add_artist(ab)
