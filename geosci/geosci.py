"""Main module."""

import os
import ipyleaflet
# from .utils import random_string
from ipyleaflet import FullScreenControl, LayersControl, DrawControl, MeasureControl, ScaleControl, basemaps, TileLayer, GeoJSON

class Map(ipyleaflet.Map):

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
        """Adds a GeoJSON file to the map.
        Args:
            in_geojson (str): The file path to the input GeoJSON.
            style (dict, optional): The style for the GeoJSON layer. Defaults to None.
            layer_name (str, optional): The layer name for the GeoJSON layer. Defaults to "Untitled".
        Raises:
            FileNotFoundError: If the provided file path does not exist.
            TypeError: If the input geojson is not a str or dict.
        """
        import json
    # 
    # import random
    # import requests

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

        geo_json = ipyleaflet.GeoJSON(data=data, style=style, name=layer_name)
        self.add_layer(geo_json)
