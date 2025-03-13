from bigfish.seafarer.common.sextant_coordinate import SextantCoordinates

def test_player_coords():
    p1 = SextantCoordinates.from_tile(Player.Position.X, Player.Position.Y)
    tile = p1.to_tile()
    p2 = SextantCoordinates(p1.latStr, p1.lonStr)
    if p1 != p2:
        print("test player coords error")

def test_coords(lat_deg, lat_min, lat_dir, lon_deg, lon_min, lon_dir):
    print("-----------------------------------------")
    lat = "{}°{}'{}".format(lat_deg, lat_min, lat_dir)
    lon = "{}°{}'{}".format(lon_deg, lon_min, lon_dir)
    print("----- P1:")
    p1 = SextantCoordinates(lat, lon)
    tile = p1.to_tile()
    print("----- P2:")
    p2 = SextantCoordinates.from_tile(tile['x'], tile['y'])
    print(p2, p2.to_tile())
    if p1 != p2:
        print(p1, p2)
        print("Player coords error")
    print("-----------------------------------------")

