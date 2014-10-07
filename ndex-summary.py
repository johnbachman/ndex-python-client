# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 11:10:59 2014

@author: Dexter Pratt
"""

def stripPrefixes(input):
    st = input.lower()
    if st.startsWith('bel:'):
        return input[4:input.len()]
    elif st.startsWith('hgnc:'):
         return input[5:input.len()]
    else:
         return input


def getFunctionAbbreviation(input):
    st = input.lower()
    fl = stripPrefixes(st)
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

        for nodeId, node in ndexNetwork['nodes'].iteritems():
            self.nodeLabelMap[nodeId] = self.getNodeLabel(node)

        for edge in ndexNetwork['edges'].values():
            for supportId in edge['supports']:
                supports = ndexNetwork['supports']
                support = supports[str(supportId)]
                if supportId in self.supportToEdgeMap:
                    edgeList = self.supportToEdgeMap[supportId]
                else:
                    edgeList = []
                edgeList.append(edge)
                self.supportToEdgeMap[supportId] = edgeList

        for supportId in self.supportToEdgeMap.keys():
            support = ndexNetwork['supports'][str(supportId)]
            citationId = support['citation']
            if citationId in self.citationToSupportMap:
                supportIdList = self.citationToSupportMap[citationId]
            else:
                supportIdList = []
            supportIdList.append(supportId)
            self.citationToSupportMap[citationId] = supportIdList

    def getEdgeLabel(self, edge):

        subjectLabel = self.nodeLabelMap[edge['subjectId']]
        objectLabel = self.nodeLabelMap[edge['objectId']]
        baseTerms = self.network['baseTerms']
        predicateTerm = baseTerms[str(edge['predicateId'])]
        predicateLabel = stripPrefixes(self.getTermLabel(predicateTerm))
        label = "%s %s %s" % (subjectLabel, predicateLabel, objectLabel)
        return label

    def getNodeLabel(self, node):
        if 'name' in node and node['name']:
            return node['name']

        elif 'represents' in node:
            return self.getTermLabel(node['represents'])

        else:
            return "node %s" % (node['id'])

    def getTermById(self, termId):
        termIdStr = str(termId)
        if termIdStr in self.network['baseTerms']:
            return self.network['baseTerms'][termIdStr]
        elif termIdStr in self.network['functionTerms']:
            return self.network['functionTerms'][termIdStr]
        elif termIdStr in self.network['reifiedEdgeTerms']:
            return self.network['reifiedEdgeTerms'][termIdStr]
        else:
            return None

    def getTermLabel(self, termId):
        if termId in self.termLabelMap:
            return self.termLabelMap[termId]
        else:
            label = "error"
            term = self.getTermById(termId)
            type = term['type'].lower()
            if type == "baseterm":
                name = term['name']
                if 'namespaceId' in term and term['namespaceId']:
                    namespaceId = term['namespaceId']
                    namespace = self.network['namespaces'][namespaceId]

                    if namespace:
                        if namespace['prefix']:
                            label = "%s:%s" % (namespace['prefix'], name)
                        elif namespace['uri']:
                            label = "%s%s" % (namespace['uri'], name)
                        else:
                            label = name
                    else:
                        label = name
                else:
                    label = name

            elif type == "functionterm":
                functionTermId = term['functionTermId']
                functionLabel = self.getTermLabel(functionTermId)
                functionLabel = getFunctionAbbreviation(functionLabel)
                parameterLabels = []
                for parameterId in term['parameters']:
                    parameterLabel = self.getTermLabel(parameterId)
                    parameterLabels.append(parameterLabel)
                label = "%s(%s)" % (functionLabel, ",".join(parameterLabels))

            elif type == "reifiededgeterm":
                edgeId = term['edgeId']
                reifiedEdge = self.network['edges'][edgeId]
                if reifiedEdge:
                    label = "(%s)" % (self.getEdgeLabel(reifiedEdge))
                else:
                    label = "(reifiedEdge: %s)" % (edgeId)

            else:
                label = "term: %s" % (termId)

            self.termLabelMap[termId] = label
            return label

    def writeSummary(self, fileName):
        file = open(fileName, 'w')
        for citationId, supportIdList in self.citationToSupportMap.iteritems():
            citations = self.network['citations']
            citation = citations[str(citationId)]
            citationId = citation['identifier']
            # Write Citation
            file.write("\n=========================================================================\n")
            file.write("        Citation: %s\n" % (citationId))
            file.write("=========================================================================\n\n")

            for supportId in supportIdList:
                support = self.network['supports'][str(supportId)]
                # Write Support
                file.write("_______________________________\n")
                file.write("Evidence: %s\n\n" % support['text'])

                edgeList = self.supportToEdgeMap[supportId]
                for edge in edgeList:
                    # Write Edge
                    file.write("       %s\n" % self.getEdgeLabel(edge))
                    for pv in edge['properties']:
                        file.write("                %s: %s\n" % (pv['predicateString'], pv['value']))

        file.close()


