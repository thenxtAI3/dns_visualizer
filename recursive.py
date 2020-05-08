#!/usr/bin/env python
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import math
import json
from ipaddress import IPv4Address, AddressValueError
import socket, struct
import sys

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
        self.longAddress = ip2long(address)
        self.coordinates = (-1, -1)
        self.server_type = ""
        self.response_time = ""
        self.msg_size = ""
        self.resolution = "" #. com. google.com
        
    #getters
    def get_coordinates(self):
        return (self.id, self.longAddress)

    def get_server_type(self):
        return self.server_type

    def get_response_time(self):
        return self.response_time

    def get_msg_size(self):
        return self.msg_size

    def get_resolution_process(self):
        return self.resolution

    #setters
    def set_coordinates(self, x, y):
        self.coordinates = (x, y)

    def set_server_type(self, type):
        self.server_type = type

    def set_response_time(self, time):
        self.response_time = time

    def set_msg_size(self, msg_size):
        self.msg_size = msg_size

    def set_resolution_process(self, process):
        self.resolution = process
        
    def __repr__(self):
        return "Node id:% s address:% s" % (self.id, self.address)
class NodeList:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.nodes = []
        self.temp_nodes = []
        self.data = {}
        self.level = []
    def initializeList(self):
        #reads from file and puts into a dictionary
        with open(self.path_to_file) as json_file:
            self.data = json.load(json_file)
            del self.data['_meta._dnsviz.']
        self.level = list(self.data)
        domainName = self.data[self.level[len(self.level)-1]]
        ip_mapping = {}
        self.nodes.append(Node(1, domainName['clients_ipv4'][0]))
        ip_mapping[domainName['clients_ipv4'][0]] = 1
        queries = domainName['queries']
        for query in queries:
            responses = query['responses']
            for ip, message in responses.items():
                if is_ipv4_only(ip):
                    if ip not in ip_mapping.keys():
                        ip_mapping[ip] = len(ip_mapping)+1
                        self.nodes.append(Node(ip_mapping[ip], ip))
        self.nodes.append(Node(3, '255.255.255.200'))
        self.nodes.append(Node(3, '192.168.1.254'))
        self.nodes.append(Node(3, '100.100.1.200'))
        print(self.nodes)
        
    #create Node objects from data, set Node class variables
    def create_Nodes(self, data):
        #indexing into responses to get time and message size
        responses = self.data[self.level[-1]]['queries'][0]['responses']
        outerIP = list(responses)[0]
        innerIP = list(responses[outerIP])[0]
        
        client = self.nodes[0]
        recursive = self.nodes[1]
        root = self.nodes[2]
        tld = self.nodes[3]
        auth = self.nodes[4]
        
        #set resolver server node statistics
        client.set_server_type("Client")

        # #set recursive server node statistics
        recursive.set_server_type("Recursive")
        recursive.set_response_time(responses[outerIP][innerIP]['time_elapsed'])
        recursive.set_msg_size(responses[outerIP][innerIP]['msg_size'])
        recursive.set_resolution_process(' -> '.join(data.keys()))
        
        root.set_server_type("Root")
        root.set_resolution_process(self.level[0])
        
        tld.set_server_type("TLD")
        tld.set_resolution_process(self.level[1])
        
        auth.set_server_type("Authoratative")
        auth.set_resolution_process(self.level[2])

        self.temp_nodes.append(client)
        self.temp_nodes.append(recursive)
        self.temp_nodes.append(root)
        self.temp_nodes.append(tld)
        self.temp_nodes.append(auth)

    def get_node_from_hover(self, x, y) :
        for node in self.nodes:
            if node.get_coordinates() == (x,y):
                return node
                
    def getNodeIds(self):
        ids = []
        for node in self.nodes:
            ids.append(node.id)
        return ids
    def getAddress(self):
        addresses = []
        for node in self.nodes:
            addresses.append(node.longAddress)
        return addresses
    def getCoordinates(self):
        coordinates = []
        for node in self.nodes:
            coordinates.append((node.id,node.longAddress))
        return coordinates
    def size(self):
        return len(self.nodes)
        
def update_annot(ind):
    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    node = sample.get_node_from_hover(pos[0], pos[1])
    if pos[0] == 1.0:
        text = "IP Address: " + node.address + "\nServer Type: " + node.server_type
    elif pos[0] == 2.0:
        text = "IP Address: " + node.address + "\nServer Type: " + node.server_type + "\nResponse Time: " + str(node.response_time) + "\nMessage Size: " + str(node.msg_size) + "\nResolution Process: " + node.resolution
    else:
        text = "\nServer Type: " + node.server_type + "\nResolution Process: " + node.resolution
    annot.set_text(text)
    annot.get_bbox_patch().set_facecolor('#BDD4B2')
    annot.get_bbox_patch().set_alpha(0.4)  # of the specific annotation box ut gets the value
    
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
if __name__ == '__main__':
    sample = NodeList("rec.json")
    sample.initializeList()
    rose = sample.getCoordinates()
    sample.create_Nodes(sample.data)

    sns.set(style="white")
    clientImage = OffsetImage(plt.imread('host.png'), zoom=0.05)
    serverImage = OffsetImage(plt.imread('server.png'), zoom=0.05)
    greyImage = OffsetImage(plt.imread('grey.png'), zoom=0.05)
    
    x = sample.getNodeIds()
    y = sample.getAddress()
    fig, ax = plt.subplots(figsize=(9, 6))
    sc = plt.scatter(x, y, marker="s", color='#FFFFFF', s = 400)

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points", bbox=props, arrowprops=dict(arrowstyle="->"))
            
    for x0, y0 in zip(x, y):
        if x0 is 1:
            ab = AnnotationBbox(clientImage, (x0, y0), frameon=False)
            ax.add_artist(ab)
        elif x0 is 2:
            ab = AnnotationBbox(serverImage, (x0, y0), frameon=False)
            ax.add_artist(ab)
        else:
            ab = AnnotationBbox(greyImage, (x0, y0), frameon=False)
            ax.add_artist(ab)
    #put in for loop possibly
    client2server = patches.FancyArrowPatch(rose[0], rose[1], color = '#4A708B', linewidth = 1.5)
    server2root = patches.FancyArrowPatch(rose[1], rose[2], color = '#ADD8E6', linewidth = 1.5, linestyle = (0, (5, 10)))
    server2tld = patches.FancyArrowPatch(rose[1], rose[3], color = '#ADD8E6', linewidth = 1.5, linestyle = (0, (5, 10)))
    server2auth = patches.FancyArrowPatch(rose[1], rose[4], color = '#ADD8E6', linewidth = 1.5, linestyle = (0, (5, 10)))
    plt.gca().add_patch(client2server)
    plt.gca().add_patch(server2root)
    plt.gca().add_patch(server2tld)
    plt.gca().add_patch(server2auth)

    ax.set_title(str(sys.argv[1]) + ' [Recursive]', fontsize = 15) #fontdict={'fontsize': 12, 'fontweight': 'medium'}
    ax.set_xlabel('Order Contacted') #order read, node id
    ax.set_ylabel('Node Address', labelpad=15) #ip address
    ax.set_yticklabels([])
    xint = range(min(x)-1, int(math.ceil(max(x))+2))
    ax.set_ylim(0.0, max(y)+(max(y)/3))
    plt.xticks(xint)
    fig.canvas.mpl_connect("motion_notify_event", hover)
#    fig.savefig("output.png",bbox_inches='tight')
    plt.show()
