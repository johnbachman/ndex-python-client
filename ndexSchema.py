# -*- coding: utf-8 -*-
"""
Created on Sat Oct 18 17:04:44 2014

@author: Dexter Pratt
"""

network = {
    "$schema": "http://www.ndexbio.org/api/schema/1.0.0/Network",
    "description": "Network schema for NDEx REST API",
    "definitions": {
        "Edge": {
            "properties": {
                "citations": {
                    "items": {
                        "type": "number"
                    },
                    "type": "array"
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
        }
    },

    "properties": {
        "baseTerms": {
            "additionalProperties": {
                "$ref": "#/definitions/BaseTerm"
            },
            "type": "object"
        },
        "citations": {
            "additionalProperties": {
                "$ref": "#/definitions/Citation"
            },
            "type": "object"
        },
        "creationTime": {
            "type": "number"
        },
        "description": {
            "type": "string"
        },
        "edgeCount": {
            "type": "integer"
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
            "required": true,
            "type": "boolean"
        },
        "isLocked": {
            "required": true,
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
    "type": "object"
}






      },
      "BaseTerm" : {
        "type" : "object",
        "properties" : {
          "name" : {
            "type" : "string"
          },
          "namespace" : {
            "type" : "number"
          },
          "termType" : {
            "type" : "string"
          },
          "id" : {
            "type" : "number"
          },
          "type" : {
            "type" : "string"
          }
      },
      "FunctionTerm" : {

      },
      "ReifiedEdgeTerm" : {
        "type" : "object",
        "properties" : {
          "edgeId" : {
            "type" : "number"
          },
          "termType" : {
            "type" : "string"
          },
          "id" : {
            "type" : "number"
          },
          "type" : {
            "type" : "string"
          }
      },
      "Citation" : {

      },
      "Support" : {

      },
      "SimplePropertyValuePair" : {

      },
      "NDExPropertyValuePair" : {

      }
    },

}