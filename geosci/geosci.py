"""Main module."""

import os
import ipyleaflet
from .utils import random_string
from ipyleaflet import FullScreenControl, LayersControl, DrawControl, MeasureControl, ScaleControl, basemaps, TileLayer, GeoJSON


class Map(ipyleaflet.Map):
    """this map class inherits the ipyleaflet Map class

    Args:
        ipyleaflet (ipyleaflet.Map): An ipyleaflet map
    """    
    def __init__(self, **kwargs):

        if "center" not in kwargs:
            kwargs["center"] = [40, 100]
        if "zoom" not in kwargs:
            kwargs["zoom"] = 4
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True
        super().__init__(**kwargs)
        if "height" not in kwargs:
            self.layout.height = "500px" 
        else:
            self.layout.height = kwargs["height"]
    
        self.add_control(FullScreenControl())
        self.add_control(LayersControl(position="topright"))
        self.add_control(DrawControl(position="topleft"))
        self.add_control(MeasureControl())
        self.add_control(ScaleControl(position="bottomleft"))

        if "google_map" not in kwargs:
            layer = TileLayer(
            url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
            attribution="Google",
            name="Google Maps",
            )
            self.add_layer(layer)
        else:
            if kwargs["google_map"] == "ROADMAP":
                layer = TileLayer(
                url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
                attribution="Google",
                name="Google Satellite"
                )
                self.add_layer(layer)
            elif kwargs["google_map"] == "HYBRID":
                layer = TileLayer(
                url="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
                attribution="Google",
                name="Google Satellite"
                )
                self.add_layer(layer)

    def add_geojson(self, in_geojson, style= None, layer_name= "Untitled"):
        """adds a Geojson to the map

        Args:
            in_geojson (str): The file path of the input Geojson
            style (dict, optional): The style of the Geojson layer. Defaults to None.
            layer_name (str, optional): The layer name for the Geojson layer. Defaults to "Untitled".

        Raises:
            FileNotFoundError: If the provided file path does not exsit.
            TypeError: If the input Geojson is not a str or dict.
        """        
        import json

        if layer_name == "Untitled":
            layer_name = "Untitled " + random_string()

        if isinstance(in_geojson, str):

            if not os.path.exists(in_geojson):
                raise FileNotFoundError("The provided GeoJSON file could not be found.")

            with open(in_geojson) as f:
                data = json.load(f)

        elif isinstance(in_geojson, dict):
            data = in_geojson
        
        else:
            raise TypeError("The input geojson must be a type of str or dict.")

        if style is None:
            style = {
                "stroke": True,
                "color": "#000000",
                "weight": 2,
                "opacity": 1,
                "fill": True,
                "fillColor": "#0000ff",
                "fillOpacity": 0.4,
            }

        geo_json = ipyleaflet.GeoJSON(data= data, style= style, layer_name=layer_name)
        self.add_layer(geo_json)

    def add_shp(self, in_shp, style= None,layer_name = "Untitled"):
        """Adds a shapefile layer to the map.
        Args:
            in_shp (str): The file path to the input shapefile.
            style (dict, optional): The style dictionary. Defaults to None.
            layer_name (str, optional): The layer name for the shapefile layer. Defaults to "Untitled".
        """
        geojson = shp_to_geojson(in_shp)
        self.add_geojson(geojson, style= style, layer_name= layer_name)


def shp_to_geojson(in_shp, out_geojson=None):
    """Converts a shapefile to GeoJSON.
    Args:
        in_shp (str): The file path to the input shapefile.
        out_geojson (str, optional): The file path to the output GeoJSON. Defaults to None.
    Raises:
        FileNotFoundError: If the input shapefile does not exist.
    Returns:
        dict: The dictionary of the GeoJSON.
    """
    import json
    import shapefile

    in_shp = os.path.abspath(in_shp)

    if not os.path.exists(in_shp):
        raise FileNotFoundError("The provided shapefile could not be found.")

    sf = shapefile.Reader(in_shp)
    geojson = sf.__geo_interface__

    if out_geojson is None:
        return geojson
    else:
        out_geojson = os.path.abspath(out_geojson)
        out_dir = os.path.dirname(out_geojson)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        with open(out_geojson, "w") as f:
            f.write(json.dumps(geojson))