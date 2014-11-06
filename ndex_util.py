# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 11:10:59 2014

@author: Dexter Pratt
"""
import sys
import networkx as nx

# Convert NDEx property graph json to a trivial networkx network
def ndex_property_graph_network_to_network_x(ndex_property_graph_network):
        g = nx.MultiDiGraph()
        for node in ndex_property_graph_network['nodes'].values():
            g.add_node(node['id'])
        for edge in ndex_property_graph_network['edges'].values():
            g.add_edge(edge['subjectId'], edge['objectId'])
        return g

# This is specific to summarizing a BEL network. 
# Need to generalize
def strip_prefixes(input):
    st = input.lower()
    if st.startswith('bel:'):
        return input[4:input.len()]
    elif st.startswith('hgnc:'):
         return input[5:input.len()]
    else:
         return input

# This is BEL specific, since BEL is the only current user of funciton terms
def get_function_abbreviation(input):
    st = input.lower()
    fl = strip_prefixes(st)
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

class NetworkWrapper:
    def __init__(self, ndex_network):
        self.network = ndex_network
        self.supportToEdgeMap = {}
        self.citationToSupportMap = {}
        self.nodeLabelMap = {}
        self.termLabelMap = {}

        for nodeId, node in ndex_network['nodes'].iteritems():
            self.nodeLabelMap[int(nodeId)] = self.get_node_label(node)

        for edge in ndex_network['edges'].values():
            for supportId in edge['supportIds']:
                supports = ndex_network['supports']
                support = supports[str(supportId)]
                if supportId in self.supportToEdgeMap:
                    edge_list = self.supportToEdgeMap[supportId]
                else:
                    edge_list = []
                edge_list.append(edge)
                self.supportToEdgeMap[supportId] = edge_list

        for supportId in self.supportToEdgeMap.keys():
            support = ndex_network['supports'][str(supportId)]
            citation_id = support['citationId']
            if citation_id in self.citationToSupportMap:
                support_id_list = self.citationToSupportMap[citation_id]
            else:
                support_id_list = []
            support_id_list.append(supportId)
            self.citationToSupportMap[citation_id] = support_id_list

    def get_edge_label(self, edge):
        subject_label = "missing"
        object_label = "missing"
        predicate_label = "missing"
        subject_id = edge['subjectId']
        object_id = edge['objectId']
        if subject_id in self.nodeLabelMap:
            subject_label = self.nodeLabelMap[subject_id]
        if object_id in self.nodeLabelMap:
            object_label = self.nodeLabelMap[object_id]
        predicate_id = edge['predicateId']
        predicate_label = strip_prefixes(self.get_term_label(predicate_id))
        label = "%s %s %s" % (subject_label, predicate_label, object_label)
        return label

    def get_node_label(self, node):
        if 'name' in node and node['name']:
            return node['name']

        elif 'represents' in node:
            return self.get_term_label(node['represents'])

        else:
            return "node %s" % (node['id'])

    def get_term_by_id(self, term_id):
        term_id_str = str(term_id)
        if term_id_str in self.network['baseTerms']:
            return self.network['baseTerms'][term_id_str]
        elif term_id_str in self.network['functionTerms']:
            return self.network['functionTerms'][term_id_str]
        elif term_id_str in self.network['reifiedEdgeTerms']:
            return self.network['reifiedEdgeTerms'][term_id_str]
        else:
            return None

    def get_term_label(self, term_id):
        if term_id in self.termLabelMap:
            return self.termLabelMap[term_id]
        else:
            label = "error"
            term = self.get_term_by_id(term_id)
            type = term['type'].lower()
            if type == "baseterm":
                name = term['name']
                if 'namespaceId' in term and term['namespaceId']:
                    namespace_id = term['namespaceId']
                    namespace = self.network['namespaces'][namespace_id]

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
                function_term_id = term['functionTermId']
                function_label = self.get_term_label(function_term_id)
                function_label = get_function_abbreviation(function_label)
                parameter_labels = []
                for parameterId in term['parameterIds']:
                    parameter_label = self.get_term_label(parameterId)
                    parameter_labels.append(parameter_label)
                label = "%s(%s)" % (function_label, ",".join(parameter_labels))

            elif type == "reifiededgeterm":
                edge_id = term['edgeId']
                edges = self.network['edges']
                if edge_id in edges:
                    reified_edge = edges[edge_id]
                    label = "(%s)" % (self.get_edge_label(reified_edge))
                else:
                    label = "(reifiedEdge: %s)" % (edge_id)

            else:
                label = "term: %s" % (term_id)

            self.termLabelMap[term_id] = label
            return label

    def write_summary(self, file_name = None):
        if file_name:
            output = open(file_name, 'w')
        else:
            output = sys.stdout
            
        for citation_id, supportIdList in self.citationToSupportMap.iteritems():
            citations = self.network['citations']
            citation = citations[str(citation_id)]
            citation_id = citation['identifier']
            # Write Citation
            output.write("\n=========================================================================\n")
            output.write("        Citation: %s\n" % (citation_id))
            output.write("=========================================================================\n\n")

            for supportId in supportIdList:
                support = self.network['supports'][str(supportId)]
                # Write Support
                output.write("_______________________________\n")
                output.write("Evidence: %s\n\n" % support['text'])

                edge_list = self.supportToEdgeMap[supportId]
                for edge in edge_list:
                    # Write Edge
                    output.write("       %s\n" % self.get_edge_label(edge))
                    for pv in edge['properties']:
                        output.write("                %s: %s\n" % (pv['predicateString'], pv['value']))

        if file_name:
            output.close()


