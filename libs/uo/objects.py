import time

from bigfish.libs.uo.map import get_facet_name, get_facet_id
from bigfish.libs.uo.search import find_in_backpack, find_in_container, find_enemy, find_corpses, find_on_layers
from bigfish.libs.uo.layers import LEFT_HAND, WEAPONS, RIGHT_HAND
from bigfish.libs.uo.types import BLADED_ITEMS, RAW_FISH, LARGE_FISHING_NET, FISHING_POLE, MUSICAL_INSTRUMENTS, \
    TREASURE_MAP, SHOVEL


def get_first(lst):
    return lst[0] if isinstance(lst, list) and len(lst) > 0 else None

def equip_item(serial):
    item = Items.FindBySerial(serial)

    if item:
        layer = item.Layer
        equipped_in_layer = Player.GetItemOnLayer(layer)
        # Already equipped
        if equipped_in_layer and equipped_in_layer.Serial == serial:
            return True

        if layer in WEAPONS:
            left_equipped = Player.GetItemOnLayer(LEFT_HAND)
            right_equipped = Player.GetItemOnLayer(RIGHT_HAND)
            if item.IsTwoHanded:
                if left_equipped:
                    Player.UnEquipItemByLayer(LEFT_HAND, 2000)
                    Misc.Pause(650)
                if right_equipped:
                    Player.UnEquipItemByLayer(RIGHT_HAND, 2000)
                    Misc.Pause(650)
        else:
            Player.UnequipItemByLayer(layer, 2000)
            Misc.Pause(650)

        Player.EquipItem(serial)
        Misc.Pause(650)
        return True
    return False

def equip_item_by_type(graphics):
    equipped_type = find_on_layers(graphics)
    if equipped_type:
        return equipped_type

    serial = get_first(find_in_backpack(graphics))
    if serial:
        equip_item(serial)
        return serial
    else:
        return None

def unmount():
    if Player.Mount:
        Mobiles.UseMobile(Player.Serial)

def cut_raw_fish():
    bladed = get_first(find_in_backpack(BLADED_ITEMS))
    if bladed:
        raw_fish = find_in_backpack(RAW_FISH)
        for fish in raw_fish:
            Items.UseItem(bladed)
            Target.WaitForTarget(6000, True)
            Target.TargetExecute(fish)
            Misc.Pause(650)

def use_large_fishing_net(target, target_timeout = 6000):
    net = get_first(find_in_backpack(LARGE_FISHING_NET))
    if net:
        Items.UseItem(net)
        Target.WaitForTarget(target_timeout)
        Target.TargetExecute(target)
        return True
    return False

def use_fishing_pole(offset = 0):
    pole = equip_item_by_type(FISHING_POLE)
    Items.UseItem(pole)
    Target.WaitForTarget(6000, True)
    Target.TargetExecuteRelative(Player.Serial, offset)

def move_all_by_type(graphics, source = None, target ="ground"):
    graphics = graphics if isinstance(graphics, list) else [graphics]

    if source is None:
        source = Player.Backpack.Serial

    for item in find_in_container(graphics, source):
        if target == "ground":
            Items.MoveOnGround(item, 99999, Player.Position.X, Player.Position.Y, Player.Position.Z)
        else:
            Items.Move(item, target, 99999)
        Misc.Pause(650)

def use_discordance(serial):
    Journal.Clear("must wait")
    Player.UseSkill("Discordance")

    Misc.Pause(100)
    if Journal.Search("must wait"):
        return

    Target.WaitForTarget(6000, True)
    if Journal.Search("What instrument"):
        instrument = get_first(find_in_backpack(MUSICAL_INSTRUMENTS))
        if instrument:
            Target.TargetExecute(instrument)
            Target.WaitForTarget(6000, True)
        else:
            Target.Cancel()
            return
    Target.TargetExecute(serial)


def kill_nearest_enemy(max_range = 10, weapon = None, discord_target = False, kill_timeout = 60000):
    nearest = find_enemy(max_range=max_range)
    while True:
        if nearest:
            if weapon:
                equip_item(weapon)

            Player.Attack(nearest)
            Misc.Pause(50)

            if discord_target:
                use_discordance(nearest)

            while True:
                mobile = Mobiles.FindBySerial(nearest)
                if not mobile:
                    return
        else:
            return

def loot_corpses(max_range = 2, names_loot_table = None, graphics_loot_table = None, container = None, ignore_objects = True):
    container = Player.Backpack.Serial if container is None else container
    corpses = find_corpses(max_range, ignore_objects)

    for corpse in corpses:
        corpse_item = Items.FindBySerial(corpse)
        Items.WaitForContents(corpse_item, 6000)
        Misc.Pause(400)
        for item in Items.FindBySerial(corpse).Contains:
            if names_loot_table:
                for name in names_loot_table:
                    if name in item.Name:
                        Items.Move(item, container, 2000)
                        Misc.Pause(650)
            if graphics_loot_table:
                for graphics in graphics_loot_table:
                    if graphics == item.ItemID:
                        Items.Move(item, container, 2000)
                        Misc.Pause(650)
        Misc.IgnoreObject(corpse)

def pull_corpses_with_net(max_range = 10, ignore_objects = True):
    for corpse in find_corpses(max_range, ignore_objects):
        use_large_fishing_net(corpse)
        Misc.Pause(250)
    Misc.Pause(400)

def get_location_from_tmap(serial):
    map_item = Items.FindBySerial(serial)
    if map_item:
        if map_item.ItemID != TREASURE_MAP:
            return
        Items.WaitForProps(serial, 6000)
        loc = Items.GetPropValueString(serial, "Location")
        strings = Items.GetPropStringList(serial)
        facet_name = strings[2].replace("for somewhere in ", "")
        name = strings[0].replace("drawn treasure map", "")
        facet_id = get_facet_id(facet_name)
        completed = is_tmap_completed(serial)
        if loc and loc != "":
            lat, lon = [int(l.strip()) for l in loc.replace("(", "").replace(")", "").split(",")]
            return lat, lon, name, facet_id, completed

def is_tmap_completed(serial):
    item = Items.FindBySerial(serial)
    if item:
        Items.WaitForProps(serial, 6000)
        for l in Items.GetPropStringList(serial):
            if "Completed" in l:
                return True
    return False

def get_location_from_tmaps(container = None, recursive = True):
    container = Player.Backpack.Serial if container is None else container
    maps = find_in_container(TREASURE_MAP, container=container, recursive=recursive)
    locations = []
    for map in maps:
        loc = get_location_from_tmap(map)
        if loc:
            locations.append(loc)
    return locations

def find_tmap_by_location(point, container = None):
    container = Player.Backpack.Serial if container is None else container
    maps = find_in_container(TREASURE_MAP, container=container)
    for map in maps:
        loc = get_location_from_tmap(map)
        if loc:
            x, y, *rest = loc
            if (x, y) == point:
                return map

def dig_treasure_map(serial):
    shovel = get_first(find_in_backpack(SHOVEL))
    if not shovel:
        return False
    Items.UseItem(shovel)
    Target.WaitForTarget(6000)
    Target.TargetExecute(serial)
    Target.WaitForTarget(6000)
    Target.TargetExecuteRelative(Player.Serial, 0)
    return True

def head_message(text, color = 80):
    Player.HeadMessage(color, text)