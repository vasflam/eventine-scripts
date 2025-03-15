import os.path
import CUO

from bigfish.libs.uo.map import is_within_range, FARAAN
from bigfish.libs.uo.markers import create_marker
from bigfish.libs.uo.objects import get_location_from_tmaps, find_tmap_by_location, dig_treasure_map, head_message, \
    is_tmap_completed
from bigfish.seafarer.common.markers import Markers
markers_dir = r'D:\Games\UO Eventine\Eventine Setup\Custom ClassicUO\Data\Client'
markers = Markers(markers_path=os.path.join(markers_dir, "tmaps.csv"))
locations = get_location_from_tmaps(Player.Backpack.Serial, recursive=True)
markers_list = []
for loc in locations:
    x, y, name, facet, completed = loc
    if completed:
        continue
    if is_within_range((Player.Position.X, Player.Position.Y), (x, y), 10):
        tmap = find_tmap_by_location((x, y))
        head_message("Found treasure map, dig it ({})".format(hex(tmap)))
        if tmap:
            tmap_item = Items.FindBySerial(tmap)
            if not dig_treasure_map(tmap):
                head_message("No shovel in backpack")
            Misc.Pause(650)
    color = "white"
    if facet == FARAAN:
        color = "black"
    marker = create_marker(x, y, name, facet=facet, color=color)
    markers_list.append(marker)
markers.write(markers_list)
CUO.LoadMarkers()