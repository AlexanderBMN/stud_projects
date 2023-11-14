from geopy import distance


def lat_lon_cmp(ref_lat, ref_lon, lat, lon):
    # lat und lon werden in  10th of Micro-Degree geliefert
    ref_lon = int(ref_lon)/10000000
    ref_lat = int(ref_lat)/10000000
    return distance.distance((ref_lat, ref_lon), (lat, lon)).m
