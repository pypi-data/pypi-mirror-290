"""Suburb network generators."""

from sydneysuburbs.suburb_network import SuburbNetwork


def generate_test() -> SuburbNetwork:
    """Generates the test suburb network.

    Returns:
        Test suburb network object
    """
    sn = SuburbNetwork(name="test", filename="test.geojson")

    # add iron cove bridge
    sn.add_bridge("rozelle", "drummoyne")

    # add anzac bridge
    sn.add_bridge("rozelle", "pyrmont")

    return sn


def generate_inner_west() -> SuburbNetwork:
    """Generates the Inner West suburb network.

    Returns:
        Inner West suburb network object
    """
    sn = SuburbNetwork(name="test", filename="inner-west.geojson")

    # add iron cove bridge
    sn.add_bridge("rozelle", "drummoyne")

    # add anzac bridge
    sn.add_bridge("rozelle", "pyrmont")

    return sn
