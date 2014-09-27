#!/usr/bin/env python

import requests
import pandas as pd

class Ndex:
        
    def __init__(self, host = "www.ndexbio.org", username = None, password = None):
        self.host = host
        self.username = username
        self.password = password
    
# Base methods for making requests to this NDEx
    
    def put(self, route, params, payload):
        url = self.host + route
        
    def post(self, route, params, payload):
        url = self.host + route
        
    def delete(self, route):
        url = self.host + route
    
    def get(self, route, params):
        url = self.host + route
        
# Network methods
        
# User methods
        
# Group methods

# Request methods

# Task methods