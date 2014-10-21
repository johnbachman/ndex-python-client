# -*- coding: utf-8 -*-
"""
Created on Sat Oct 18 17:04:44 2014

@author: Dexter Pratt
"""

network = {
    "$schema": "http://www.ndexbio.org/api/schema/1.0.0/Network",
    "description": "Schema for Network objects used in NDEx REST API",
    "type": "object",
        "required": [
        "type", 
        "edges", 
        "nodes", 
        "baseTerms", 
        "functionTerms", 
        "reifiedEdgeTerms", 
        "citations", 
        "supports", 
        "properties", 
        "presentationProperties",
        "namespaces", 
        "name"
        ],
    "properties": {
        "type": {
            "description": "NDEx object type. Must always = 'Network' for Network objects",
            "type": "string"
        },
        "creationTime": {
            "description": "Timestamp indicating Networks creation time. Ignored and can be null when Network is POSTed for creation.",
            "type": ["number", "null"],
        },
        "modificationTime": {
            "description": "Timestamp indicating Networks last modification time. Ignored and can be null when Network is POSTed or PUT",
            "type": ["number", "null"],
        },
        "isComplete": {
            "description": "Set to false while the network is being incrementally created or modified, true otherwise. Ignored and can be null when Network is POSTed or PUT",
            "type": ["boolean", "null"],
        },
        "isLocked": {
            "description": "Content modification permitted only if false. Ignored and can be null when Network is POSTed or PUT",
            "type": ["boolean", "null"],
        },
        "externalId": {
            "description": "UUID for the Network. Ignored and can be null when Network is POSTed for creation",
            "type": ["string", "null"]
        },
        "uri": {
            "description": "Unique URI for the Network based on the server address and Network UUID. Ignored and can be null when Network is POSTed for creation",
            "type": "string"
        },
        "nodeCount": {
            "description": "Number of Node objects in the Network, set by server when Network is returned. Ignored and can be null when Network is POSTed or PUT",
            "type": ["integer", "null"]
        },
        "edgeCount": {
            "description": "Number of Edge objects in the Network, set by server when Network is returned. Ignored and can be null when Network is POSTed or PUT",
            "type": "integer"
        },
        "visibility": {
            "description": "Visibility status of the Network. Set by server when Network is returned. Ignored and can be null when Network is POSTed or PUT",
            "type": ["string", "null"],
            "enum": [
                "PUBLIC",
                "PRIVATE",
                "DISCOVERABLE"
            ]
        },
        "name": {
            "description": "Name or Title of the Network. Required, but not a unique identifier for the Network.",
            "type": "string"
        },
        "description": {
            "description": "Text description of the Network.",
            "type": ["string", "null"]
        },
        "version": {
            "description": "Version string for the Network. No required format but strings conforming to semantic versioning standard are recommended and may be parsed.",
            "type": ["string", "null"]
        },
        "namespaces": {
            "description": "Object keys are integer element ids, values are Namespace objects",
            "type": "object",
            "additionalProperties": {
                "$ref": "#/definitions/Namespace"
            },   
        },
        "baseTerms": {
            "description": "Object keys are integer element ids, values are BaseTerm objects",
            "type": "object",
            "additionalProperties": {
                "$ref": "#/definitions/BaseTerm"
            }   
        },
        "functionTerms": {
            "description": "Object keys are integer element ids, values are FunctionTerm objects",
            "type": "object",
            "additionalProperties": {
                "$ref": "#/definitions/FunctionTerm"
            }
        },
        "reifiedEdgeTerms": {
            "description": "Object keys are integer element ids, values are ReifiedEdgeTerm objects",
            "type": "object",
            "additionalProperties": {
                "$ref": "#/definitions/ReifiedEdgeTerm"
            }
        },
        "nodes": {
            "description": "Object keys are integer element ids, values are Node objects",
            "type": "object",
            "additionalProperties": {
                "$ref": "#/definitions/Node"
            }
        },
        "edges": {
            "description": "Object keys are integer element ids, values are Edge objects",
            "type": "object",
            "additionalProperties": {
                "$ref": "#/definitions/Edge"
            }
        },
        "citations": {
            "description": "Object keys are integer element ids, values are Citation objects",
            "type": "object",
            "additionalProperties": {
                "$ref": "#/definitions/Citation"
            }
        },
        "supports": {
            "description": "Object keys are integer element ids, values are Support objects",
            "type": "object",
            "additionalProperties": {
                "$ref": "#/definitions/Support"
            }
        },
        "presentationProperties": {
            "description": "Items are SimplePropertyValuePair objects describing the appearance and layout of the Network",
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": {
                    "$ref": "#/definitions/SimplePropertyValuePair"
                }
            }
        },
        "properties": {
            "description": "Items are NdexPropertyValuePair objects describing the content of the Network",
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": {
                    "$ref": "#/definitions/NdexPropertyValuePair"
                }              
            }
        }
    },
    "definitions": {
        "Edge": {
            "properties": {
                "citationIds": {
                    "type": "array",
                    "items": {
                        "type": "number"
                    }
                },
                "id": {
                    "type": "number"
                },
                "objectId": {
                    "type": "number"
                },
                "predicateId": {
                    "type": "number"
                },
                "presentationProperties": {
                    "type": "object",
                    "items": {
                    
                        "additionalProperties": {
                            "$ref": "#/definitions/SimplePropertyValuePair"
                        }
                        
                    },
                    "type": "array"
                },
                "properties": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": {
                            "$ref": "#/definitions/NdexPropertyValuePair"
                        } 
                    }                    
                },
                "subjectId": {
                    "type": "number"
                },
                "supports": {
                    "items": {
                        "type": "number"
                    },
                    "type": "array"
                },
                "type": {
                    "type": "string"
                }
            },
            "type": "object"
        },
        "Node": {
            "properties": {
                "aliases": {
                    "items": {
                        "type": "number"
                    },
                    "type": "array"
                },
                "citations": {
                    "items": {
                        "type": "number"
                    },
                    "type": "array"
                },
                "id": {
                    "type": "number"
                },
                "name": {
                    "type": "string"
                },
                "presentationProperties": {
                    "items": {
                        "additionalProperties": {
                            "$ref": "#/definitions/SimplePropertyValuePair"
                        },
                        "type": "object"
                    },
                    "type": "array"
                },
                "properties": {
                    "items": {
                        "additionalProperties": {
                            "$ref": "#/definitions/NdexPropertyValuePair"
                        },
                        "type": "object"
                    },
                    "type": "array"
                },
                "relatedTerms": {
                    "items": {
                        "type": "number"
                    },
                    "type": "array"
                },
                "represents": {
                    "type": "number"
                },
                "representsTermType": {
                    "type": "string"
                },
                "supportIds": {
                    "items": {
                        "type": "number"
                    },
                    "type": "array"
                },
                "type": {
                    "type": "string"
                }
            },
            "type": "object"
        }
    }
}




