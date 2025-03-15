import json
import time

from bigfish.libs import Observable, SettingsAware
from bigfish.libs import load_settings_from_json
from bigfish.libs.uo.journal import in_journal
from bigfish.libs.uo.objects import unmount, use_fishing_pole, cut_raw_fish, move_all_by_type, \
    kill_nearest_enemy, pull_corpses_with_net, loot_corpses
from bigfish.libs.uo.types import FISH_STEAK, FISHING_NET, GOLD, TREASURE_MAP, BOTTLE
import threading

CATCH_MESSAGES = [
    "You fish a while",
    "an item along with a monster",
    "pull out",
    "something odd",
    "do not have room",
    "You need to be closer",
]
STOP_MESSAGES = [
    "biting here",
    "heavy chest",
    "heavy crate",
    "heavy box",
]

class FishingSettings(SettingsAware):
    def __init__(self, **kwargs):
        super()
        self.cut_raw_fish: bool = True
        self.steaks_container = Player.Backpack.Serial
        self.attack_enemies = True
        self.weapon = None
        self.discord_target = False
        self.loot_corpses = True
        self.loot_container = None
        self.graphics_loot_table = [
            FISHING_NET, GOLD, TREASURE_MAP, BOTTLE
        ]
        self.names_loot_table = []

        for key, value in kwargs.items():
            setattr(self, key, value)

class Fishing(Observable):
    STATUS_STOPPED = 0
    STATE_RUNNING = 1
    STATUS_STOPPING = 2

    def __init__(self, settings: FishingSettings = None):
        super().__init__()
        self.status = Fishing.STATUS_STOPPED
        self.settings = settings if settings else FishingSettings()
        self.lock = threading.RLock()

    def is_stopping(self):
        with self.lock:
            return self.status == Fishing.STATUS_STOPPING

    def is_running(self):
        with self.lock:
            return self.status == Fishing.STATE_RUNNING

    def stop(self):
        with self.lock:
            self.status = self.STATUS_STOPPING
        self.notify()

    # one action, return False if there is no fish
    def fishing(self):
        Journal.Clear()
        use_fishing_pole()
        Timer.Create("fishing", 12000)
        Misc.Pause(650)
        while True and Timer.Check("fishing") and not self.is_stopping():
            if in_journal(STOP_MESSAGES):
                return False
            if in_journal(CATCH_MESSAGES):
                break
            Misc.Pause(300)
        return True

    def start(self):
        with self.lock:
            self.status = Fishing.STATE_RUNNING
        try:
            self.notify()
            Player.ChatSay("Stop")
            while True and not self.is_stopping():
                unmount()
                result = self.fishing()

                if self.settings.attack_enemies:
                    # Attack and loot enemies here
                    kill_nearest_enemy(weapon=self.settings.weapon, discord_target=self.settings.discord_target)
                    pull_corpses_with_net()
                    loot_corpses(names_loot_table=self.settings.names_loot_table, graphics_loot_table=self.settings.graphics_loot_table, container=self.settings.loot_container)

                if self.settings.cut_raw_fish:
                    cut_raw_fish()

                if self.settings.steaks_container:
                    move_all_by_type(FISH_STEAK, self.settings.steaks_container)

                if not result:
                    return
                Misc.Pause(100)
        finally:
            with self.lock:
                self.status = self.STATUS_STOPPED

            self.notify()
