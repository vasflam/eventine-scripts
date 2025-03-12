import sys
from System.Collections.Generic import List
from System import Int32

loot_list = [
    0x2556,  # Metal Detector
    0x099F,  # A Message in a bottle
    0x0DCA,  # Fishing net
    0x14EC,  # Treasure map
    0x1EA7,  # Nautical gem
    0x0DF9,  # Event cotton
    0x1BDA,  # Event Toy wood
    0x0EEF,  # Event Lepro gold
    0x1EBA,  # Evet toolkit
    0x1763,  # Event velvet
    0x0FA0,  # Event silk thread
    # 0x09F1, # Ribs
    0x0eed,  # Gold
    0x3198,  # Big diamand
    0x1079,  # Hides
    # 0xEB49, # Dragon Ribs
    0x26B4,  # Dragon Scales
    0x4077,  # Dragon Blood
    0x0F80,  # Demon bone
]

skinning_corpses = [
    "cow",
    "deer",
    "bull",
    "dragon",
    "drake",
    "wyrm",
    "daemon",
]

corpse_id = 0x2006
hides_id = 0x1079
scales_id = 0x26B4
scissors_id = 0x0F9F
leather_id = 0x1081
skinning_knife_id = 0x0EC4
key_gump_id = 0x6abce12
resource_key_id = 0x176B
tailor_key_color = 0x0044

def find_corpses():
    f = Items.Filter()
    f.Enabled = True
    f.RangeMax = 2
    f.IsCorpse = True
    f.CheckIgnoreObject = True
    return Items.ApplyFilter(f)

def get_knife()
    for i in Items.FindBySerial(Player.Backpack.Serial).Contains:
        if i.ItemID in blade_ids:
            return item.Serial

def cut_corpse(serial):
    bladed = get_blade()
    if bladed:
        Items.UseItem(bladed)
        Target.WaitForTarget(6000, True)
        Target.Execute(serial)
        Misc.Pause(200)
