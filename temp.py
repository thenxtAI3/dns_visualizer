#!/usr/bin/env python
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import math
import json
from ipaddress import IPv4Address, AddressValueError

def is_ipv4_only(addr):  # filtering for ipv6
    try:
        IPv4Address(addr.split('/')[0])
        return True
    except AddressValueError:
        return False


class Node:
    def __init__(self, id, IP):
        self.id = id
        self.address = IP
        self.coordinates = (-1, -1)
        self.server_type = ""
        self.response_time = ""
        self.msg_size = ""
        self.resolution = ""
        self.start_time = ""
        self.end_time = ""

    #getters
    def get_coordinates(self):
        return self.coordinates

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

class NodeList:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.nodes = []
        self.temp_nodes = []
        self.data = {}

    def initializeList(self):
        with open(self.path_to_file) as json_file:
            self.data = json.load(json_file)
            del self.data['_meta._dnsviz.']
        ip_mapping = {}
        self.nodes.append(Node(1, self.data['google.com.']['clients_ipv4'][0]))
        ip_mapping[self.data['google.com.']['clients_ipv4'][0]] = 1
        queries = self.data['google.com.']['queries']
        for query in queries:
            responses = query['responses']
            for ip, message in responses.items():
                if is_ipv4_only(ip):
                    if ip not in ip_mapping.keys():
                        ip_mapping[ip] = len(ip_mapping) + 1
                        self.nodes.append(Node(ip_mapping[ip], ip))
        self.nodes.append(Node(3, '255.255.255.0'))
        self.nodes.append(Node(3, '192.168.1.200'))
        self.nodes.append(Node(3, '192.168.1.254'))


    #create Node objects from data, set Node class variables
    def create_Nodes(self, data):
        #create resolver and recursive server nodes
        resolver = Node(1,
                        data["."]["clients_ipv4"])
        recursive = Node(2,
                         data["."][ "auth_ns_ip_mapping"]["ns0."])



        # #set resolver server node statistics
        resolver.set_server_type("Resolver")
        # resolver.set_response_time()
        resolver.set_resolution_process("N\A")
        # resolver.set_msg_size()
        resolver.set_coordinates(1.0, 0.0)

        # #set recursive server node statistics
        recursive.set_server_type("Recursive")
        # recursive.set_response_time()
        recursive.set_resolution_process(' -> '.join(data.keys()))
        # recursive.set_msg_size()
        recursive.set_coordinates(2.0, 1.0)

        self.temp_nodes.append((resolver))
        self.temp_nodes.append(recursive)

    def get_node_from_hover(self, x, y) :
        for node in self.temp_nodes:
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
            addresses.append(node.address)
        return addresses

    def getCoordinates(self):
        coordinates = []
        for node in self.nodes:
            coordinates.append((node.id, node.address))
        return coordinates

    def size(self):
        return len(self.nodes)


def update_annot(ind):
    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    print(pos)
    # node = sample.get_node_from_hover(pos[0], pos[1])
    # a = node.address
    text = "sample" # + a[0]
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
    sample = NodeList("rec.json")
    sample.initializeList()
    sample.getCoordinates()
    sample.create_Nodes(sample.data)

clientImage = OffsetImage(plt.imread('host.png'), zoom=0.05)
serverImage = OffsetImage(plt.imread('server.png'), zoom=0.05)

x = sample.getNodeIds()
y = sample.getAddress()
fig, ax = plt.subplots()
sc = plt.scatter(x, y, color='#999999', s = 350)
ax.plot(x, y)

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
annot = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points", bbox=props,
                    arrowprops=dict(arrowstyle="->"))

firstNode = True
for x0, y0 in zip(x, y):
    if firstNode:
        ab = AnnotationBbox(clientImage, (x0, y0), frameon=False)
        ax.add_artist(ab)
        firstNode = False
    else:
        ab = AnnotationBbox(serverImage, (x0, y0), frameon=False)
        ax.add_artist(ab)

ax.set_title('Recursive Query')
ax.set_xlabel('Node ID')  # order read
ax.set_ylabel('Node Address', labelpad=15)  # ip address
xint = range(int(min(x) - 1), int(math.ceil(max(x)) + 2))
plt.xticks(xint)




fig.canvas.mpl_connect("motion_notify_event", hover)
plt.show()
