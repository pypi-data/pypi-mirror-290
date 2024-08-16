"""Tests for the SuburbNetwork class."""

from typing import TYPE_CHECKING

import pytest

from sydneysuburbs.generators import generate_test

if TYPE_CHECKING:
    from sydneysuburbs.suburb_network import SuburbNetwork


@pytest.fixture
def load_network() -> "SuburbNetwork":
    """Loads the test suburb network.

    Returns:
        Test suburb network object
    """
    return generate_test()


def test_suburb_network(load_network: "SuburbNetwork"):
    """Tests creating the test SuburbNetwork object."""
    sn = load_network
    print(sn.name)


def test_add_bridge(load_network: "SuburbNetwork"):
    """Tests adding a bridge to the SuburbNetwork."""
    sn = load_network

    # test adding a bridge with id
    c_id = sn.get_suburb_id_by_name("concord")
    a_id = sn.get_suburb_id_by_name("ashfield")
    sn.add_bridge(suburb1=c_id, suburb2=a_id)

    # test neighbours
    assert c_id in sn.weights.neighbors[a_id]
    assert a_id in sn.weights.neighbors[c_id]

    # test adding a bridge with name
    r_id = sn.get_suburb_id_by_name("rhodes")
    a_id = sn.get_suburb_id_by_name("ashfield")
    sn.add_bridge(suburb1="rhodes", suburb2="ashfield")

    # test neighbours
    assert r_id in sn.weights.neighbors[a_id]
    assert a_id in sn.weights.neighbors[r_id]

    # test already neighbours
    with pytest.raises(RuntimeError, match="There is already a connection between"):
        sn.add_bridge(suburb1="ashfield", suburb2="summer hill")


def test_get_suburb_id(load_network: "SuburbNetwork"):
    """Tests the get id method."""
    sn = load_network

    # get ashfield id from dataframe
    a_id = sn.df[sn.df["suburbname"] == "Ashfield"].index.tolist()[0]

    assert sn.get_suburb_id_by_name("ashfield") == a_id
    assert sn.get_suburb_id_by_name("Ashfield") == a_id
    assert sn.get_suburb_id_by_name("AshFielD") == a_id

    # test cannot find
    with pytest.raises(ValueError, match="Cannot find suburb:"):
        sn.get_suburb_id_by_name("ahfield")


def test_get_suburb(load_network: "SuburbNetwork"):
    """Tests the get suburb method."""
    sn = load_network

    ashfield = sn.get_suburb_by_name("ashfield")

    assert ashfield.name == "Ashfield"
    assert ashfield.postcode == 2131

    # test cannot find
    with pytest.raises(ValueError, match="Cannot find suburb:"):
        sn.get_suburb_by_name("ahfield")
