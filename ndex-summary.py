# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 11:10:59 2014

@author: Dexter Pratt
"""

def stripPrefixes(string):
    if string.lower().startsWith("bel:"):
        return string[4:string.len()]
    elif string.lower().startsWith("hgnc:"):
         return string[5:string.len()]
    else:
         return string
         

def getFunctionAbbreviation(string):
        fl = stripPrefixes(string).lower()

        if fl == "abundance":
            return "a"
        elif fl == "biological_process":
            return "bp"
        elif fl ==  "catalytic_activity":
            return "cat"
        elif fl ==  "complex_abundance":
            return "complex"
        elif fl ==  "pathology":
            return "path"
        elif fl ==  "peptidase_activity":
            return "pep"
        elif fl ==  "protein_abundance":
            return "p"
        elif fl ==  "rna_abundance":
            return "r"
        elif fl ==  "protein_modification":
            return "pmod"
        elif fl ==  "transcriptional_activity":
            return "tscript"
        elif fl ==  "molecular_activity":
            return "act"
        elif fl ==  "degradation":
            return "deg"
        elif fl ==  "kinase_activity":
            return "kin"
        elif fl ==  "substitution":
            return "sub"
        else:
            return fl

class NetworkSummary:
    def __init__(self, ndexNetwork):
        self.network = ndexNetwork
        self.supportToEdgeMap = {}
        self.citationToSupportMap = {}
        self.nodeLabelMap = {}
        self.termLabelMap = {}
        
        for nodeId, node in ndexNetwork.nodes.iteritems():
            self.nodeLabelMap[nodeId] = self.getNodeLabel(node)
        
        for edge in ndexNetwork.edges.values():
            for supportId in edge.supports:
                support = ndexNetwork.supports[supportId]
                edgeList = self.supportToEdgeMap[supportId] or []
                edgeList.append(edge)
                self.supportToEdgeMap[supportId] = edgeList
                    
        for supportId in self.supportToEdgeMap.keys():
            support = ndexNetwork.supports[supportId]
            supportIdList = self.citationToSupportMap[support.citationId] or []
            supportIdList.append(supportId)
            self.citationToSupportMap[support.citationId] = supportIdList

    def getEdgeLabel(self, edge):
        subjectLabel = self.nodeLabelMap[edge.subjectId]
        objectLabel = self.nodeLabelMap[edge.objectId]
        predicateTerm = self.network.baseTerms[edge.predicateId]
        predicateLabel = stripPrefixes(self.getTermLabel(predicateTerm))
        label = "%s %s %s" % (subjectLabel, predicateLabel, objectLabel)
        return label
          
    def getNodeLabel(self, node):
        if node.name:
            return node.name
        elif node.represents:
            termLabel = self.termLabelMap[node.represents]
            if termLabel:
                return termLabel
            else:
                term = self.getTermById(node.represents)
                if term:
                    termLabel = self.getTermLabel(term)
                    self.termLabelMap[node.represents] = termLabel
                    return termLabel
        else:
            return "node %s" % (node.id)
                
    def getTermById(self, termId):
        term = self.network.baseTerms[termId] or self.network.functionTerms[termId] or self.network.reifiedEdgeTerms[termId]
        return term
        
    def getTermLabel(self, termId):
        label = self.termLabelMap[termId]
        if label:
            return label
        else:
            term = self.getTermById(termId)
            if term.type.lower() == "baseterm":
                if term.namespaceId:
                    namespace = self.network.namespaces[term.namespaceId]
                    if namespace:
                        if namespace.prefix:
                            label = "%s:%s" % (namespace.prefix, term.name)
                        elif namespace.uri:
                            label = "%s%s" % (namespace.uri, term.name)
                        else:
                            label = term.name
                    else:
                        label = term.name
                else:
                    label = term.name
        
            elif term.type.lower() == "functionterm": 
                functionLabel = self.getTermLabel[term.functionTermId]
                functionLabel = getFunctionAbbreviation(functionLabel)
                parameterLabels = []
                for parameterId in term.parameterIds:
                    parameterLabel = self.getTermLabel[parameterId]
                    parameterLabels.append(parameterLabel)
                label = "%s(%s)" % (functionLabel, ",".join(parameterLabels))
            
            elif term.type.lower() == "reifiededgeterm": 
                reifiedEdge = self.network.edges[term.edgeId]
                if reifiedEdge:
                    label = "(%s)" % (self.getEdgeLabel(reifiedEdge))
                else: 
                    label = "(reifiedEdge: %s)" % (term.edgeId)
                    
            else:
                label = "term: %s" % (termId)
        
        self.termLabelMap[termId] = label      
        return label   
        
    def writeSummary(self, fileName):
        file = open(fileName, 'w')
        for citationId, supportIdList in self.citationToSupportMap.iteritems():
            citation = self.network.citations[citationId]
            # Write Citation
            file.write("\n=========================================================================\n")
            file.write("        Citation: %s\n" % citation.identifier)
            file.write("=========================================================================\n\n")

            for supportId in supportIdList:
                support = self.network.supports[supportId]
                # Write Support
                file.write("_______________________________\n")
                file.write("Evidence: %s\n\n" % support.text)
                
                edgeList = self.supportToEdgeMap[supportId]
                for edge in edgeList:
                    # Write Edge
                    file.write("       %s\n" % self.getEdgeLabel(edge))
                    for pv in edge.properties:
                        file.write("                %s: %s\n" % (pv.predicateString, pv.value))
                        
        file.close()


