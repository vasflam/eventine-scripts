from System.Collections.Generic import List
from System import Int32
import math

NORTH = "North"
EAST = "East"
SOUTH = "South"
WEST = "West"
BUTTON_UP = 1
BUTTON_RIGHT_UP = 2
BUTTON_RIGHT = 3
BUTTON_RIGHT_DOWN = 4
BUTTON_DOWN = 5
BUTTON_LEFT_DOWN = 6
BUTTON_LEFT = 7
BUTTON_LEFT_UP = 8
BUTTON_TURN_LEFT = 9
BUTTON_TURN_RIGHT = 10
BUTTON_STOP = 11
BUTTON_CLEAN = 12

unknown_ship_commands = {
    BUTTON_UP: 'Forward',
    BUTTON_RIGHT_UP: 'Forward Right',
    BUTTON_RIGHT: 'Right',
    BUTTON_RIGHT_DOWN: 'Back Right',
    BUTTON_DOWN: 'Back',
    BUTTON_LEFT_DOWN: 'Back Left',
    BUTTON_LEFT: 'Left',
    BUTTON_LEFT_UP: 'Forward Left',
}

# UP button acts as forward/back/left/right
direction_commands_1 = {
    NORTH: {
        BUTTON_UP: 'Forward',
        BUTTON_RIGHT_UP: 'Forward Right',
        BUTTON_RIGHT: 'Right',
        BUTTON_RIGHT_DOWN: 'Back Right',
        BUTTON_DOWN: 'Back',
        BUTTON_LEFT_DOWN: 'Back Left',
        BUTTON_LEFT: 'Left',
        BUTTON_LEFT_UP: 'Forward Left',
    },
    SOUTH: {
        BUTTON_UP: 'Back',
        BUTTON_RIGHT_UP: 'Back Left',
        BUTTON_RIGHT: 'Left',
        BUTTON_RIGHT_DOWN: 'Forward Left',
        BUTTON_DOWN: 'Forward',
        BUTTON_LEFT_DOWN: 'Forward Right',
        BUTTON_LEFT: 'Right',
        BUTTON_LEFT_UP: 'Back Right',
    },
    WEST: {
        BUTTON_UP: 'Right',
        BUTTON_RIGHT_UP: 'Back Right',
        BUTTON_RIGHT: 'Back',
        BUTTON_RIGHT_DOWN: 'Back Left',
        BUTTON_DOWN: 'Left',
        BUTTON_LEFT_DOWN: 'Forward Left',
        BUTTON_LEFT: 'Forward',
        BUTTON_LEFT_UP: 'Forward Right',
    },
    EAST: {
        BUTTON_UP: 'Left',
        BUTTON_RIGHT_UP: 'Forward Left',
        BUTTON_RIGHT: 'Forward',
        BUTTON_RIGHT_DOWN: 'Forward Right',
        BUTTON_DOWN: 'Right',
        BUTTON_LEFT_DOWN: 'Back Right',
        BUTTON_LEFT: 'Back',
        BUTTON_LEFT_UP: 'Back Left',
    },
}

# diagonal arrows acts as forward/back/left/right
direction_commands_2 = {
    NORTH: {
        BUTTON_UP: 'Forward Left',
        BUTTON_RIGHT_UP: 'Forward',
        BUTTON_RIGHT: 'Forward Right',
        BUTTON_RIGHT_DOWN: 'Right',
        BUTTON_DOWN: 'Back Right',
        BUTTON_LEFT_DOWN: 'Back',
        BUTTON_LEFT: 'Back Left',
        BUTTON_LEFT_UP: 'Left',
    },
    SOUTH: {
        BUTTON_UP: 'Back Right',
        BUTTON_RIGHT_UP: 'Back',
        BUTTON_RIGHT: 'Back Left',
        BUTTON_RIGHT_DOWN: 'Left',
        BUTTON_DOWN: 'Forward Left',
        BUTTON_LEFT_DOWN: 'Forward',
        BUTTON_LEFT: 'Forward Right',
        BUTTON_LEFT_UP: 'Right',
    },
    WEST: {
        BUTTON_UP: 'Forward Right',
        BUTTON_RIGHT_UP: 'Right',
        BUTTON_RIGHT: 'Back Right',
        BUTTON_RIGHT_DOWN: 'Back',
        BUTTON_DOWN: 'Back Left',
        BUTTON_LEFT_DOWN: 'Left',
        BUTTON_LEFT: 'Forward Left',
        BUTTON_LEFT_UP: 'Forward',
    },
    EAST: {
        BUTTON_UP: 'Back Left',
        BUTTON_RIGHT_UP: 'Left',
        BUTTON_RIGHT: 'Forward Left',
        BUTTON_RIGHT_DOWN: 'Forward',
        BUTTON_DOWN: 'Forward Right',
        BUTTON_LEFT_DOWN: 'Right',
        BUTTON_LEFT: 'Back Right',
        BUTTON_LEFT_UP: 'Back',
    },
}

