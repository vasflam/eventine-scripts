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
        degree = int(parts[0]) + int(parts[1]) / 60
        if parts[2] in ["S", "W"]:
            degree *= -1
        return degree

    def to_tile(self):
        center_x, center_y = SextantCoordinates.MAP_CENTER
        map_x, map_y = SextantCoordinates.MAP
        x = abs(round(self.lon * map_x / 360 + map_x + center_x))
        y = abs(round(self.lat * map_y / 360 + map_y + center_y))

        if x > map_x:
            x = x - map_x
        if y > map_y:
            y = y - map_y
        return {"x": x, "y": y}

    @staticmethod
    def from_string(s):
        if "X:" in s:
            x, y = s.replace("X: ", "").replace("Y: ", "").replace("- ", "").split(" ")
            return SextantCoordinates.from_tile(int(x), int(y))
        lat, lon = [part.strip() for part in s.split(',')]
        return SextantCoordinates(lat, lon)

    @staticmethod
    def from_tile(x, y):
        # d = (t - C) * 360 / N
        # when W - floor
        lon = (x - SextantCoordinates.MAP_CENTER[0]) * 360 / SextantCoordinates.MAP[0]
        lat = (y - SextantCoordinates.MAP_CENTER[1]) * 360 / SextantCoordinates.MAP[1]

        def normalize_degree(degree):
            if degree > 180:
                return degree - 360
            elif degree < -180:
                return -(360 + degree)
            else:
                return degree

        def convert(value, is_latitude):
            direction = ('Y' if value < 0 else 'S') if is_latitude else ('W' if value < 0 else 'E')

            degrees = int(value)
            minutes = abs(value - degrees) * 60
            if direction in ["W", "S"]:
                minutes = math.floor(minutes)
            else:
                minutes = round(minutes)
            return "{}°{}'{}".format(abs(degrees), minutes, direction)

        lat_str = convert(normalize_degree(lat), True)
        lon_str = convert(normalize_degree(lon), False)

        return SextantCoordinates(lat_str, lon_str)

    def __str__(self):
        return "{}, {}".format(self.latStr, self.lonStr)

    def __eq__(self, other):
        if isinstance(other, SextantCoordinates):
            return self.lat == other.lat and self.lon == other.lon
        return NotImplemented