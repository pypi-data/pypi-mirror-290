"""Class for a suburb."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shapely import MultiPolygon, Point


class Suburb:
    """Class for a suburb."""

    def __init__(
        self,
        name: str,
        sub_id: int,
        postcode: int,
        perimeter: float,
        area: float,
        geometry: "MultiPolygon",
        centroid: "Point",
    ) -> None:
        """Inits the Suburb class.

        Args:
            name: Suburb name
            sub_id: Suburb id
            postcode: Suburb postcode
            perimeter: Perimeter of the suburb
            area: Area of the suburb
            geometry: Suburb geometry
            centroid: Suburb geometric centroid
        """
        self.name = name
        self.sub_id = sub_id
        self.postcode = postcode
        self.perimeter = perimeter
        self.area = area
        self.geometry = geometry
        self.centroid = centroid

    def __repr__(self) -> str:
        """String representation of the Suburb class.

        Returns:
            String representation
        """
        return self.name
