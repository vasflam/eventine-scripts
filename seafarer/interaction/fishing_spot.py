class FishingSpot:
    POLE_ID = 0x0DC0
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
    ]

    def __init__(self):
        self.started = False
        self.stopping = False

    def find_pole(self):
        return Items.FindByID(self.POLE_ID, -1, Player.Backpack.Serial, True, False)

    def equip_pole(self):
        rHand = Player.GetItemOnLayer('RightHand')
        if rHand.ItemID != self.POLE_ID:
            Player.UnEquipItemByLayer('RightHand', 3500)
            pole = self.find_pole()
            if pole:
                Player.EquipItem(pole)
                Misc.Pause(650)
                return pole
        else:
            return rHand

    def in_journal(self, lines = []):
        for line in lines:
            if Journal.Search(line):
                return True

    def start(self):
        self.started = True
        print("started")
        try:
            if Player.Mount:
                Items.UseItem(Player.Serial)
                Misc.Pause(650)

            print(self.started)
            while True and self.started:
                Journal.Clear()
                pole = self.equip_pole()
                if not pole:
                    Player.HeadMessage(80, "I don't have fishing pole")
                    return
                Items.UseItem(pole)
                Target.WaitForTarget(3000)
                Target.TargetExecuteRelative(Player.Serial, 0)
                Timer.Create("fishing", 12000)
                Misc.Pause(650)
                while True and Timer.Check("fishing"):
                    if self.in_journal(self.STOP_MESSAGES):
                        return
                    if self.in_journal(self.CATCH_MESSAGES):
                        break
                    Misc.Pause(750)
        finally:
            self.started = False

    def stop(self):
        self.started = False