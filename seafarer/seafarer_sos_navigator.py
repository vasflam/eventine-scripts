import os

from bigfish.seafarer.interaction.sos_navigator import SOSNavigator

from bigfish.settings import fishing_settings, sos_navigator_settings

sos_navigator_settings.fishing_settings = fishing_settings
navigator = SOSNavigator(__file__, settings=sos_navigator_settings)
navigator.start()