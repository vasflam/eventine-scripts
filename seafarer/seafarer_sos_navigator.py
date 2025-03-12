from bigfish.seafarer.interaction.sos_navigator import SOSNavigator

markers_file = r'D:\Games\UO Eventine\Eventine Setup\Custom ClassicUO\Data\Client\sos.csv'
navigator = SOSNavigator(markers_file)
navigator.start()