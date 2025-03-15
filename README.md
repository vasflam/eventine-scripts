SOS Navigator configuration:
- Add script to razor
- Run it and stop
- Close the client
- Open SOSNavigator.json in settings folder 
- Set `markers_dir` to your ClassicUO Data folder, required!
- Change the values (item serials must be converted from hex to decimal)

Example
```
{
    "fishing_settings": {
        "cut_raw_fish": true,
        # Serial of container where to put fish steaks
        "steaks_container": 1074990012,
        # Attack enemies while fishing
        "attack_enemies": true,
        # Weapon serial to equip
        "weapon": 1078077802,
        # Use discordance on emenies, at this time only tambourines are used
        "discord_target": true,
        # Loot nearby corpses, if you have large fishing net
        # it will pull corpses to you
        "loot_corpses": true,
        # Where to loot corpses
        "loot_container": 1079887362,
        # List of items graphic id to loot, by default it loots
        # maps, sos bottles, gold and fishing nets
        "graphics_loot_table": [
            3530,
            3821,
            5356,
            2463
        ],
        # List of item names to loot, empty by default
        "names_loot_table": []
    },
    # You should set this to your client Data folder
    "markers_dir": "C:\\ClassicUO\\Data",
    # How often to refresh gump in milisecconds
    "refresh_interval": 300,
    # Gump position
    "gump_position": [
        0,
        100
    ]
}
```