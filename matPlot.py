#!/usr/bin/env python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import math
import json
import ipaddress


class Node:
    def __init__(self, id, stats):
        self.id = id
        self.stats = stats
class NodeList:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.nodes = []
    def initializeList(self):
        #reads from file and puts into a dictionary
        #with open('test.json') as json_file:
            #data = json.load(json_file.read())
        #n1 = Node(1, "I am the first node")
        #self.node.append(n1)
        print("Type")
    def getNodeIds(self):
        ids = [] #ip addresses
        for node in self.nodes:
            ids.append(node.id)
            return ids
    def size(self):
        return len(self.nodes)

df = pd.read_csv('backup.txt', encoding= 'unicode_escape')

sns.set(style="white")
serverImage = OffsetImage(plt.imread('server.png'), zoom=0.05)

for i, row in df.iterrows():
    ip = ipaddress.ip_address(df.loc[i,"Address"])
    df.loc[i,"Address"]  = int(ip)
#print(df.columns)
x = df["Step"]
y = df["Address"]
fig, ax = plt.subplots()
ax.scatter(x, y, marker="None")
ax.plot(x, y)

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

for x0, y0 in zip(x, y):
    ab = AnnotationBbox(serverImage, (x0, y0), frameon=False)
    ax.add_artist(ab)
#    ax.annotate(s='', xy = (x0, y0), arrowprops=dict(arrowstyle="->"))
    
#formatting
ax.set_xlabel('Node Index') #order read
ax.set_ylabel('Node ID') #ip address
#plt.ylim(0,200)
xint = range(min(x)-1, math.ceil(max(x))+2)
plt.xticks(xint)

#textstr = 'IP:192.168.1.1\nType:Server\nRuntime:118ms'
#props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
#ax.text(0.27, 0.63, textstr, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=props)

fig.savefig("output.png")
