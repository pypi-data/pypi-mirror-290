import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from text_to_sidc import austrian

from milgeo import FeatureBuilder, PlacemarkBuilder
from milgeo import ColorFinder
from milgeo import PlatformType, ReliabilityCredibility


@dataclass
class Geometry:
    name: str
    coordinates: List
    metadata: Dict[str, List[str]] = field(default_factory=lambda: defaultdict(list))

    id: Optional[str] = None
    sidc: Optional[str] = None
    observation_datetime: Optional[str] = None
    reliability_credibility: Optional[ReliabilityCredibility] = None
    staff_comments: Optional[str] = None
    platform_type: Optional[PlatformType] = None
    quantity: Optional[str] = None
    direction: Optional[str] = None
    speed: Optional[str] = None
    comments: Optional[str] = None
    outline_color: Optional[str] = None
    fill_color: Optional[str] = None
    fill_opacity: Optional[str] = None

    def __post_init__(self):
        if self.sidc and len(self.sidc) != 20:
            raise ValueError("sidc must be exactly 20 digits.")

        if self.platform_type and not isinstance(self.platform_type, PlatformType):
            raise ValueError("platform_type must be an instance of PlatformType.")

        if not self.coordinates:
            raise ValueError("coordinates cannot be empty.")

        if isinstance(self.coordinates, list):
            if isinstance(self, Polygon):
                for ring in self.coordinates:
                    if len(ring) < 4:
                        raise ValueError("Each LinearRing in a Polygon must have at least 4 coordinate tuples.")
                    if ring[0] != ring[-1]:
                        raise ValueError("The first and last coordinate pairs in a LinearRing must be the same.")
            elif isinstance(self, Line) and len(self.coordinates) < 2:
                raise ValueError("LineString must have at least 2 coordinate tuples.")

        if self.reliability_credibility and not isinstance(self.reliability_credibility, ReliabilityCredibility):
            raise ValueError(
                f"reliability_credibility '{self.reliability_credibility}' is not a valid ReliabilityCredibility value.")

        hex_color_pattern = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{8})$')

        if self.outline_color and not hex_color_pattern.match(self.outline_color):
            raise ValueError(f"outline_color '{self.outline_color}' is not a valid HEX color.")

        if self.fill_color:
            if not hex_color_pattern.match(self.fill_color):
                raise ValueError(f"fill_color '{self.fill_color}' is not a valid HEX color.")
            if not self.fill_opacity or not 0 <= float(self.fill_opacity) <= 1:
                raise ValueError(
                    f"fill_opacity '{self.fill_opacity}' must be a number between 0 and 1 when fill_color is specified.")

        if self.observation_datetime:
            try:
                datetime.strptime(self.observation_datetime, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                raise ValueError(
                    f"observation_datetime '{self.observation_datetime}' "
                    f"is not a valid timestamp in the format yyyy-MM-ddThh:mm:ss.")

        if self.quantity:
            try:
                int_quantity = int(self.quantity)
                if str(int_quantity) != self.quantity:
                    raise ValueError()
            except ValueError:
                raise ValueError(f"quantity '{self.quantity}' must be a string representing an integer.")

    @property
    def geometry_type(self):
        raise NotImplementedError("Subclasses should implement this property")

    @property
    def default_sidc(self):
        raise NotImplementedError("Subclasses should implement this property")

    def find_outline_color(self, string: str, finder=ColorFinder()):
        self.outline_color = finder.find_hex_color(string)

    def find_sidc(self, string: str, unit_designator=austrian.UnitDesignator()):
        if isinstance(self, Point):
            self.sidc = unit_designator.calculate_icon(string)

    def to_feature(self):
        builder = FeatureBuilder(self)
        builder.add_basic_elements()
        builder.add_optional_properties()
        builder.add_geometry()
        return builder.build()

    def to_placemark(self):
        builder = PlacemarkBuilder(self)
        builder.add_basic_elements()
        builder.add_optional_properties()
        builder.add_geometry()
        return builder.build()


@dataclass
class Point(Geometry):
    coordinates: List[float]

    @property
    def geometry_type(self):
        return "Point"

    @property
    def default_sidc(self):
        return "10012500001313000000"


@dataclass
class Line(Geometry):
    coordinates: List[List[float]]

    @property
    def geometry_type(self):
        return "LineString"

    @property
    def default_sidc(self):
        return "10016600001100000000"


@dataclass
class Polygon(Geometry):
    coordinates: List[List[List[float]]]

    @property
    def geometry_type(self):
        return "Polygon"

    @property
    def default_sidc(self):
        return "10012500001505010000"


class GeometriesList:
    def __init__(self):
        self.geometries = []

    def add_geometry(self, geometry: Geometry):
        if not isinstance(geometry, Geometry):
            raise ValueError("Only Geometry objects can be added.")
        self.geometries.append(geometry)

    def remove_geometry(self, geometry: Geometry):
        self.geometries.remove(geometry)

    def find_by_name(self, name: str) -> Optional[Geometry]:
        for geometry in self.geometries:
            if geometry.name == name:
                return geometry
        return None

    def get_all_geometries(self) -> List[Geometry]:
        return self.geometries

    def count_geometries(self) -> int:
        return len(self.geometries)

    def remove_duplicates(self, fields: List[str]):
        def make_hashable(value):
            if isinstance(value, list):
                return tuple(make_hashable(v) for v in value)
            return value

        seen = set()
        unique_geometries = []

        for geometry in self.geometries:
            comparison_tuple = tuple(make_hashable(getattr(geometry, attr)) for attr in fields)
            if comparison_tuple not in seen:
                seen.add(comparison_tuple)
                unique_geometries.append(geometry)

        self.geometries = unique_geometries

    def find_outline_colors(self):
        finder = ColorFinder()
        for geometry in self.geometries:
            concat_string = ''.join(filter(None, [geometry.name, geometry.comments, geometry.outline_color]))
            if concat_string:
                geometry.find_outline_color(concat_string, finder)

    def find_sidcs(self):
        for geometry in self.geometries:
            concat_string = ''.join(filter(None, [geometry.name, geometry.comments, geometry.outline_color]))
            if concat_string:
                geometry.find_sidc(concat_string)

    def to_features(self):
        return [geometry.to_feature() for geometry in self.geometries]

    def to_placemarks(self):
        return [geometry.to_placemark() for geometry in self.geometries]

    def __str__(self):
        return "\n".join(str(geometry) for geometry in self.geometries)

    def __iter__(self):
        return iter(self.geometries)

    def __len__(self):
        return len(self.geometries)

    def __contains__(self, item):
        return item in self.geometries
