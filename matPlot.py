#!/usr/bin/env python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import math
import json

class Node:
    def __init__(self, id, address):
        self.id = id
        self.address = address
    def __repr__(self):
        return "Node id:% s address:% s" % (self.id, self.address)
class NodeList:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.nodes = []
        self.data = {}
    def initializeList(self):
        #reads from file and puts into a dictionary
        with open(self.path_to_file) as json_file:
            self.data = json.load(json_file)
        ip_mapping = {}
        self.nodes.append(Node(1, self.data['google.com.']['clients_ipv4'][0]))
        ip_mapping[self.data['google.com.']['clients_ipv4'][0]] = 1
        queries = self.data['google.com.']['queries']
        for query in queries:
            responses = query['responses']
            for ip, message in responses.items():
                if ip not in ip_mapping.keys():
                    ip_mapping[ip] = len(ip_mapping)+1
                    self.nodes.append(Node(ip_mapping[ip], ip))
                print(len(ip_mapping))
        print(self.nodes)
    def getNodeIds(self):
        ids = []
        for node in self.nodes:
            ids.append(node.id)
        return ids
    def getAddress(self):
        addresses = []
        for node in self.nodes:
            addresses.append(node.address)
        return addresses
    def getCoordinates(self):
        coordinates = []
        for node in self.nodes:
            coordinates.append((node.id,node.address))
        print(coordinates)
    def size(self):
        return len(self.nodes)
sample = NodeList("test.json")
sample.initializeList()

sns.set(style="white")
serverImage = OffsetImage(plt.imread('server.png'), zoom=0.05)

x = sample.getNodeIds()
y = sample.getAddress()
fig, ax = plt.subplots()
ax.scatter(x, y, marker="None")
ax.plot(x, y)

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

for x0, y0 in zip(x, y):
    ab = AnnotationBbox(serverImage, (x0, y0), frameon=False)
    ax.add_artist(ab)

ax.set_xlabel('Node ID') #order read
ax.set_ylabel('Node Address') #ip address
xint = range(min(x)-1, math.ceil(max(x))+2)
plt.xticks(xint)
#plt.ylim(0.0.0.0, 255.255.255.255)

fig.savefig("output.png")

