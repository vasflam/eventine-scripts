import math

class SextantCoordinates:
    DEGREE_SYMBOL = "°"
    MAP = (5120, 4096)  # x, y
    MAP_CENTER = (1323, 1624)  # x, y

    def __init__(self, lat, lon):
        self.latStr = lat
        self.lonStr = lon
        self.lat = self.parse_coordinate(lat)
        self.lon = self.parse_coordinate(lon)

    def parse_coordinate(self, text):
        parts = text.replace("°", " ").replace("'", " ").split(" ")
        degree = (int(parts[0]) + int(parts[1]) / 60)
        if parts[2] in ["S", "W"]:
            degree *= -1
        return degree

    def to_tile(self):
        center_x, center_y = SextantCoordinates.MAP_CENTER
        map_x, map_y = SextantCoordinates.MAP
        x = round((self.lon * map_x / 360) + map_x + center_x)
        if x > map_x:
            x -= map_x

        y = round((self.lat * map_y / 360) - center_y - map_y)
        if abs(y) > map_y:
            y = abs(y) - map_y

        return {"x": round(abs(x)), "y": round(abs(y))}

    @staticmethod
    def from_string(s):
        if "X:" in s:
            x, y = s.replace("X: ", "").replace("Y: ", "").replace("- ", "").split(" ")
            return SextantCoordinates.from_tile(int(x), int(y))
        lat, lon = [part.strip() for part in s.split(',')]
        return SextantCoordinates(lat, lon)

    @staticmethod
    def get_direction(x, y):
        if 1323 <= x <= 3883:
            lon_direction = "E"
        elif x < 1323:
            lon_direction = "W"
        else:
            lon_direction = "W"

        if 1624 <= y <= 3672:
            lat_direction = "S"
        elif y < 1264:
            lat_direction = "N"
        else:
            lat_direction = "N"

        return lat_direction, lon_direction


    @staticmethod
    def from_tile(x, y):
        # d = (t - C) * 360 / N
        lon = (x - SextantCoordinates.MAP_CENTER[0]) * 360 / SextantCoordinates.MAP[0]
        lat = (y - SextantCoordinates.MAP_CENTER[1]) * 360 / SextantCoordinates.MAP[1]

        if lon > 180:
            # Right part of West, from 3883 to 4090 on map
            lon = 360 - lon

        if lat > 180:
            lat = 360 - lat

        lat_direction, lon_direction = SextantCoordinates.get_direction(x, y)

        def convert(value):
            degrees = int(value)
            if (value - degrees) * 60 < 0:
                minutes = int(abs(value - degrees) * 60)
            else:
                minutes = int(abs(value - degrees) * 60)
            return "{}°{}'".format(abs(degrees), minutes)

        lat_str = convert(lat) + lat_direction
        lon_str = convert(lon) + lon_direction
        return SextantCoordinates(lat_str, lon_str)

    def __str__(self):
        return "{}, {}".format(self.latStr, self.lonStr)

    def __eq__(self, other):
        if isinstance(other, SextantCoordinates):
            return self.lat == other.lat and self.lon == other.lon
        return NotImplemented