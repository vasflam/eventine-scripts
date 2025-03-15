from bigfish.libs import SettingsAware
from bigfish.seafarer.common.sextant_coordinate import SextantCoordinates

class SextantSettings(SettingsAware):
    def __init__(self):
        self.a = 1

class SextantGump:
    GUMP_ID = 100011
    def __init__(self, refresh_interval:int = 100):
        self.refresh_interval = refresh_interval
        self.gump_last_x = 50
        self.gump_last_y = 50

    def start(self):
        last_point = None
        while True:
            point = SextantCoordinates.from_tile(Player.Position.X, Player.Position.Y)
            if point != last_point or last_point is None:
                last_point = point
                self.show_gump(point)
            Misc.Pause(self.refresh_interval)

    def show_gump(self, point):
        gump = Gumps.CreateGump(True, True, True, True)
        gump.x = self.gump_last_x
        gump.y = self.gump_last_y
        gump.gumpId = self.GUMP_ID
        startX = 0
        startY = 0

        html = ""
        Gumps.AddHtml(gump, startX, startY, 145, 63, html, True, False)
        Gumps.AddLabel(gump, startX + 43, startY + 5, 0, "Sextant")
        Gumps.AddLabel(gump, startX + 20, startY + 30, 80, "{}, {}".format(point.latStr, point.lonStr))

        if Gumps.HasGump(self.GUMP_ID):
            gd = Gumps.GetGumpData(self.GUMP_ID)
            self.gump_last_x = gd.x
            self.gump_last_y = gd.y
            gump.x = gd.x
            gump.y = gd.y
        Gumps.SendGump(gump, self.gump_last_x, self.gump_last_y)
