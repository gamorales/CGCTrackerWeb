#!/usr/bin/python
# -*- coding: utf-8 -*

commands = {
    "load":              "LOAD",                          # Success log on
    "on":                "ON",                            # on line
    "single_pos00":      "**,imei:#imei#,B",              # Single position
    "single_pos01":      "**,imei:#imei#,100",            # Single position
    "multi_pos00":       "**,imei:#imei#,C,#time#",       # Mutiple position
    "multi_pos01":       "**,imei:#imei#,C,10s",          # Mutiple position
    "multi_pos02":       "**,imei:#imei#,C,15s",          # Mutiple position
    "multi_pos03":       "**,imei:#imei#,C,20s",          # Mutiple position
    "multi_pos04":       "**,imei:#imei#,C,30s",          # Mutiple position
    "multi_pos05":       "**,imei:#imei#,C,1m",           # Mutiple position
    "multi_pos06":       "**,imei:#imei#,C,5m",           # Mutiple position
    "multi_pos07":       "**,imei:#imei#,C,10m",          # Mutiple position
    "multi_pos08":       "**,imei:#imei#,C,30m",          # Mutiple position
    "multi_pos09":       "**,imei:#imei#,C,1h",           # Mutiple position
    "multi_pos10":       "**,imei:#imei#,C,5h",           # Mutiple position
    "multi_pos11":       "**,imei:#imei#,C,10h",          # Mutiple position
    "multi_pos12":       "**,imei:#imei#,C,24h",          # Mutiple position
    "cancel_pos":        "**,imei:#imei#,D",              # Position cancel
    "move_alarm":        "**,imei:#imei#,G",              # Move alarm
    "move_cancel":       "**,imei:#imei#,E",              # Alarm cancel
    "over_speed":        "**,imei:#imei#,H,#speed#",      # Over speed alarm(speed xKM/hour,it has 10-300 for option)
    "time_setup":        "**,imei:#imei#,I,-5",           # Time set up(Time zone+1,it has 1-12 for option,different from positive and negative)
    "sms_mode00":        "**,imei:#imei#,N",              # Back to SMS mode
    "sms_mode01":        "**,imei:#imei#,113",            # Back to SMS mode
    "track_time":        "**,imei:#imei#,101,#time#",     # Report location by time interval
    "track_distance":    "**,imei:#imei#,103,#distance#", # Report location by distance interval (eg. 0200m)
    "cancel_track":      "**,imei:#imei#,102",            # Cancel auto track continuosly
    "cancel_alarm":      "**,imei:#imei#,104",            # All alarms settings will be cancel
    "set_move_alarm":    "**,imei:#imei#,105,65535",      # Tracker will alarm when goes out of 200M, after set movement alarm
    "cancel_move_alarm": "**,imei:#imei#,106",            # 
    "set_overspeed":     "**,imei:#imei#,107,080",        # Set over_speed alarm
    "set_time":          "**,imei:#imei#,108,#time#",     # Set time zone (eg. -5 Colombia)
    "cut_off_oil":       "**,imei:#imei#,109",            # Cut off oil and power
    "resume_oil":        "**,imei:#imei#,110",            # Resume the oil and power
    "arm":               "**,imei:#imei#,111",            # 
    "disarm":            "**,imei:#imei#,112",            # 
    "geo_fence":         "**,imei:#imei#,113,#latitud01#,#longitud01#;#latitud02#,#longitud02#",         # Set Geo-fence
    "cancel_geo":        "**,imei:#imei#,115",            # Cancel Geo-fence
    "speed_limit_on":    "**,imei:#imei#,150",            # Activate speed limit mode
    "speed_limit_off":   "**,imei:#imei#,151",            # Deactivate speed limit mode
    "speed_limit":       "**,imei:#imei#,152,#speed#",    # Activate speed limit (eg. 080)
}

