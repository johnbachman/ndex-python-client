#!/usr/bin/env python

import requests
import pandas as pd
import networkx as nx
import json

class PropertyGraph:
    def __init__(self, network):
        #print network
        self.nodes = pd.DataFrame(network['nodes'].values())
        self.edges = pd.DataFrame(network['edges'].values())
        self.properties = pd.DataFrame(network['properties'])

class Ndex:
        
    def __init__(self, host = "http://www.ndexbio.org", username = None, password = None):
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
    
    def put(self, route, putJson):
        url = self.host + route  
        print "PUT route: " + url
        print putJson
        headers = {'Content-Type' : 'application/json;charset=UTF-8',
                   'Accept' : 'application/json',
                   'Cache-Control' : 'no-cache',
                   }
        response = self.s.put(url, data = putJson, headers = headers)
        response.raise_for_status()
        return response.json()
        
    def post(self, route, postJson):
        url = self.host + route
        print "POST route: " + url
        print postJson
        
#                con.setRequestProperty("charset", "utf-8");
#        con.setRequestProperty("Content-Length",
#                "" + Integer.toString(postDataString.getBytes().length));
#        con.setUseCaches(false);
# ;charset=UTF-8
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Cache-Control': 'no-cache',
                   }
        response = self.s.post(url, data=postJson, headers=headers)
        response.raise_for_status()
        return response.json()
        
    def delete(self, route):
        url = self.host + route
        response = self.s.delete(url)
        response.raise_for_status()
        return response.json()
    
    def get(self, route, getParams = None):
        url = self.host + route
        print "GET route: " + url
        print getParams
        response = self.s.get(url, params = getParams)
        response.raise_for_status()
        return response.json()
        
# Network methods
        
# Utility to strip UUID from property graph before writing, ensure that we create new network
    def removeUUIDFromNetwork(propertyGraphNetwork):   
        counter = 0
        for property in propertyGraphNetwork.properties:
            if property.predicateString == "UUID":
                del propertyGraphNetwork.properties[counter]
                return None
            else:
                counter = counter + 1
                
# Return network depending on asType parameter
    def networkAsType(self, network, asType):
        if asType == "PropertyGraph":
            return PropertyGraph(network)
        elif asType == "networkx":
            return self.ndexToNetworkX(network)
        else:
            return network
            
# Convert NDEx property graph json to networkx network
    def ndexToNetworkX(self, network):
        g = nx.MultiDiGraph()
        for node in network['nodes'].values():
            g.add_node(node['id'])
        for edge in network['edges'].values():
            g.add_edge(edge['subjectId'], edge['objectId'])
        return g
        
# Search for networks by keywords
#    network    POST    /network/search/{skipBlocks}/{blockSize}    SimpleNetworkQuery    NetworkSummary[]
    def findNetworks(self, searchString="", accountName=None, skipBlocks=0, blockSize=100, asType="DataFrame"): 
        route = "/network/search/%s/%s" % (skipBlocks, blockSize)
        postData = {"searchString" : searchString}
        if accountName:
            postData["accountName"] = accountName
        postJson = json.dumps(postData)
        decodedJson = self.post(route, postJson)
        if asType == "DataFrame":
            return pd.DataFrame(decodedJson)
        else:
            return decodedJson

    def getNetworkApi(self, asType="DataFrame"):
        route = "/network/api"
        decodedJson = self.get(route)
        if asType == "DataFrame":
            return pd.DataFrame(decodedJson)
        else:
            return decodedJson
        
# Network PropertyGraph methods
        
#    network    POST    /network/{networkUUID}/edge/asPropertyGraph/{skipBlocks}/{blockSize}        PropertyGraphNetwork
    def getPropertyGraphNetworkByEdges(self, networkId, skipBlocks=0, blockSize=100, asType = "PropertyGraph"):
        route = "/network/%s/edge/asPropertyGraph/%s/%s" % (networkId, skipBlocks, blockSize)
        network = self.get(route)
        return self.networkAsType(network, asType)

#    network    GET    /network/{networkUUID}/asPropertyGraph        PropertyGraphNetwork
    def getPropertyGraphNetwork(self, networkId, asType = "PropertyGraph"):
        route = "/network/%s/asPropertyGraph" % (networkId)
        network = self.get(route)
        return self.networkAsType(network, asType)

#    network    POST    /network/asPropertyGraph    PropertyGraphNetwork    NetworkSummary
    def saveNewPropertyGraphNetwork(self, propertyGraphNetwork):
        route = "/network/asPropertyGraph"
        self.removeUUIDFromNetwork(propertyGraphNetwork)
        return self.post(route, propertyGraphNetwork)

#    network    POST    /network/asPropertyGraph/group/{group UUID}    PropertyGraphNetwork    NetworkSummary
    def saveNewPropertyGraphNetworkForGroup(self, propertyGraphNetwork, groupId):
        route = "/network/asPropertyGraph/group/%s" % (groupId)
        self.removeUUIDFromNetwork(propertyGraphNetwork)
        return self.post(route, propertyGraphNetwork)
       
##  Neighborhood PathQuery
#    network    POST    /network/{networkUUID}/asPropertyGraph/query    SimplePathQuery    PropertyGraphNetwork    
    def getNeighborhoodAsPropertyGraph(self, networkId, searchString, searchDepth=1, asType = "PropertyGraph"):
        route = "/network/%s/asPropertyGraph/query" % (networkId) 
        postData = {'searchString': searchString,
                   'searchDepth': searchDepth}
        postJson = json.dumps(postData)
        network = self.post(route, postJson)
        return self.networkAsType(network, asType)

        
# User methods
        
# Group methods

# Request methods

# Task methods