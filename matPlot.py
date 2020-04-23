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
    def __repr__(self):
        return "Node id:% s stats:% s" % (self.id, self.stats)
class NodeList:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.nodes = []
        self.data = {}
    def initializeList(self):
        #reads from file and puts into a dictionary
        with open(self.path_to_file) as json_file:
            self.data = json.load(json_file)
        n1 = Node(1, self.data['google.com.']['clients_ipv4'][0])
        self.nodes.append(n1)
        i=2
        queries = self.data['google.com.']['queries']
        for query in queries:
            #getting the first ip address from each response
            ipResp = list(query['responses'].keys())[0]
            n = Node(i, ipResp)
            self.nodes.append(n)
            i+=1
        print(self.nodes)
    def getNodeIds(self):
        ids = []
        for node in self.nodes:
            ids.append(node.id)
        print(ids)
    def getCoordinates(self):
        coordinates = []
        for node in self.nodes:
            coordinates.append((node.id,node.stats))
        print(coordinates)
    def size(self):
        return len(self.nodes)
sample = NodeList("test.json")
sample.initializeList()
sample.getNodeIds()
sample.getCoordinates()


#df = pd.read_csv('backup.txt', encoding= 'unicode_escape')
#
#sns.set(style="white")
#serverImage = OffsetImage(plt.imread('server.png'), zoom=0.05)
#
##for i, row in df.iterrows():
##    ip = ipaddress.ip_address(df.loc[i,"Address"])
##    df.loc[i,"Address"]  = int(ip)
##print(df.columns)
#x = df["Step"]
#y = df["Address"]
#fig, ax = plt.subplots()
#ax.scatter(x, y, marker="None")
#ax.plot(x, y)
#
#props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
#
#for x0, y0 in zip(x, y):
#    ab = AnnotationBbox(serverImage, (x0, y0), frameon=False)
#    ax.add_artist(ab)
##    ax.annotate(s='', xy = (x0, y0), arrowprops=dict(arrowstyle="->"))
#
##formatting
#ax.set_xticklabels(df[0])
#ax.set_yticklabels(df[1])
#ax.set_xticks(df["Step"])
#ax.set_yticks(df["Address"])
#ax.set_xlabel('Node Index') #order read
#ax.set_ylabel('Node ID') #ip address
##plt.ylim(0,200)
#xint = range(min(x)-1, math.ceil(max(x))+2)
#plt.xticks(xint)
#
##textstr = 'IP:192.168.1.1\nType:Server\nRuntime:118ms'
##props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
##ax.text(0.27, 0.63, textstr, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=props)
#
#fig.savefig("output.png")



