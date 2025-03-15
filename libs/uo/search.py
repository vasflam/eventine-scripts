from System.Collections.Generic import List
from System import Int32
from System import Byte

from bigfish.libs.uo.layers import ALL_LAYERS
from bigfish.libs.uo.types import CORPSE


def create_item_filter(graphics = None, min_range = 0, max_range = 10, on_ground = None, is_corpse = None, is_container = None, is_movable = None, ignore_objects = True):
    graphics = graphics if isinstance(graphics, list) else [graphics]

    f = Items.Filter()
    f.Enabled = True
    if graphics:
        graphics = graphics if isinstance(graphics, list) else [graphics]
        f.Graphics = List[Int32](graphics)

    f.RangeMin = min_range
    f.RangeMax = max_range

    if on_ground is not None:
        f.OnGround = on_ground

    if is_corpse is not None:
        f.IsCorpse = is_corpse

    if is_container is not None:
        f.IsContainer = is_container

    if is_movable is not None:
        f.Movable = is_movable

    if ignore_objects is not None:
        f.CheckIgnoreObject = ignore_objects

    return f

def create_mobile_filter(graphics = None, notoriety = None, min_range:int = 0, max_range:int = 10, ignore_objects = True):
    f = Mobiles.Filter()
    f.Enabled = True
    if graphics:
        graphics = graphics if isinstance(graphics, list) else [graphics]
        f.Graphics = List[Int32]([graphics])

    if not notoriety:
        notoriety = [3, 4, 5, 6]

    f.Notorieties = List[Byte](bytes(notoriety))
    f.RangeMin = min_range
    f.RangeMax = max_range

    if ignore_objects is not None:
        f.CheckIgnoreObject = ignore_objects

    return f

def find_enemies(graphics = None, min_range:int = 0, max_range:int = 10, notoriety = None, ignore_objects = True):
    """
    Find enemies
    return Mobile[]
    """
    f = create_mobile_filter(graphics=graphics, min_range=min_range, max_range=max_range, notoriety=notoriety, ignore_objects=ignore_objects)
    return Mobiles.ApplyFilter(f)

def find_enemy(min_range:int = 0, max_range:int = 10, graphics = None, notoriety = None):
    """
    Find closest enemy

    return int
    """
    enemies = find_enemies(graphics, min_range=min_range, max_range=max_range, notoriety=notoriety)
    if len(enemies) > 0:
        closest = min(enemies, key=lambda enemy: abs(enemy.Position.X - Player.Position.X) + abs(enemy.Position.Y - Player.Position.Y))
        if closest:
            return closest.Serial

def find_in_container(graphics, color = -1, container = None, recursive = True, ignore_objects = True):
    container = Player.Backpack.Serial if container is None else container
    graphics = graphics if isinstance(graphics, list) else [graphics]

    container_item = Items.FindBySerial(container)
    if len(container_item.Contains) < 1:
        Items.WaitForContents(container, 6000)

    items = []
    for type_id in graphics:
        found = Items.FindAllByID(type_id, color, container, recursive, ignore_objects)
        if found:
            items += [f.Serial for f in found]
    return items

def find_in_backpack(graphics, recursive = True, ignore_objects = True):
    return find_in_container(graphics=graphics, recursive=recursive, ignore_objects=ignore_objects)

def find_on_ground(graphics, min_range = 0, max_range = 2, ignore_objects = True):
    graphics = graphics if isinstance(graphics, list) else [graphics]
    f = create_item_filter(graphics=graphics, min_range=min_range, max_range=max_range, ignore_objects=ignore_objects, on_ground=True)
    return [i.Serial for i in Items.ApplyFilter(f)]

def find_corpses(max_range = 10, ignore_objects = True):
    f = create_item_filter(graphics=CORPSE, max_range=max_range, ignore_objects=ignore_objects)
    return [i.Serial for i in Items.ApplyFilter(f)]

def find_on_layers(graphics):
    for layer in ALL_LAYERS:
        item = Player.GetItemOnLayer(layer)
        if item:
            if item.ItemID == graphics:
                return item.Serial

    return None