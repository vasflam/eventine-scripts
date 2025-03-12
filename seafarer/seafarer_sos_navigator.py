import os
from bigfish.seafarer.interaction.sos_navigator import SOSNavigator

markers_dir = r'D:\Games\UO Eventine\Eventine Setup\Custom ClassicUO\Data\Client'
markers_file = os.path.join(markers_dir, "sos.csv")
navigator = SOSNavigator(markers_file)
navigator.start()