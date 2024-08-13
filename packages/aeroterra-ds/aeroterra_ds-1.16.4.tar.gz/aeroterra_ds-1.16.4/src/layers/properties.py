import requests

from arcgis.geometry.filters import intersects

import json

from shapely.geometry import Polygon

from .common import get_fields_aux, get_display_field_aux
from .gets import get_layer, get_item

from geometry.geometry import create_geo_json
from geometry.change_crs import change_crs

def get_fields(gis, layer_id, number=None):
    """
    Returns a list of the fields of a layer
    
    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be read
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
    
    Returns a list of tuples of type (name, alias, field type)
    """
    layer = get_layer(gis, layer_id, number)
    
    return get_fields_aux(layer)


def get_objectid_field_aux(layer):
    """
    Returns the name of the field that works as the objectID field
    
    Parameters:
        - layer: Layer Item of the structure looking to be read
    """
    fields = get_fields_aux(layer)
    
    for field in fields:
        if field[2] == "ObjectID":
            return field[0]
    
    raise Exception(f"Couldn't Find ObjectID Field Between Given Fields [{fields}]")


def get_objectid_field(gis, layer_id, number=None):
    """
    Returns the name of the field that works as the objectID field
    
    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be read
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
    """
    layer = get_layer(gis, layer_id, number)
    
    return get_objectid_field_aux(layer)


def get_symbology_aux(layer):
    """
    Returns the symbology data of a given layer
    
    Parameters:
        - layer: Layer Item of the structure looking to be read
    """
    return layer.properties.drawingInfo


def get_symbology(gis, layer_id, number=None):
    """
    Returns the symbology data of a given layer
    
    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be read
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
    """
    layer = get_layer(gis, layer_id, number)
    
    return get_symbology_aux(layer)


def get_spatial_reference_api(layer, verify=True):
    """
    Returns the spatial reference of a given layer asking to the api
    
    Parameters:
        - layer: Layer Item of the structure looking to be read
        - verify (Optional): If it should verify SSL Certificates.
            By default in True
    """
    gis = layer._gis
    item = get_item(gis, layer.properties.serviceItemId)

    url_base = item.url
    token = gis._con.token
    ask_url = url_base + f"?f=json&token={token}"

    response_api = requests.get(ask_url, verify=verify)
    if response_api.status_code // 100 != 2:
        raise Exception("Could Not Connect To REST API")
    
    data = response_api.json()
    spatial_reference = data["spatialReference"]

    return spatial_reference


def get_layer_crs_aux(layer):
    """
    Returns the spatial reference of a given layer

    Parameters:
        - layer: Layer Item of the structure looking to be read
    """
    properties = layer.properties
    if properties is None:
        spatial_reference = get_spatial_reference_api(layer)
    else:
        extent = properties["extent"]
        if extent is None:
            spatial_reference = get_spatial_reference_api(layer)
        else:
            spatial_reference = extent["spatialReference"]

    if "latestWkid" in spatial_reference:
        crs = spatial_reference["latestWkid"]
    elif "wkid" in spatial_reference:
        crs = spatial_reference["wkid"]
    else:
        raise Exception(f"CRS Cant't Be Found In Spatial Reference {spatial_reference}")

    return crs


def get_layer_crs(gis, layer_id, number=None):
    """
    Returns the spatial reference of a given layer
    
    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be read
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
    """
    layer = get_layer(gis, layer_id, number)
    
    return get_layer_crs_aux(layer)


def get_layer_extent_aux(layer, out_crs=None):
    """
    Returns the extent of a given layer
    
    Parameters:
        - layer: Layer Item of the structure looking to be read
        - out_crs (Optional): The CRS to get the extent in. If None,
            the crs of the layer will be used. By default in None.
    """
    extent = layer.properties["extent"]

    min_x = extent["xmin"]
    max_x = extent["xmax"]
    min_y = extent["ymin"]
    max_y = extent["ymax"]

    polygon = Polygon([(min_x, min_y), (min_x, max_y), (max_x, max_y), (max_x, min_y)])

    if out_crs:
        crs = get_layer_crs_aux(layer)
        polygon = change_crs(layer, crs, out_crs)

    return polygon


