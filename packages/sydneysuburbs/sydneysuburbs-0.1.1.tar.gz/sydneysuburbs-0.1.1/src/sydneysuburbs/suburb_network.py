"""Class for a network of suburbs."""

from importlib import resources as impresources

import geopandas as gp
import libpysal.weights as pysal_weights
import networkx as nx
import topojson as tp

from sydneysuburbs import data
from sydneysuburbs.suburb import Suburb


class SuburbNetwork:
    """Class for a network of suburbs.

    Attributes:
        name: Suburb network name
        suburbs: List of suburb objects
        suburbs_sorted: List of suburb objects (sorted alphabetically)
        df: Geopandas dataframe containing suburb data
        df_gps: Geopandas dataframe converted to EPSG4326 for plotting
        weights: libpysal weights object
        graph: Networkx graph object
    """

    name: str
    suburbs: list[Suburb]
    suburbs_sorted: list[Suburb]
    df: gp.GeoDataFrame
    df_gps: gp.GeoDataFrame
    weights: pysal_weights.W
    graph: nx.Graph

    def __init__(
        self,
        name: str,
        filename: str,
    ) -> None:
        """Inits the SuburbNetwork class.

        Args:
           name: Suburb network name
           filename: Path to suburbs json file.
        """
        self.name = name
        self.load_suburbs(filename=filename)
        self.generate_graph()

    def load_suburbs(
        self,
        filename: str,
    ) -> None:
        """Loads suburbs from json file.

        Note the json file is obtained from
        https://portal.spatial.nsw.gov.au/portal/home/item.html?id=9dc2caa5f5f4418a87c7913b231b7b66
        and is titled "NSW Administrative Boundaries Theme". The suburb layer should be
        exported.

        Args:
            filename: Path to suburbs json file.
        """
        # reset suburb list
        self.suburbs = []

        # get filename
        fn = impresources.files(data) / filename

        # load suburb json file into a geopandas dataframe
        self.df = gp.read_file(
            filename=fn,
            columns=["suburbname", "postcode", "Shape__Length", "Shape__Area"],
        )

        # change suburbs to title case
        self.df["suburbname"] = self.df["suburbname"].str.title()

        # transform geometry to MGA zone 56 (epsg 7856)
        self.df.to_crs(epsg=7856, inplace=True)

        # calculate the centroids of each suburb and store in "centroid" column
        self.df["centroid"] = self.df.centroid

        # simplify geometry for plotting & convert to gps
        topo = tp.Topology(self.df, prequantize=True)

        # convert to gps coords for plotting
        self.df_gps = topo.toposimplify(epsilon=20).to_gdf().to_crs(epsg=4326)  # type: ignore

        # create suburb objects and store in self.suburbs
        for row in self.df.itertuples(index=True):
            suburb = Suburb(
                # name=row.suburbname,
                name=getattr(row, "suburbname"),
                sub_id=getattr(row, "Index"),
                postcode=getattr(row, "postcode"),
                perimeter=getattr(row, "Shape__Length"),
                area=getattr(row, "Shape__Area"),
                geometry=getattr(row, "geometry"),
                centroid=getattr(row, "centroid"),
            )
            self.suburbs.append(suburb)

        # sort suburbs alphabetically
        self.suburbs_sorted = sorted(self.suburbs, key=lambda suburb: suburb.name)

    def generate_graph(self) -> None:
        """Generates the libpysal weights and Networkx graph objects."""
        # generate list of polygon objects and suburb ids
        polygons = []
        ids = []

        for suburb in self.suburbs:
            polygons.append(suburb.geometry)
            ids.append(suburb.sub_id)

        # construct rook adjacency graph (must share an edge)
        self.weights = pysal_weights.Rook(polygons=polygons, ids=ids)

        # convert the graph to a networkx object
        self.graph = self.weights.to_networkx()

    def add_bridge(
        self,
        suburb1: str | int,
        suburb2: str | int,
    ) -> None:
        """Adds a connection between two suburbs.

        Args:
            suburb1: Suburb 1 name or id
            suburb2: Suburb 2 name or id

        Raises:
            RuntimeError: If there is already a connection between the two suburbs
            ValueError: If suburb cannot be found
        """
        # get suburb ids
        if isinstance(suburb1, str):
            suburb1 = self.get_suburb_id_by_name(suburb_name=suburb1)

        if isinstance(suburb2, str):
            suburb2 = self.get_suburb_id_by_name(suburb_name=suburb2)

        # check bridge doesn't already exist
        if suburb1 in self.weights.neighbors[suburb2]:
            msg = f"There is already a connection between {suburb1} and {suburb2}."
            raise RuntimeError(msg)

        # get current list of neighbours
        neighbors = self.weights.neighbors

        # add bridge
        neighbors[suburb1].append(suburb2)
        neighbors[suburb2].append(suburb1)

        # regenerate weights and graph
        self.weights = pysal_weights.W(neighbors=neighbors)
        self.graph = self.weights.to_networkx()

    def get_suburb_id_by_name(
        self,
        suburb_name: str,
    ) -> int:
        """Gets a suburb id by name.

        Args:
            suburb_name: Suburb name

        Raises:
            ValueError: If suburb cannot be found

        Returns:
            Suburb id
        """
        for sub in self.suburbs:
            if sub.name.lower() == suburb_name.lower():
                return sub.sub_id
        else:
            raise ValueError(f"Cannot find suburb: {suburb_name}.")

    def get_suburb_by_name(
        self,
        suburb_name: str,
    ) -> Suburb:
        """Gets a suburb object by name.

        Args:
            suburb_name: Suburb name

        Raises:
            ValueError: If suburb cannot be found

        Returns:
            Suburb object
        """
        return self.suburbs[self.get_suburb_id_by_name(suburb_name=suburb_name)]
