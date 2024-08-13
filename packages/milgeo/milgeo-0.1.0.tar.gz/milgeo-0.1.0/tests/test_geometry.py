import pytest

from milgeo import GeometriesList, Point, Line, Polygon


@pytest.mark.parametrize("name, coordinates, geometry_type, sidc, fill_color, fill_opacity, "
                         "observation_datetime, quantity, expected_exception", [
                             ("Valid input", [(0, 0)], "Point", "12345678901234567890", "#ff0000", "0.5", None, None, None),
                             ("Invalid SIDC length", [(0, 0)], "Point", "123456", None, None, None, None, ValueError),
                             ("Invalid fill color", [(0, 0)], "Point", None, "not_a_color", None, None, None, ValueError),
                             ("Invalid fill opacity", [(0, 0)], "Point", None, "#ff0000ff", "2", None, None, ValueError),
                             ("Invalid observation datetime", [(0, 0)], "Point", None, None, None, "2020-13-01T00:00:00", None,
                              ValueError),
                             ("Invalid quantity", [(0, 0)], "Point", None, None, None, None, "12.5", ValueError),
                             ("Empty coordinates", [], "Point", None, None, None, None, None, ValueError),
                             ("Invalid Polygon coordinates", [[[0, 0], [1, 1]]], "Polygon", None, None, None, None, None, ValueError),
                             ("Invalid Polygon LinearRing", [[[0, 0], [1, 1], [2, 2], [3, 3]]], "Polygon", None, None, None, None, None, ValueError),
                             ("Invalid LineString coordinates", [[0, 0]], "LineString", None, None, None, None, None, ValueError),
                         ])
def test_geometry_post_init(name, coordinates, sidc, geometry_type, fill_color, fill_opacity,
                            observation_datetime, quantity, expected_exception):

    geometry_class = None
    if geometry_type == "Polygon":
        geometry_class = Polygon
    elif geometry_type == "Point":
        geometry_class = Point
    elif geometry_type == "LineString":
        geometry_class = Line
    if expected_exception:
        with pytest.raises(expected_exception):
            geometry_class(
                name=name,
                coordinates=coordinates,
                sidc=sidc,
                fill_color=fill_color,
                fill_opacity=fill_opacity,
                observation_datetime=observation_datetime,
                quantity=quantity
            )
    else:
        geom = geometry_class(
            name=name,
            coordinates=coordinates,
            sidc=sidc,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
            observation_datetime=observation_datetime,
            quantity=quantity
        )
        assert geom.name == name
        assert geom.coordinates == coordinates
        assert geom.sidc == sidc
        assert geom.fill_color == fill_color
        assert geom.fill_opacity == fill_opacity
        assert geom.observation_datetime == observation_datetime
        assert geom.quantity == quantity


@pytest.mark.parametrize("geometries, fields, expected_names", [
    (
            [
                Point(name="Point", coordinates=[1.0, 2.0]),
                Point(name="Point", coordinates=[1.0, 2.0]),  # Duplicate
                Line(name="Line", coordinates=[[1.0, 2.0], [3.0, 4.0]]),
                Polygon(name="Polygon", coordinates=[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]]),
            ],
            ["name", "coordinates"],
            ["Point", "Line", "Polygon"]
    ),
    (
            [
                Point(name="FirstPoint", coordinates=[1.0, 2.0]),
                Point(name="SecondPoint", coordinates=[1.0, 2.0]),  # Not a duplicate based on 'name' only
                Line(name="Line", coordinates=[[1.0, 2.0], [3.0, 4.0]]),
                Line(name="Line", coordinates=[[1.0, 2.0], [3.0, 4.0]]),  # Duplicate
            ],
            ["name"],
            ["FirstPoint", "SecondPoint", "Line"]
    )
])
def test_remove_duplicates(geometries, fields, expected_names):
    geometries_list = GeometriesList()
    for geom in geometries:
        geometries_list.add_geometry(geom)

    geometries_list.remove_duplicates(fields)

    result_names = [geom.name for geom in geometries_list.get_all_geometries()]
    assert result_names == expected_names


@pytest.mark.parametrize("geometries, name_to_find, expected_geometry", [
    (
            [
                Point(name="Point", coordinates=[1.0, 2.0]),
                Line(name="Line", coordinates=[[1.0, 2.0], [3.0, 4.0]]),
            ],
            "Point",
            Point(name="Point", coordinates=[1.0, 2.0])
    ),
    (
            [
                Polygon(name="Polygon", coordinates=[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]]),
                Line(name="Line", coordinates=[[1.0, 2.0], [3.0, 4.0]]),
            ],
            "Line",
            Line(name="Line", coordinates=[[1.0, 2.0], [3.0, 4.0]])
    )
])
def test_find_by_name(geometries, name_to_find, expected_geometry):
    geometries_list = GeometriesList()
    for geom in geometries:
        geometries_list.add_geometry(geom)

    result_geometry = geometries_list.find_by_name(name_to_find)
    assert result_geometry == expected_geometry


@pytest.mark.parametrize("geometries, expected_count", [
    (
            [
                Point(name="Point", coordinates=[1.0, 2.0]),
                Line(name="Line", coordinates=[[1.0, 2.0], [3.0, 4.0]]),
                Polygon(name="Polygon", coordinates=[[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]]),
            ],
            3
    ),
    (
            [
                Point(name="FirstPoint", coordinates=[1.0, 2.0]),
                Point(name="SecondPoint", coordinates=[3.0, 4.0]),
            ],
            2
    )
])
def test_count_geometries(geometries, expected_count):
    geometries_list = GeometriesList()
    for geom in geometries:
        geometries_list.add_geometry(geom)

    assert geometries_list.count_geometries() == expected_count
    