#!/usr/bin/python

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json
import sys

class Node:
    def __init__(self, name, ns_mappings, queries):
        self.name = name
        self.ns_mappings = ns_mappings
        self.queries = queries
        self.coord = ()

    def get_coords(self):
    	return self.coord

    def set_coords(self, x, y):
    	self.coord = (x, y)

    # def set_info(self, request, response):
    # 	self.request = request
    # 	self.response = response

class Nodelist:
	def __init__(self, file_path, query):
		self.file_path = file_path
		self.nodes = [] # list of query nodes
		self.levels = [] # list of outer nodes [., com., etc.]
		self.mapping = {} # node id to coordinates mapping
		self.data = [] # placeholder for json response
		self.query = query # for level comparison

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
		# initialize counters
		level_counter = 2
		y_lim = 20 # max 20 query servers per level
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

			new_node = Node(node_name, ns_mappings, queries)
			new_node.set_coords(level_counter, y_lim / 2) # leaving logic for extension
		
			self.nodes.append(new_node)
			level_counter += 1


		client_node = Node('client [' + client_ipv4 + ']', [], [])
		client_node.set_coords(1, y_lim / 2)
		self.nodes = [client_node] + self.nodes

		for node in self.nodes:
			print(node.name + ': ' + str(node.coord))
			print(node.ns_mappings)




	def get_mapping(self):
		return self.mapping

	def generate_graph(self):
		# run the setup functions
		self.parse_json()
		self.index_nodes()

		plt.title(self.query + ' [authoritative]', fontsize = 20)

		plt.xlabel("Order Contacted", fontsize = 10)
		plt.ylabel(" ", fontsize = 10)


		for node in self.nodes:
			plt.scatter(node.get_coords()[0], node.get_coords()[1], s = 50)

		style="Simple,tail_width=0.5,head_width=6,head_length=10"
		kw = dict(arrowstyle = style, color = "k", connectionstyle = "arc3,rad=.5")
		for i in range(1, len(self.nodes)):
			front = patches.FancyArrowPatch(self.nodes[0].get_coords(), self.nodes[i].get_coords(), **kw)
			back = patches.FancyArrowPatch(self.nodes[i].get_coords(), self.nodes[0].get_coords(), **kw)
			plt.gca().add_patch(front)
			plt.gca().add_patch(back)

		plt.show()


def script():
	nodelist = Nodelist('aut.json', str(sys.argv[1]) + '.')
	nodelist.generate_graph()


if __name__ == '__main__':
	script()


