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

    # Calculate coordinates 1 kilometer to the north, east, and south
    north_dist = geodesic(original_coord, (latitude + 0.009, longitude)).destination(original_coord, bearing=0)
    east_dist = geodesic(original_coord, (latitude, longitude + 0.009)).destination(original_coord, bearing=0)
    south_dist = geodesic(original_coord, (latitude - 0.009, longitude)).destination(original_coord, bearing=0)

    # create coordinates
    north_coord = (north_dist.latitude, north_dist.longitude)
    east_coord = (east_dist.latitude, east_dist.longitude)
    south_coord = (south_dist.latitude, south_dist.longitude)

    return [north_coord, east_coord, south_coord]


def triangulate_pos(pos_list):
    """
    Triangulate the position of the user based on the positions of other users.
    :input pos_list: list of positions
    :return: the center of the triangulation
    :rtype: tuple of (latitude, longitude)
    """
    
    coords_list = []
    distance_list = []

    # create coords and distance list
    for pos in pos_list:
        coords_list.append(pos['cord'])
        distance_list.append(pos['distance'])

    # Calculate the center using weighted average based on distances
    total_weight = sum(distance_list)
    weighted_coordinates = [(lat * w / total_weight, lon * w / total_weight) for (lat, lon), w in zip(coords_list, distance_list)]
    center = (sum(lat for lat, _ in weighted_coordinates), sum(lon for _, lon in weighted_coordinates))

    return center
