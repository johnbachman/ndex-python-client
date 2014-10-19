# -*- coding: utf-8 -*-
"""
Created on Sat Oct 18 17:04:44 2014

@author: Dexter Pratt
"""

network = {
    "$schema": "http://www.ndexbio.org/api/schema/1.0.0/Network",
    "description": "Network schema for NDEx REST API",
    "type": "object",
    "properties": {
        "creationTime": {
            "type": "number"
        },
        "description": {
            "type": "string"
        },
        "edgeCount": {
            "type": "integer"
        },
        "baseTerms": {
            "type": "object",
            "additionalProperties": {
                "$ref": "#/definitions/BaseTerm"
            }   
        },
        "citations": {
            "additionalProperties": {
                "$ref": "#/definitions/Citation"
            },
            "type": "object"
        },

        "edges": {
            "additionalProperties": {
                "$ref": "#/definitions/Edge"
            },
            "type": "object"
        },
        "externalId": {
            "type": "string"
        },
        "functionTerms": {
            "additionalProperties": {
                "$ref": "#/definitions/FunctionTerm"
            },
            "type": "object"
        },
        "isComplete": {
            "type": "boolean"
        },
        "isLocked": {
            "type": "boolean"
        },
        "modificationTime": {
            "type": "number"
        },
        "name": {
            "type": "string"
        },
        "namespaces": {
            "additionalProperties": {
                "$ref": "#/definitions/Namespace"
            },
            "type": "object"
        },
        "nodeCount": {
            "type": "integer"
        },
        "nodes": {
            "additionalProperties": {
                "$ref": "#/definitions/Node"
            },
            "type": "object"
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
        "reifiedEdgeTerms": {
            "additionalProperties": {
                "$ref": "#/definitions/ReifiedEdgeTerm"
            },
            "type": "object"
        },
        "supports": {
            "additionalProperties": {
                "$ref": "#/definitions/Support"
            },
            "type": "object"
        },
        "type": {
            "type": "string"
        },
        "uri": {
            "type": "string"
        },
        "version": {
            "type": "string"
        },
        "visibility": {
            "enum": [
                "PUBLIC",
                "PRIVATE",
                "DISCOVERABLE"
            ],
            "type": "string"
        }
    },
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