other_commands = {
    BUTTON_TURN_LEFT: 'Turn Left',
    BUTTON_TURN_RIGHT: 'Turn Right',
    BUTTON_STOP: 'Stop',
    BUTTON_CLEAN: '[Clean',
}


class BoatControl:
    GUMP_ID = 100010
    def __init__(self, refresh_interval:int = 100):
        self.refresh_interval = refresh_interval

    def find_object_position(self, name):
        f = Items.Filter()
        f.Enabled = True
        f.RangeMax = 16
        items = Items.ApplyFilter(f)
        result = []
        for item in items:
            if name in item.Name:
                result.append(item)
        if len(result) > 0:
            return min(result,
                       key=lambda box: abs(box.Position.X - Player.Position.X) + abs(
                           box.Position.Y - Player.Position.Y))
        return None

    def get_cargo_hold(self):
        return self.find_object_position("cargo hold")

    def get_hatch(self):
        return self.find_object_position("hatch")

    def get_direction_relative_to(self, object, behindPlayer=True):
        x = Player.Position.X
        y = Player.Position.Y
        if not object:
            return None
        tx = object.Position.X
        ty = object.Position.Y
        if abs(tx - x) > abs(ty - y):
            return (WEST if tx > x else EAST) if behindPlayer else (WEST if tx < x else EAST)
        else:
            return (NORTH if ty > y else SOUTH) if behindPlayer else (NORTH if ty < y else SOUTH)

    def get_boat_direction(self):
        cargo_hold = self.get_cargo_hold()
        hatch = self.get_hatch()
        if cargo_hold:
            return self.get_direction_relative_to(cargo_hold)
        elif hatch:
            return self.get_direction_relative_to(hatch, False)
        else:
            return None

    def handle_navigation_controls(self, button_id):
        direction = self.get_boat_direction()
        navigation_commands = unknown_ship_commands

        if direction:
            navigation_commands = direction_commands_2[direction]

        command = "Unknown button with id {}".format(button_id)
        if button_id in navigation_commands:
            command = navigation_commands[button_id]
        elif button_id in other_commands:
            command = other_commands[button_id]
        else:
            Player.HeadMessage(88, command)
            return
        Player.ChatSay(80, command)

    def get_player_coordinates(self):
        return Point.from_tile(Player.Position.X, Player.Position.Y)

    def start(self):
        gump = self.get_gump()
        Gumps.SendGump(gump.gumpId, Player.Serial, 100, 100, gump.gumpDefinition, gump.gumpStrings)
        Misc.Pause(300)
        # Gumps.WaitForGump(gump.gumpId, 10000)
        while True:
            gd = Gumps.GetGumpData(gump.gumpId)
            if gd and gd.hasResponse:
                button_id = gd.buttonid
                if button_id == 0:
                    return
                else:
                    self.handle_navigation_controls(button_id)
                gump = self.get_gump()
                Gumps.SendGump(gump.gumpId, Player.Serial, gump.x, gump.y, gump.gumpDefinition, gump.gumpStrings)
            Misc.Pause(self.refresh_interval)

    def get_gump(self):
        gump = Gumps.CreateGump(True, True, True, True)
        gump.gumpId = self.GUMP_ID
        startX = 300
        startY = 300

        html = ""
        Gumps.AddHtml(gump, startX, startY, 145, 260, html, True, False)
        Gumps.AddLabel(gump, startX + 43, startY + 5, 0, "Navigation")

        Gumps.AddButton(gump, startX + 50, startY + 30, 4500, 4500, BUTTON_UP, 1, 1)
        Gumps.AddButton(gump, startX + 90, startY + 30, 4501, 4501, BUTTON_RIGHT_UP, 1, 1)
        Gumps.AddButton(gump, startX + 90, startY + 80, 4502, 4502, BUTTON_RIGHT, 1, 1)
        Gumps.AddButton(gump, startX + 90, startY + 125, 4503, 4503, BUTTON_RIGHT_DOWN, 1, 1)
        Gumps.AddButton(gump, startX + 50, startY + 125, 4504, 4504, BUTTON_DOWN, 1, 1)
        Gumps.AddButton(gump, startX + 5, startY + 125, 4505, 4505, BUTTON_LEFT_DOWN, 1, 1)
        Gumps.AddButton(gump, startX + 5, startY + 80, 4506, 4506, BUTTON_LEFT, 1, 1)
        Gumps.AddButton(gump, startX + 5, startY + 30, 4507, 4507, BUTTON_LEFT_UP, 1, 1)

        Gumps.AddButton(gump, startX + 63, startY + 93, 40014, 40015, BUTTON_STOP, 1, 1)

        Gumps.AddButton(gump, startX + 5, startY + 170, 4506, 4506, BUTTON_TURN_LEFT, 1, 1)
        Gumps.AddButton(gump, startX + 90, startY + 170, 4502, 4502, BUTTON_TURN_RIGHT, 1, 1)

        Gumps.AddButton(gump, startX + 10, startY + 225, 40019, 40029, BUTTON_CLEAN, 1, 5)
        Gumps.AddLabel(gump, startX + 55, startY + 228, 80, "Clean")

        return gump