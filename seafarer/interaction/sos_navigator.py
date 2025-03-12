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

    def __init__(self, caller_script, markers_file = None, refresh_interval = 300):
        self.markers_file = markers_file
        self.refresh_interval = refresh_interval
        self.selected_book = None
        self.markers = Markers(markers_file)
        self.fishing_spot = FishingSpot()
        self.fishing_thread = None
        self.update_events = []
        self.caller_script = caller_script

    def get_gump_data(self):
        return Gumps.GetGumpData(self.GUMP_ID)

    def select_book(self):
        self.selected_book = Target.PromptTarget("Select SOS book")

    def is_within_range(self, x1, y1, x2, y2, max_range = 2):
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance <= max_range

    def refresh_markers(self):
        if self.selected_book:
            Player.HeadMessage(80, "Refreshing markers...")
            book = SOSBook(self.selected_book)
            entries = book.get_content()
            markers = []
            for entry in entries:
                sos = entry[0]
                tile = sos.to_tile()
                color = "white" if entry[1] else "yellow"
                markers.append("{},{},{},SOS {}:{},,{},0".format(tile['x'], tile['y'], Player.Map, sos.latStr, sos.lonStr, color))
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
            for entry in entries:
                sos = entry[0]
                tile = sos.to_tile()
                if self.is_within_range(Player.Position.X, Player.Position.Y, tile['x'], tile['y']):
                    book.get_content(with_remove=sos)
                    return True
            return False
        else:
            Player.HeadMessage(80, "Please set SOS book first")

    def fishing(self):
        if self.fishing_spot.state == FishingSpot.STATE_STOPPING:
            self.update_events.append(1)
            return
        elif self.fishing_spot.state == FishingSpot.STATE_STARTED:
            self.fishing_spot.stop()
            self.update_events.append(1)
            return

        if self.get_scroll_from_book():
            Player.HeadMessage(80, "Got SOS scroll from book")
        else:
            Player.HeadMessage(80, "Fishing without SOS scroll")

        self.fishing_thread = Thread(target=self.fishing_spot.start)
        self.fishing_thread.start()
        Misc.Pause(200)
        self.update_events.append(1)

    def handle_controls(self):
        gd = self.get_gump_data()
        if gd.hasResponse:
            if Player.IsGhost:
                Player.HeadMessage(80, "Ghost can't use items")
                return
            button = gd.buttonid
            if button == self.BUTTON_REFRESH_MARKERS:
                self.refresh_markers()
                self.update_events.append(1)
            elif button == self.BUTTON_FISHING:
                self.fishing()
            elif button == self.BUTTON_SET_BOOK:
                self.select_book()
                self.update_events.append(1)
            else:
                Misc.SendMessage("Unknown button")

        if len(self.update_events) > 0:
            self.show_gump()
            self.update_events = []

    def monitor_threads(self):
        prev_fishing_state = self.fishing_spot.state
        while True and Misc.ScriptStatus(self.caller_script):
            state = self.fishing_spot.state
            if state != prev_fishing_state:
                self.update_events.append(1)
                prev_fishing_state = state
            Misc.Pause(500)
        self.fishing_spot.stop()

    def start(self):
        monitor_thread = Thread(target=self.monitor_threads)
        monitor_thread.start()
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
        if self.fishing_spot.state == FishingSpot.STATE_STARTED:
            if self.fishing_spot.state == FishingSpot.STATE_STOPPING:
                Gumps.AddLabel(gump, startX + 30, startY + 28, 80, "Stopping...")
            else:
                Gumps.AddLabel(gump, startX + 30, startY + 28, 80, "Stop Fishing")
        else:
            Gumps.AddLabel(gump, startX + 30, startY + 28, 80, "Start Fishing")

        Gumps.AddButton(gump, startX + 10, startY + 55, 40019, 40029, self.BUTTON_REFRESH_MARKERS, 1, 1)
        Gumps.AddLabel(gump, startX + 30, startY + 58, 80, "Refresh Markers")

        Gumps.AddButton(gump, startX + 10, startY + 85, 40019, 40029, self.BUTTON_SET_BOOK, 1, 1)
        Gumps.AddLabel(gump, startX + 30, startY + 88, 80, "Select book " + ("(*)" if self.selected_book else ""))
        if Gumps.HasGump(self.GUMP_ID):
            gd = self.get_gump_data()
            gump = gd
        Gumps.SendGump(gump.gumpId, Player.Serial, gump.x, gump.y, gump.gumpDefinition, gump.gumpStrings)
