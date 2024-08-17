from typing import Union, List, Tuple

ESRI_DATA_TYPES = {"esriFieldTypeOID": "ObjectID", "esriFieldTypeString": "str", "esriFieldTypeDouble": "float", "esriFieldTypeDate": "datetime", "esriFieldTypeGlobalID": "GlobalID", "esriFieldTypeInteger": "int", "esriFieldTypeSmallInteger": "int"}
PYTHON_DATA_TYPES = {'ObjectID': 'esriFieldTypeOID', 'str': 'esriFieldTypeString', 'float': 'esriFieldTypeDouble', 'datetime': 'esriFieldTypeDate', 'GlobalID': 'esriFieldTypeGlobalID', 'int': 'esriFieldTypeInteger'}

BBOX_TYPE = Union[List[float], Tuple[float]]

FEATURE_LAYER_TYPE = "Feature Service"
WEBMAP_ITEM_TYPE = "Web Map"

