#!/usr/bin/python

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import json
import sys

class Node:
	def __init__(self, name, queries):
		self.name = name
		self.ns_mappings = {}
		self.queries = queries # self.queries[0]['qname'] --> '.'
		self.coord = ()
		self.qname = []
		self.qclass = []
		self.qtype = []
		self.ips = []

		

	def get_coords(self):
		return self.coord

	def set_coords(self, x, y):
		self.coord = (x, y)

	def get_mapping(self):
		return self.ns_mappings

	def set_mapping(self, mapping):
		flip_dict = {}
		for name, ip in self.ns_mappings.iteritems():
			flip_dict[ip[0]] = name
			print(ip[0] + " - " + name)

		self.ns_mappings = flip_dict

	def get_info(self):
		info = ''
		info += "Server Name: " + self.name + "\n"

		if self.qclass:
			info += "qClass: " + self.qclass[0] + "\n"

		if self.qtype:
			info += "qType: " + ", ".join(list(set(self.qtype))) + "\n"

		if self.ips:
			info += "IPs Contacted: \n"+  "\n".join(self.ips) + "\n"

			try:
				name_servers = [self.ns_mappings[ip] for ip in self.ips]  #contacted name servers using flip_dict
				info += "Name Servers Contacted: \n" + "\n".join(name_servers)
			except KeyError:
				pass

		return info

class Nodelist:
	def __init__(self, file_path, query):
		self.file_path = file_path
		self.nodes = [] # list of query nodes
		self.levels = [] # list of outer nodes [., com., etc.]
		self.data = [] # placeholder for json response
		self.query = query # for level comparison
		self.mapping = {}

	def get_node(self, coord):
		return self.mapping[coord]
	
	def parse_json(self):
		# convert json file to dictionary
		with open(self.file_path) as json_file:
			self.data = json.load(json_file)
			del self.data['_meta._dnsviz.']

		# convert dictionary into iterable list
		self.levels = list(self.data)
		# sort to mimic dns resolution order
		self.levels.sort(key=len)

		# find the final level and move it to front
		# in case final query isn't longest the level
		temp = {}
		for level in self.levels:
			if (level == self.query):
				temp = level
				self.levels.remove(level)
				break
		self.levels.append(temp)

	def index_nodes(self):
		client_ipv4 = '' # placeholder for client node

		for level in self.levels:
			new_node = [] # placeholder for empty node
			node = self.data[level] # for easier access
			node_name = level

			if 'clients_ipv4' in node:
				client_ipv4 = node['clients_ipv4'][0]

			ns_mappings = {}
			if 'auth_ns_ip_mapping' in node:
				ns_mappings = node['auth_ns_ip_mapping']

			queries = {}
			if 'queries' in node:
				queries = node['queries']

			new_node = Node(node_name, queries)
			new_node.set_mapping(ns_mappings)

			for subquery in queries:
				new_node.qname.append(subquery['qname'])  # qname
				new_node.qclass.append(subquery['qclass'])  # qclass
				new_node.qtype.append(subquery['qtype'])  # qtype
				contacted_ips = list(subquery['responses'].keys())
				new_node.ips = contacted_ips			
		
			self.nodes.append(new_node)



		# main 3 servers
		self.nodes[0].set_coords(3, 20)
		self.nodes[1].set_coords(3, 15)
		self.nodes[2].set_coords(3, 10)

		mapping = self.nodes[2].get_mapping()

		# if we have sub servers
		if len(self.nodes) > 3:
		# initialize counters
			server_x_coord = 4
			y_lim = 15
			offset = y_lim / (len(self.nodes) - 3)
			server_y_coord = y_lim - (offset * ((len(self.nodes) - 1.0) / len(self.nodes))) + 5
			for i in range(len(self.nodes)):
				if i < 3:
					continue
				self.nodes[i].set_coords(server_x_coord, server_y_coord)
				self.nodes[i].set_mapping(mapping)
				server_y_coord -= offset
				# print(node.ns_mappings)

		client_node = Node('client [' + client_ipv4 + ']', {})
		client_node.set_coords(2, 15)
		host_node = Node('[host]', {})
		host_node.set_coords(1.5, 15)

		self.nodes = [host_node, client_node] + self.nodes

		# build mapping for hover
		for node in self.nodes:
			self.mapping[node.get_coords()] = node

	def build(self):
		# run the setup functions
		self.parse_json()
		self.index_nodes()

		# for node in self.nodes:
		# 	print(node.name + ': ' + str(node.coord))

		return self.nodes



