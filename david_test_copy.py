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
result['presentationProperties'] = []
result['properties'] = []

nodes = {}

nodes_df = pd_network.nodes

for index in nodes_df.index.values:
    node = {'id': index}
    properties = []
    for column in nodes_df.columns.values:
        ndex_property = {}
        ndex_property['valueId'] = 0
        ndex_property['dataType'] = 'String'
        ndex_property['value'] = nodes_df.at[index, column]
        ndex_property['predicateId'] = 0
        ndex_property['predicateString'] = column
        ndex_property['type'] = 'NdexPropertyValuePair'
        properties.append(ndex_property)
    node['properties'] = properties
    node['presentationProperties'] = []
    node['type'] = 'PropertyGraphNode'
    node['name'] = index
    nodes[index] = node

result['nodes'] = nodes

edges = {}

edges_df = pd_network.edges

# for index in edges_df.index.values:
#     edge = {'id': index}
#
#     for column in edges_df.columns.values:
#         edge[column] = edges_df.at[index, column]
#     edge['properties'] = []
#     edge['presentationProperties'] = []
#     edge['type'] = 'PropertyGraphEdge'
#     edges[index] = edge
#
# result['edges'] = edges

post_json = json.dumps(result, indent=2, separators=(',', ':'))

print post_json

#my_ndex.validate_network(post_json)
#
my_ndex.save_new_property_graph_network(post_json)