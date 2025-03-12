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

    STATE_STOPPED = 0
    STATE_STARTED = 1
    STATE_STOPPING = 2

    def __init__(self):
        self.started = False
        self.stopping = False
        self.state = self.STATE_STOPPED

    def find_pole(self):
        return Items.FindByID(self.POLE_ID, -1, Player.Backpack.Serial, True, False)

    def equip_pole(self):
        r_hand = Player.GetItemOnLayer('RightHand')
        if r_hand is None or r_hand.ItemID != self.POLE_ID:
            if r_hand:
                Player.UnEquipItemByLayer('RightHand', 3500)
                Misc.Pause(100)
            pole = self.find_pole()
            if pole:
                Player.EquipItem(pole)
                Misc.Pause(650)
                return pole
        else:
            return r_hand

    def in_journal(self, lines = []):
        for line in lines:
            if Journal.Search(line):
                return True

    def start(self):
        self.state = self.STATE_STARTED
        try:
            if Player.Mount:
                Player.HeadMessage(80, "Unmounting")
                Mobiles.UseMobile(Player.Serial)
                Misc.Pause(650)

            while True and self.state != self.STATE_STOPPING:
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
                    Misc.Pause(650)
                Misc.Pause(100)
        finally:
            self.state = self.STATE_STOPPED

    def stop(self):
        self.state = self.STATE_STOPPING