def script():
	nodelist = Nodelist('aut.json', str(sys.argv[1]) + '.')
	nodes = nodelist.build()

	fig, ax = plt.subplots()
	props = dict(boxstyle='round', facecolor='white', alpha=0.0)
	annot = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points", bbox=props)

	host = 0
	client = 1
	root = 2
	tld = 3
	auth = 4

	hostImage = OffsetImage(plt.imread('host.png'), zoom=0.12)
	clientImage = OffsetImage(plt.imread('resolver.png'), zoom=0.12)
	rootImage = OffsetImage(plt.imread('root.png'), zoom=0.12)
	tldImage = OffsetImage(plt.imread('tld.png'), zoom=0.12)
	targetImage = OffsetImage(plt.imread('target.png'), zoom=0.12)
	subImage = OffsetImage(plt.imread('sub.png'), zoom=0.12)
	authImage = OffsetImage(plt.imread('auth.png'), zoom=0.12)


	x_list = []
	y_list = []

	for i in range(len(nodes)):
		node = nodes[i]
		x, y = node.get_coords()
		x_list.append(x)
		y_list.append(y)
		ax.plot(x, y)
		if i == host:
			ab = AnnotationBbox(hostImage, (x, y), frameon=False)
			ax.add_artist(ab)
		elif i == client:
			ab = AnnotationBbox(clientImage, (x, y), frameon=False)
			ax.add_artist(ab)
		elif i == root:
			ab = AnnotationBbox(rootImage, (x, y), frameon=False)
			ax.add_artist(ab)
		elif i == tld:
			ab = AnnotationBbox(tldImage, (x, y), frameon=False)
			ax.add_artist(ab)
		elif i == auth:
			ab = AnnotationBbox(authImage, (x, y), frameon=False)
			ax.add_artist(ab)
		elif i == len(nodes) - 1:
			ab = AnnotationBbox(targetImage, (x, y), frameon=False)
			ax.add_artist(ab)
		else:
			ab = AnnotationBbox(subImage, (x, y), frameon=False)
			ax.add_artist(ab)	

	sc = plt.scatter(x_list, y_list, s = 2000, marker='s', color='white')

	ax.set_title(str(sys.argv[1]) + ' [authoritative]', fontsize = 20)

	ax.set_xlabel("Order Contacted", fontsize = 10)
	ax.set_ylabel(" ", fontsize = 10)

	ax.set_ylim([0, 30])
	ax.set_xlim([1, 7])

	style="Simple,tail_width=1,head_width=3,head_length=10"
	curve = dict(arrowstyle = style, color = "k", connectionstyle = "arc3, rad = 0.05")
	flat = dict(arrowstyle = style, color = "k")


	for i in range(auth + 1, len(nodes)):
		front = patches.FancyArrowPatch(nodes[auth].get_coords(), nodes[i].get_coords(), **curve)
		back = patches.FancyArrowPatch(nodes[i].get_coords(), nodes[auth].get_coords(), **curve)
		plt.gca().add_patch(front)
		plt.gca().add_patch(back)

	# connect host client
	a = patches.FancyArrowPatch(nodes[host].get_coords(), nodes[client].get_coords(), **curve)
	b = patches.FancyArrowPatch(nodes[client].get_coords(), nodes[host].get_coords(), **curve)
	# connect client to root, TLD, and auth
	c = patches.FancyArrowPatch(nodes[client].get_coords(), nodes[root].get_coords(), **curve)
	d = patches.FancyArrowPatch(nodes[root].get_coords(), nodes[client].get_coords(), **curve)
	e = patches.FancyArrowPatch(nodes[client].get_coords(), nodes[tld].get_coords(), **curve)
	f = patches.FancyArrowPatch(nodes[tld].get_coords(), nodes[client].get_coords(), **curve)
	g = patches.FancyArrowPatch(nodes[client].get_coords(), nodes[auth].get_coords(), **curve)
	h = patches.FancyArrowPatch(nodes[auth].get_coords(), nodes[client].get_coords(), **curve)

	for edge in [a, b, c, d, e, f, g, h]:
		plt.gca().add_patch(edge)

	def update_annot(ind):
		pos = sc.get_offsets()[ind["ind"][0]]
		node = nodelist.get_node((pos[0], pos[1]))
		annot.xy = (4.5, 0.5)
		text = str(node.get_info())
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

	fig.canvas.mpl_connect("motion_notify_event", hover)
	plt.show()


if __name__ == '__main__':
	script()


