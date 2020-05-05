#!/usr/bin/env python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import math
import json
from ipaddress import IPv4Address, AddressValueError
import socket, struct

def is_ipv4_only(addr): #filtering for ipv6
    try:
        IPv4Address(addr.split('/')[0])
        return True
    except AddressValueError:
        return False
def ip2long(ip):
    packedIP = socket.inet_aton(ip)
    return struct.unpack("!L", packedIP)[0]

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
        self.level = []
    def initializeList(self):
        #reads from file and puts into a dictionary
        with open(self.path_to_file) as json_file:
            self.data = json.load(json_file)
            del self.data['_meta._dnsviz.']
        self.levels = list(self.data)
        domainName = self.data[self.levels[len(self.levels)-1]]
        ip_mapping = {}
        self.nodes.append(Node(1, ip2long(domainName['clients_ipv4'][0]))) #self.data[self.levels[pineapple-1]]
        ip_mapping[ip2long(domainName['clients_ipv4'][0])] = 1
        queries = domainName['queries']
        for query in queries:
            responses = query['responses']
            for ip, message in responses.items():
                if is_ipv4_only(ip):
                    if ip not in ip_mapping.keys():
                        ip_mapping[ip] = len(ip_mapping)+1
                        self.nodes.append(Node(ip_mapping[ip], ip2long(ip)))
#                    print(len(ip_mapping))
        self.nodes.append(Node(3, ip2long('100.168.1.200')))
        self.nodes.append(Node(3, ip2long('192.168.1.254')))
        self.nodes.append(Node(3, ip2long('255.255.255.0')))
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
        return coordinates
    def size(self):
        return len(self.nodes)
        
if __name__ == '__main__':
    sample = NodeList("recursive.json")
    sample.initializeList()
    sample.getCoordinates()

    sns.set(style="white")
    clientImage = OffsetImage(plt.imread('client.png'), zoom=0.05)
    serverImage = OffsetImage(plt.imread('server.png'), zoom=0.05)
    
    x = sample.getNodeIds()
    y = sample.getAddress()
    fig, ax = plt.subplots()
    sc = plt.scatter(x, y, marker="+", color='#999999')
#    ax.scatter(x, y, marker="None")
    ax.plot(x, y)

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points", bbox=props, arrowprops=dict(arrowstyle="->"))

    firstNode = True
    for x0, y0 in zip(x, y):
        if firstNode:
            ab = AnnotationBbox(clientImage, (x0, y0), frameon=False)
            ax.add_artist(ab)
            firstNode = False
        else:
            ab = AnnotationBbox(serverImage, (x0, y0), frameon=False)
            ax.add_artist(ab)

    ax.set_title('Recursive Query') #fontdict={'fontsize': 12, 'fontweight': 'medium'}
    ax.set_xlabel('Node ID') #order read
    ax.set_ylabel('Node Address', labelpad=15) #ip address
    xint = range(min(x)-1, math.ceil(max(x))+2)
    plt.xticks(xint)
    
    def update_annot(ind):
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        print(annot.xy)
        text = "sample"
        annot.set_text(text)
#        annot.get_bbox_patch().set_facecolor(cmap(norm(sample.getNodeIds()))) #getting annnotate and getting that patch
        annot.get_bbox_patch().set_alpha(0.4) #of the specific annotation box ut gets the value
        
    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()
    fig.canvas.mpl_connect("motion_notify_event", hover)
#    fig.savefig("output.png",bbox_inches='tight')
    plt.show()
