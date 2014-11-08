import ndex_client as nc
import json
import numpy as np
import pandas as pd

print "1"

my_ndex = nc.Ndex("http://www.ndexbio.org", "mytestuser", "mytestpassword")
df = my_ndex.find_networks_as_data_frame("metabolism")

print "2"

id = "27229ef3-39ed-11e4-bbbc-000c29202374"
property_graph_network = my_ndex.get_neighborhood_as_property_graph(id, "PHAX")
pd_network = nc.PDGraph(property_graph_network)
pd_network.properties

print "3"

print json.dumps(property_graph_network, indent=2, separators=(',', ':'))

print pd_network.nodes.head()

print '4'
nodes = pd_network.nodes
nodes["values"] = pd.Series(np.random.randn(len(nodes)), index=nodes.index)
pd_network.nodes

print pd_network.nodes.head()

print '\n5'

result = {}
result['name'] = 'foo'

nodes = {}

nodes_df = pd_network.nodes

for index in nodes_df.index.values:
    node = {'id': index}
    properties = {}
    for column in nodes_df.columns.values:
        properties[column] = nodes_df.at[index, column]
    node['properties'] = properties
    nodes[index] = node

result['nodes'] = nodes

edges = {}

edges_df = pd_network.nodes

for index in edges_df.index.values:
    edge = {'id': index}
    properties = {}
    for column in edges_df.columns.values:
        properties[column] = edges_df.at[index, column]
    edge['properties'] = properties
    edges[index] = edge

result['nodes'] = edges

post_json = json.dumps(result, indent=2, separators=(',', ':'))

print post_json

#my_ndex.validate_network(post_json)
#
my_ndex.save_new_property_graph_network(post_json)