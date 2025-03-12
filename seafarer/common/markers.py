class Markers:
    def __init__(self, markers_path = None):
        self.markers_path = markers_path

    def read(self):
        lines = []
        with open(self.markers_path, 'r') as source:
            for line in source:
                lines.append(line)
        return lines

    def write(self, lines):
        with open(self.markers_path, 'w') as dest:
            for line in lines:
                if not line.endswith("\n"):
                    line += "\n"
                dest.write(line)
