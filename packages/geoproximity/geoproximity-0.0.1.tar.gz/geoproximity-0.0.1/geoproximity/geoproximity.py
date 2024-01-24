from math import radians, sin, cos, sqrt, atan2

def haversine_distance(coord1, coord2):
    # Haversine formula for great-circle distance
    lat1, lon1 = map(radians, coord1)
    lat2, lon2 = map(radians, coord2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Radius of Earth in kilometers
    radius = 6371.0

    distance = radius * c
    return distance