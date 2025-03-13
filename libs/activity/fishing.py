import time

from bigfish.libs import Observable
from bigfish.libs.uo.journal import in_journal
from bigfish.libs.uo.objects import unmount, use_fishing_pole, cut_raw_fish, move_all_by_type, \
    kill_nearest_enemy, pull_corpses_with_net, loot_corpses
from bigfish.libs.uo.types import FISH_STEAK, FISHING_NET, GOLD, TREASURE_MAP, BOTTLE

CATCH_MESSAGES = [
    "You fish a while",
    "an item along with a monster",
    "pull out",
    "something odd",
    "do not have room"
]
STOP_MESSAGES = [
    "biting here",
    "heavy chest",
    "heavy crate",
    "heavy box",
]

class FishingSettings:
    def __init__(self):
        self.cut_raw_fish = True
        self.steaks_container = Player.Backpack.Serial
        self.attack_enemies = True
        self.weapon = None
        self.discord_target = False
        self.loot_corpses = True
        self.loot_container = None
        self.names_loot_table = []
        self.graphics_loot_table = [
            FISHING_NET,
            GOLD,
            TREASURE_MAP,
            BOTTLE,
        ]

class Fishing(Observable):
    STATUS_STOPPED = 0
    STATE_RUNNING = 1
    STATUS_STOPPING = 2

    def __init__(self, settings: FishingSettings = None):
        super().__init__()
        self.status = Fishing.STATUS_STOPPED
        self.settings = settings if settings else FishingSettings()

    def is_stopping(self):
        return self.status == Fishing.STATUS_STOPPING

    def is_running(self):
        return self.status == Fishing.STATE_RUNNING

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
        self.status = Fishing.STATE_RUNNING
        try:
            self.notify()
            while True and not self.is_stopping():
                unmount()
                result = self.fishing()

                if self.settings.attack_enemies:
                    # Attack and loot enemies here
                    kill_nearest_enemy(weapon=self.settings.weapon, discord_target=self.settings.discord_target)
                    pull_corpses_with_net()
                    print("pulled")
                    loot_corpses(names_loot_table=self.settings.names_loot_table, graphics_loot_table=self.settings.graphics_loot_table, container=self.settings.loot_container)
                    print("looted")

                if self.settings.cut_raw_fish:
                    print(time.time(), "cutting fish")
                    cut_raw_fish()
                    print(time.time(), "cutted fish")

                if self.settings.steaks_container:
                    print(time.time(), "move steaks")
                    move_all_by_type(FISH_STEAK, self.settings.steaks_container)
                    print(time.time(), "moved steaks")

                if not result:
                    print(time.time(), "no fish here")
                    return
                Misc.Pause(100)
        finally:
            self.status = self.STATUS_STOPPED
            self.notify()

    def stop(self):
        self.status = self.STATUS_STOPPING
