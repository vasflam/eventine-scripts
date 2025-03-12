from threading import Thread

from bigfish.seafarer.interaction.sos_book import SOSBook
from bigfish.seafarer.common.markers import Markers
from bigfish.seafarer.interaction.fishing_spot import FishingSpot
import CUO
import math

class SOSNavigator:
    GUMP_ID = 100012
    BUTTON_REFRESH_MARKERS = 1
    BUTTON_FISHING = 2
    BUTTON_SET_BOOK = 3

    def __init__(self, markers_file = None, refresh_interval = 300):
        self.markers_file = markers_file
        self.refresh_interval = refresh_interval
        self.selected_book = None
        self.markers = Markers(markers_file)
        self.fishing_spot = FishingSpot()
        self.fishing_thread = None

    def get_gump_data(self):
        return Gumps.GetGumpData(self.GUMP_ID)

    def select_book(self):
        self.selected_book = Target.PromptTarget("Select SOS book")

    def is_within_range(self, x1, y1, x2, y2, max_range = 2):
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance <= max_range

    def refresh_markers(self):
        if self.selected_book:
            book = SOSBook(self.selected_book)
            entries = book.get_content()
            markers = []
            for sos in entries:
                tile = sos.to_tile()
                markers.append("{},{},{},SOS {}:{},,yellow,0".format(tile['x'], tile['y'], Player.Map, sos.latStr, sos.lonStr))
            self.markers.write(markers)
            Misc.Pause(300)
            CUO.LoadMarkers()
            Misc.SendMessage("Markers refreshed")
        else:
            Player.HeadMessage(80, "Please set SOS book first")

    def get_scroll_from_book(self):
        if self.selected_book:
            book = SOSBook(self.selected_book)
            entries = book.get_content()
            for sos in entries:
                tile = sos.to_tile()
                if self.is_within_range(Player.Position.X, Player.Position.Y, tile['x'], tile['y']):
                    book.get_content(with_remove=sos)
                    return True
            return False
        else:
            Player.HeadMessage(80, "Please set SOS book first")

    def fishing(self):
        if self.fishing_spot.started:
            self.fishing_spot.stop()
            return

        if self.get_scroll_from_book():
            self.fishing_thread = Thread(target=self.fishing_spot.start)
            self.fishing_thread.start()
            Misc.Pause(200)

    def handle_controls(self):
        gd = self.get_gump_data()
        if gd.hasResponse:
            if Player.IsGhost:
                Player.HeadMessage(80, "Ghost can't use items")
                return
            button = gd.buttonid
            if button == self.BUTTON_REFRESH_MARKERS:
                self.refresh_markers()
            elif button == self.BUTTON_FISHING:
                if self.fishing_thread:
                    print(self.fishing_thread.isAlive)
                print(self.fishing_spot.started)
                print(self.fishing_spot.stopping)
                self.fishing()
            elif button == self.BUTTON_SET_BOOK:
                self.select_book()
            else:
                Misc.SendMessage("Unknown button")
            self.show_gump()

        if not self.fishing_spot.started:
            self.show_gump()

    def start(self):
        self.show_gump()
        while True:
            self.handle_controls()
            Misc.Pause(self.refresh_interval)

    def show_gump(self):
        gump = Gumps.CreateGump(True, True, True, True)
        gump.gumpId = self.GUMP_ID
        startX = 300
        startY = 300

        html = ""
        Gumps.AddHtml(gump, startX, startY, 145, 120, html, True, False)
        Gumps.AddLabel(gump, startX + 43, startY + 5, 0, "SOS Navigator")

        Gumps.AddButton(gump, startX + 10, startY + 25, 40019, 40029, self.BUTTON_FISHING, 1, 1)
        if self.fishing_spot.started:
            Gumps.AddLabel(gump, startX + 30, startY + 28, 80, "Stop Fishing")
        else:
            Gumps.AddLabel(gump, startX + 30, startY + 28, 80, "Start Fishing")

        Gumps.AddButton(gump, startX + 10, startY + 55, 40019, 40029, self.BUTTON_REFRESH_MARKERS, 1, 1)
        Gumps.AddLabel(gump, startX + 30, startY + 58, 80, "Refresh Markers")

        Gumps.AddButton(gump, startX + 10, startY + 85, 40019, 40029, self.BUTTON_SET_BOOK, 1, 1)
        Gumps.AddLabel(gump, startX + 30, startY + 88, 80, "Select book " + ("(*)" if self.selected_book else ""))
        if Gumps.HasGump(self.GUMP_ID):
            gd = self.get_gump_data()
            print(gd)
            gump = gd
        Gumps.SendGump(gump.gumpId, Player.Serial, gump.x, gump.y, gump.gumpDefinition, gump.gumpStrings)
