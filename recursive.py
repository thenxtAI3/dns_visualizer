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
        self.longAddress = ip2long(address)
        self.coordinates = (-1, -1)
        self.server_type = ""
        self.response_time = ""
        self.msg_size = ""
        self.resolution = ""
        self.start_time = ""
        self.end_time = ""
        
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
        self.levels = list(self.data)
        domainName = self.data[self.levels[len(self.levels)-1]]
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
        self.nodes.append(Node(3, '100.168.1.200'))
        self.nodes.append(Node(3, '192.168.1.254'))
        self.nodes.append(Node(3, '255.255.255.0'))
        print(self.nodes)
        
    #create Node objects from data, set Node class variables
#    def create_Nodes(self, data):
#        #create resolver and recursive server nodes
#        resolver = Node(1,
#                        data["."]["clients_ipv4"])
#        recursive = Node(2,
#                         data["."][ "auth_ns_ip_mapping"]["ns1."])
#
#        # #set resolver server node statistics
#        resolver.set_server_type("Resolver")
#        # resolver.set_response_time()
#        resolver.set_resolution_process("N\A")
#        # resolver.set_msg_size()
#        resolver.set_coordinates(1.0, 0.0)
#
#        # #set recursive server node statistics
#        recursive.set_server_type("Recursive")
#        # recursive.set_response_time()
#        recursive.set_resolution_process(' -> '.join(data.keys()))
#        # recursive.set_msg_size()
#        recursive.set_coordinates(2.0, 1.0)
#
#        self.temp_nodes.append((resolver))
#        self.temp_nodes.append(recursive)

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
            coordinates.append((node.id,node.address))
        return coordinates
    def size(self):
        return len(self.nodes)
        
def update_annot(ind):
    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
#    print(pos)
    node = sample.get_node_from_hover(pos[0], pos[1])
    text = "sample" + node.address
    annot.set_text(text)
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
    sample = NodeList("recursive.json")
    sample.initializeList()
    sample.getCoordinates()
    #sample.create_Nodes(sample.data)

    sns.set(style="white")
    clientImage = OffsetImage(plt.imread('client.png'), zoom=0.05)
    serverImage = OffsetImage(plt.imread('server.png'), zoom=0.05)
    greyImage = OffsetImage(plt.imread('grey.png'), zoom=0.05)
    
    x = sample.getNodeIds()
    y = sample.getAddress()
    fig, ax = plt.subplots()
    sc = plt.scatter(x, y, marker="s", color='#FFFFFF', s = 400)
    ax.plot(x, y)

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

    ax.set_title('Recursive Query') #fontdict={'fontsize': 12, 'fontweight': 'medium'}
    ax.set_xlabel('Order Contacted') #order read, node id
    ax.set_ylabel('Node Address', labelpad=15) #ip address
    xint = range(min(x)-1, math.ceil(max(x))+2)
    plt.xticks(xint)
    
    fig.canvas.mpl_connect("motion_notify_event", hover)
#    fig.savefig("output.png",bbox_inches='tight')
    plt.show()
