#!/usr/bin/env python

import requests
import pandas as pd
import json
from jsonschema import validate
import ndex_schema as schema


# Utility to strip UUID from property graph before writing, ensure that we create new network
def remove_uuid_from_network(ndex_property_graph_network):
    counter = 0
    for pv in ndex_property_graph_network.properties:
        if pv.predicateString == "UUID":
            del ndex_property_graph_network.properties[counter]
            return None
        else:
            counter = counter + 1


# Each ndex property becomes a dict property
def add_ndex_properties_to_dict(properties, target):
    for pv in properties:
        predicate = pv['predicateString']
        # dataType = pv['dataType']
        value = pv['value']
        # next, convert values based on datatype...
        target[predicate] = value


class PDGraph:
    def __init__(self, ndex_property_graph_network):
        # assemble a dictionary of nodes and then create the dataframe 
        node_rows = []
        node_indexes = []
        for index, node in ndex_property_graph_network['nodes'].iteritems():
            node_dict = {}
            # PropertyGraphNodes just have properties
            add_ndex_properties_to_dict(node['properties'], node_dict)
            node_rows.append(node_dict)
            node_indexes.append(index)

        self.nodes = pd.DataFrame(node_rows, node_indexes)

        # assemble an array of dictionaries of edges where the edge id is the key
        # and the dictionary properties are the edge properties, the predicate, and the 
        # ids for subject and object.
        # then create the dataframe
        edge_rows = []
        edge_indexes = []
        for index, edge in ndex_property_graph_network['edges'].iteritems():
            edge_dict = {}
            # PropertyGraphEdges have special fields describing the 
            # edge itself, in addition to properties of the edge
            edge_dict['ndex:subjectId'] = edge['subjectId']
            edge_dict['ndex:predicate'] = edge['predicate']
            edge_dict['ndex:objectId'] = edge['objectId']
            add_ndex_properties_to_dict(edge['properties'], edge_dict)
            edge_rows.append(edge_dict)
            edge_indexes.append(index)

        self.edges = pd.DataFrame(edge_rows, edge_indexes)

        # assemble a dictionary of the network properties
        property_dict = {}
        add_ndex_properties_to_dict(ndex_property_graph_network['properties'], property_dict)
        self.properties = pd.Series(property_dict)

        ## TBD export a PDGraph to an NDEx PropertyGraphNetwork dict structure
    def to_property_graph_network(self, name):
        result = {}
        result['name'] = name

        nodes = {}

        nodes_df = self.nodes

        for index in nodes_df.index.values:
            node = {'id': index}
            properties = []
            for column in nodes_df.columns.values:
                property = {}
                property['valueId'] = 0
                property['dataType'] = 'String'
                property['value'] = nodes_df.at[index, column]
                property['predicateId'] = 0
                property['predicateString'] = column
                property['type'] = 'NdexPropertyValuePair'
                properties.append(property)
            node['properties'] = properties
            nodes[index] = node

        result['nodes'] = nodes

        edges = {}

        edges_df = self.edges

        for index in edges_df.index.values:
            edge = {'id': index}

            for column in edges_df.columns.values:
                edge[column] = edges_df.at[index, column]
            edge['properties'] = []
            edge['presentationProperties'] = []
            edge['type'] = 'PropertyGraphEdge'
            edges[index] = edge

        result['edges'] = edges

        property_graph_network = json.dumps(result, indent=2, separators=(',', ':'))

        return property_graph_network


