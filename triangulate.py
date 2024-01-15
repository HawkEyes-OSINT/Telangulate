from geopy.distance import geodesic


def get_coordinates(original_coord):
    """
    Get coordinates 10 kilometers to the north, east, and south of the original coordinate.
    :input original_coord: tuple of (latitude, longitude)
    :return list of coordinates: [(latitude + 0.09, longitude), (latitude, longitude + 0.09), (latitude - 0.09, longitude)]
    :rtype: list of tuples of (latitude, longitude)
    """
    latitude = original_coord[0]
    longitude = original_coord[1]

    # Calculate coordinates 10 kilometers to the north, east, and south
    north_coord = (latitude + 0.09, longitude)
    east_coord = (latitude, longitude + 0.09)
    south_coord = (latitude - 0.09, longitude)

    return [north_coord, east_coord, south_coord]


