import json
import pandas as pd

from .features import Feature, FeatureCollection


class GISManager:
    """
    Class to make geojson objects from cytoscape data.
    - turn Cytoscape Nodes into Point geojson objects
    - turn Cytoscape Edges into LineString geojson objects

    expects a config dictionary
    * cyto_path - specifies path to the .cyjs Cytoscape file: str
    * coord_path - specifies path to a csv containing lat and long for the places: str
    * lat_long_cols - specifies the names of the columns containing lat and long coordinates: tuple
    optional:
    * cols_to_drop - specifies which cols from the csv containing the coordinates should be dropped: list

    """

    def __init__(self, config) -> None:
        self.config = config
        self.list_of_nodes, self.list_of_edges = self._get_nodes_edges()
        self.coordinates_data = self._map_locations()
        self.unique_locations = self._get_location_set(self.coordinates_data)

    def _read_data_cyto(self) -> dict:
        """
        func to read cytoscape json files
        :return: dict
        """
        try:
            with open(self.config["cyto_path"], 'r') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            self.config['cyto_path'] = input(
                f"File not found: {self.config['cyto_path']}, please provide a valid path to file:")
            return self._read_data_cyto()
        except OSError:
            self.config['cyto_path'] = input(
                f"Corrupted path: {self.config['cyto_path']}.  does the path you provided contain ' or \"? ")
            return self._read_data_cyto()

    def _get_nodes_edges(self) -> tuple:
        """
        func to slice cyto json in to nodes and edges.
        :return: tuple of lists of dicts representing the cytoscape objects
        """
        data = self._read_data_cyto()
        nodes = data["elements"]["nodes"]
        edges = data["elements"]["edges"]
        return nodes, edges

    def _map_locations(self, delimiter: str = ";") -> pd.DataFrame:
        """
        func to map locations to coordinates. only uses locations that have associated coordinates.
        :return: pd.DataFrame containing the places and their respective coordinates
        """
        lat, long = self.config["lat_long_cols"]
        # read in data from csv
        locations_data = pd.read_csv(self.config["coord_path"], delimiter=delimiter)
        # drop unnecessary cols if configured to do so
        if "cols_to_drop" in self.config.keys():
            locations_data.drop(self.config["cols_to_drop"], axis=1, inplace=True)
        # drop NAN containing rows
        locations_data.dropna(axis=0, inplace=True)
        # filter "undefined"
        locations_data = locations_data[(locations_data[lat] != "undefined") & (locations_data[long] != "undefined")]
        return locations_data

    def create_features_edges(self) -> FeatureCollection:
        """
        method produces LineString geojson objects, puts them into a geojson FeatureCollection
        and returns the FeatureCollection.
        :return: FeatureCollection of network edges
        """
        # create collection
        collection = FeatureCollection()
        for line_string in self._make_line_strings():
            collection.add_feature(line_string)
        return collection

    def create_features_nodes(self) -> FeatureCollection:
        """
        method produces Point objects for geojson. Returns a Feature collection in geojson object.
        :return: FeatureCollection of network nodes
        """
        collection = FeatureCollection()

        for node in self.list_of_nodes:

            # validate city has data
            if node["data"].get("lat") and node["data"].get("lat") != "undefined":
                # get coordinates
                lat = node["data"]["lat"]
                lng = node["data"]["lng"]
                # float them
                coordinates = [float(lng.lstrip("0")), float(lat.lstrip("0"))]

                # create feature
                feature = Feature("Point", coordinates,
                                  properties={"name": node["data"]["id"], "typ": node["data"]["Typ"],
                                              "connections": None}
                                  )
                # append current feature to feature list

                collection.add_feature(feature.populated_obj)

        return collection

    def _make_line_strings(self) -> list:
        """
        func to make LineString objects for geojson.
        :return: list of Linestring objects.
        """
        unique_locations = self.unique_locations
        locations_map = self._dataframe_to_dict(self.coordinates_data)
        list_of_edges = []
        edges = self.list_of_edges
        edges = self._get_connections(edges)
        for source, targets in edges.items():

            # check if source has coordinates
            if source in unique_locations:

                source_coordinates = locations_map[source]
                for target in targets:
                    target_items = list(target.items())
                    target_name, weight = target_items[0]
                    # check if target has coordinates
                    if target_name in unique_locations:
                        target_coordinates = locations_map[target_name]
                        coordinates = [source_coordinates, target_coordinates]
                        edge = Feature("LineString", coordinates,
                                       properties={"source": source, "target": target_name, "weight": weight})
                        list_of_edges.append(edge.populated_obj)
        return list_of_edges

    @staticmethod
    def _get_connections(edges: list) -> dict:
        """
        func to get a dict with all locations and their respective outward communications(target: amount of letters)
        :param edges: list
        :return: dict with source of letter as key and targets as values
        """
        all_edges = {}  # a dictionary to store connections

        # loop through edges
        for edge in edges:
            data = edge["data"]
            source = data["source"]
            weight = data["weight"]
            target = data["target"]

            # Create a dictionary for the current target and weight
            target_city = {target: weight}

            # Create or update the edge dictionary for the source city
            if source in all_edges:
                all_edges[source].append(target_city)
            else:
                all_edges[source] = [target_city]

        return all_edges

    @staticmethod
    def _dataframe_to_dict(df: pd.DataFrame) -> dict:
        """
        helper method: takes a pd.DataFrame and (re)turns it in to a dictionary.
        :param df: pd.DataFrame
        :return: dict
        """
        places_dict = {}

        for index, row in df.iterrows():
            place = row["Ort"]
            lat = row["Lat"]
            lon = row["Len"]

            places_dict[place] = [float(lon), float(lat)]

        return places_dict

    @staticmethod
    def _get_location_set(location_df: pd.DataFrame) -> set:
        """
        func to get a set of locations that have coordinates
        :param location_df:
        :return: set of unique locations that contain coordinates
        """
        locations_set = set(location_df["Ort"].unique())
        return locations_set