class Ndex:
    def __init__(self, host="http://www.ndexbio.org", username=None, password=None):
        if "localhost" in host:
            self.host = "http://localhost:8080/ndexbio-rest"
        else:
            self.host = host + "/rest"
        # create a session for this Ndex
        self.s = requests.session()
        if username and password:
            # add credentials to sesson, if available
            self.s.auth = (username, password)

            # Base methods for making requests to this NDEx

    def put(self, route, put_json):
        url = self.host + route
        print "PUT route: " + url
        print put_json
        headers = {'Content-Type': 'application/json;charset=UTF-8',
                   'Accept': 'application/json',
                   'Cache-Control': 'no-cache',
        }
        response = self.s.put(url, data=put_json, headers=headers)
        response.raise_for_status()
        return response.json()

    def post(self, route, post_json):
        url = self.host + route
        print "POST route: " + url
        print post_json

        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Cache-Control': 'no-cache',
        }
        response = self.s.post(url, data=post_json, headers=headers)
        response.raise_for_status()
        return response.json()

    def delete(self, route):
        url = self.host + route
        response = self.s.delete(url)
        response.raise_for_status()
        return response.json()

    def get(self, route, get_params=None):
        url = self.host + route
        print "GET route: " + url
        print get_params
        response = self.s.get(url, params=get_params)
        response.raise_for_status()
        return response.json()

    # Network methods


    # Search for networks by keywords
    # network    POST    /network/search/{skipBlocks}/{blockSize}    SimpleNetworkQuery    NetworkSummary[]
    def find_networks(self, search_string="", account_name=None, skip_blocks=0, block_size=100):
        route = "/network/search/%s/%s" % (skip_blocks, block_size)
        post_data = {"searchString": search_string}
        if account_name:
            post_data["accountName"] = account_name
        post_json = json.dumps(post_data)
        return self.post(route, post_json)

    def find_networks_as_data_frame(self, search_string="", account_name=None, skip_blocks=0, block_size=100):
        return pd.DataFrame(self.find_networks(search_string, account_name, skip_blocks, block_size))

    def get_network_api(self, as_type="DataFrame"):
        route = "/network/api"
        decoded_json = self.get(route)
        if as_type == "DataFrame":
            return pd.DataFrame(decoded_json)
        else:
            return decoded_json

            # network    POST    /network/{networkUUID}/edge/asNetwork/{skipBlocks}/{blockSize}        Network

    def get_network_by_edges(self, network_id, skip_blocks=0, block_size=100):
        route = "/network/%s/edge/asNetwork/%s/%s" % (network_id, skip_blocks, block_size)
        return self.get(route)

    # network    GET    /network/{networkUUID}/asNetwork       Network
    def get_complete_network(self, network_id):
        route = "/network/%s/asNetwork" % (network_id)
        return self.get(route)

    # network    GET    /network/{networkUUID}       NetworkSummary
    def get_network_summary(self, network_id):
        route = "/network/%s" % (network_id)
        return self.get(route)

    #    network    POST    /network    Network    NetworkSummary
    def save_new_network(self, network):
        route = "/network/asNetwork"
        return self.post(route, network)

    #    network    POST    /network/asNetwork/group/{group UUID}    Network    NetworkSummary
    def save_new_network_for_group(self, network, group_id):
        route = "/network/asNetwork/group/%s" % (group_id)
        self.removeUUIDFromNetwork(network)
        return self.post(route, network)

    ##  Neighborhood PathQuery
    #    network    POST    /network/{networkUUID}/asPropertyGraph/query    SimplePathQuery    PropertyGraphNetwork
    def get_neighborhood(self, network_id, search_string, search_depth=1):
        route = "/network/%s/asNetwork/query" % (network_id)
        post_data = {'searchString': search_string,
                     'searchDepth': search_depth}
        post_json = json.dumps(post_data)
        return self.post(route, post_json)

    # PropertyGraphNetwork methods

    #    network    POST    /network/{networkUUID}/edge/asPropertyGraph/{skipBlocks}/{blockSize}  PropertyGraphNetwork
    def get_property_graph_network_by_edges(self, network_id, skip_blocks=0, block_size=100):
        route = "/network/%s/edge/asPropertyGraph/%s/%s" % (network_id, skip_blocks, block_size)
        return self.get(route)

    #    network    GET    /network/{networkUUID}/asPropertyGraph        PropertyGraphNetwork
    def get_complete_property_graph_network(self, network_id):
        route = "/network/%s/asPropertyGraph" % (network_id)
        return self.get(route)

    #    network    POST    /network/asPropertyGraph    PropertyGraphNetwork    NetworkSummary
    def save_new_property_graph_network(self, property_graph_network):
        route = "/network/asPropertyGraph"
        # self.removeUUIDFromNetwork(property_graph_network)
        return self.post(route, property_graph_network)

    #    network    POST    /network/asPropertyGraph/group/{group UUID}    PropertyGraphNetwork    NetworkSummary
    def save_new_property_graph_network_for_group(self, property_graph_network, group_id):
        route = "/network/asPropertyGraph/group/%s" % (group_id)
        # self.removeUUIDFromNetwork(property_graph_network)
        return self.post(route, property_graph_network)

    ##  Neighborhood PathQuery
    #    network    POST    /network/{networkUUID}/asPropertyGraph/query    SimplePathQuery    PropertyGraphNetwork
    def get_neighborhood_as_property_graph(self, network_id, search_string, search_depth=1):
        route = "/network/%s/asPropertyGraph/query" % (network_id)
        post_data = {'searchString': search_string,
                     'searchDepth': search_depth}
        post_json = json.dumps(post_data)
        return self.post(route, post_json)


    # User methods

    # Group methods

    # Request methods

    # Task methods

    # Validation

    def validate_network(self, network):
        return validate(network, schema.network)