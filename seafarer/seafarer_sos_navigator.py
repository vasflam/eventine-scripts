import os

from bigfish.seafarer.interaction.sos_navigator import SOSNavigator, SOSNavigatorSettings


settings = SOSNavigatorSettings.load()
navigator = SOSNavigator(__file__, settings=settings)
navigator.start()