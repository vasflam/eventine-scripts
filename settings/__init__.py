from bigfish.libs.activity.fishing import FishingSettings
from bigfish.seafarer.interaction.sos_navigator import SOSNavigatorSettings

# Fishing Settings
fishing_settings = FishingSettings()
fishing_settings.cut_raw_fish = True
fishing_settings.steaks_container = None # none - backpack, "ground", or container serial
fishing_settings.attack_enemies = True
fishing_settings.weapon = 0x4042296A # Set you bow serial
fishing_settings.discord_target = True
fishing_settings.loot_corpses = True
fishing_settings.loot_container = None # Loot to Backpack
#fishing_settings.graphics_loot_table = [] # Default set to maps, bottles, nets and gold
#fishing_settings.names_loot_table = [] # Default is empty

# SOS navigator settings
sos_navigator_settings = SOSNavigatorSettings()
sos_navigator_settings.markers_dir = r'D:\Games\UO Eventine\Eventine Setup\Custom ClassicUO\Data\Client'
sos_navigator_settings.refresh_interval = 300