def get_layer_extent(gis, layer_id, number=None, out_crs=None):
    """
    Returns the extent of a given layer
    
    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be read
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
        - out_crs (Optional): The CRS to get the extent in. If None,
            the crs of the layer will be used. By default in None.
    """
    layer = get_layer(gis, layer_id, number)
    
    return get_layer_extent_aux(layer)




def get_display_field(gis, layer_id, number=None):
    """
    Returns the display field of a given layer
    
    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be read
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
    """
    layer = get_layer(gis, layer_id, number)
    
    return get_display_field_aux(layer)



def get_layer_geom_type_aux(layer):
    """
    Returns the geometry type of a given layer
    
    Parameters:
        - layer: Layer Item of the structure looking to be read
    """
    geom_type = layer.properties["geometryType"]

    return geom_type


def get_layer_geom_type(gis, layer_id, number=None):
    """
    Returns the geometry type of a given layer
    
    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be read
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
    """
    layer = get_layer(gis, layer_id, number)
    
    return get_layer_geom_type_aux(layer)


def get_pop_up(gis, layer_id, number=None):
    """
    Returns the popupInfo of a given layer
    
    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be read
        - number(Optional): Number layer of the layer wanting to be read. If
            not set, default at 0
    """
    layer_item = get_item(gis, layer_id)
    
    layers_data = layer_item.get_data()

    if "layers" not in layers_data:
        layers = layer_item.layers
        if number >= len(layers):
            raise Exception(f"Layer Number {number} Can't Be Found Inside Item {layer_id}")
        return {}            
    
    layer_data = None
    for layer in layers_data["layers"]:
        if layer["id"] == number:
            layer_data = layer
            break
    
    if layer_data is None:
        raise Exception(f"Layer Number {number} Can't Be Found Inside Item {layer_id}")
    
    if "popupInfo" in layer_data:
        popup_data = layer_data["popupInfo"]
    else:
        popup_data = {}
    
    return popup_data


def get_items_amount_aux(layer, query="1=1", geometry_filter=None, geometry_crs=4326):
    """
    Returns the amount of items saved in layer
    
    Parameters:
        - layer: Layer Item of the structure looking to be read
        - query (Optional): String representing a SQL query to filter the data to 
            to be read from the layer. If None, all the data will be providen.
        - geometry_filter (Optional): Shapely (Multi)Polygon to filter data geographically.
            If None, all the data will be providen.
        - geometry_crs (Optional): CRS of the given geometry_filer. If missing, 4326 will be assumed.
    """
    geo_filter = None
    if geometry_filter is not None:
        bounds = create_geo_json(geometry_filter, geometry_crs)
        geo_filter = intersects(bounds)

    return layer.query(where = query, geometry_filter=geo_filter, return_count_only=True)


def get_items_amount(gis, layer_id, number=None):
    """
    Returns the amount of items saved in layer
    
    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be read
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
    """
    layer = get_layer(gis, layer_id, number)
    
    return get_items_amount_aux(layer)


def refresh_layer_aux(layer, verify=True):
    """
    Refresh a given layer

    Parameters:
        - layer: Layer Item of the structure looking to be read
        - verify (Optional): If it should verify SSL Certificates.
            By default in True
    """
    gis = layer._gis

    url_base = layer.url
    token = gis._con.token
    ask_url = url_base + f"/refresh?f=json&token={token}"

    response_api = requests.get(ask_url, verify=verify)
    if response_api.status_code // 100 != 2:
        raise Exception("Could Not Connect To REST API")
    
    data = response_api.json()

    return data


def refresh_layer(gis, layer_id, number=None, verify=True):
    """
    Refresh a given layer

    Parameters:
        - gis: GIS struct from the user that owns the layer
        - layer_id: Layer ID of the layer wanting to be read
        - number (Optional): Layer Number inside the item. If not provided
            it'll be assumed the item should only have 1 layer
        - verify (Optional): If it should verify SSL Certificates.
            By default in True
    """
    layer = get_layer(gis, layer_id, number)
    
    return refresh_layer_aux(layer, verify)