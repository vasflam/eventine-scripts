def in_journal(lines):
    for line in lines:
        if Journal.Search(line):
            return True
    return False