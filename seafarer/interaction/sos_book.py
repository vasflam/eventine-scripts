from bigfish.seafarer.common.sextant_coordinate import SextantCoordinates

class BookEntry:
    def __init__(self, coordinates: SextantCoordinates, rarity = "Normal"):
        self.coordinates = coordinates
        self.rarity = rarity

    def __eq__(self, other):
        if isinstance(other, BookEntry):
            return self.coordinates == other.coordinates and self.rarity == other.rarity
        return NotImplemented

    def __str__(self):
        return str(self.coordinates)

class SOSBook:
    GUMP_ID = 0xf37bcaf2
    TYPE_ID = 0xAA70
    COLOR = 0x000b

    def __init__(self, book_serial, wait_timeout = 6000):
        self.wait_timeout = 6000
        self.book = Items.FindBySerial(book_serial)
        if not self.book:
            raise "Failed to find SOS book"

    def wait_for_gump(self):
        Gumps.WaitForGump(self.GUMP_ID, self.wait_timeout)

    def open(self):
        Items.UseItem(self.book)
        self.wait_for_gump()

    def get_content(self, with_remove: SextantCoordinates = None):
        content = []
        self.open()
        if Gumps.HasGump(self.GUMP_ID):
            while True:
                gd = Gumps.GetGumpData(self.GUMP_ID)
                text = gd.stringList[8:]
                page_content = self.parse_page(text)
                content += page_content

                if with_remove and with_remove in content:
                    button = (content.index(with_remove) * 2) + 10
                    Gumps.SendAction(self.GUMP_ID, button)
                    self.wait_for_gump()
                    Gumps.CloseGump(self.GUMP_ID)
                    break

                if self.has_next_page(gd):
                    Gumps.SendAction(self.GUMP_ID, 3)
                    self.wait_for_gump()
                else:
                    Gumps.CloseGump(self.GUMP_ID)
                    break
        return content

    def parse_page(self, text = []):
        book_entries = []
        def chunk_list(lst, chunk_size):
            return [lst[i:i+chunk_size] for i in range(0, len(lst), chunk_size)]
        chunks = chunk_list(text, 4)
        for entry in chunks:
            if None in entry:
                break
            coordinates = SextantCoordinates.from_string(entry[1])
            book_entries.append(BookEntry(coordinates, rarity=entry[0]))
        return book_entries

    def has_next_page(self, gump_data):
        for t in gump_data.gumpText:
            if t == "Next page":
                return True
        return False