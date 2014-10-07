# -*- coding: utf-8 -*-
"""
Created on Mon Oct  6 22:34:42 2014

@author: dexter pratt
"""
import ndexClient as nc
import ndexUtil as util

myNdex = nc.Ndex("http://test.ndexbio.org", "doom", "doom")
#myNet = myNdex.getNetworkByEdges("63177354-433b-11e4-9369-90b11c72aefa", 0 , 25)
myNet = myNdex.getNeighborhood('1ada3330-45cc-11e4-a9e5-000c29873918', 'BRAF')
myWrapper = util.NetworkWrapper(myNet)
myWrapper.writeSummary()