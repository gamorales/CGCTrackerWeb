#!/usr/bin/python
# -*- coding: utf-8 -*

commands = {
    'load':        'LOAD',                              # Success log on
    'on':          'ON',                                # on line
    'single_pos':  '**,imei:359586018966098,B',         # Single position
    'multi_pos00': '**,imei:359586018966098,C,#time#',  # Mutiple position
    'multi_pos01': '**,imei:359586018966098,C,10s',     # Mutiple position
    'multi_pos02': '**,imei:359586018966098,C,15s',     # Mutiple position
    'multi_pos03': '**,imei:359586018966098,C,20s',     # Mutiple position
    'multi_pos04': '**,imei:359586018966098,C,30s',     # Mutiple position
    'multi_pos05': '**,imei:359586018966098,C,1m',      # Mutiple position
    'multi_pos06': '**,imei:359586018966098,C,5m',      # Mutiple position
    'multi_pos07': '**,imei:359586018966098,C,10m',     # Mutiple position
    'multi_pos08': '**,imei:359586018966098,C,30m',     # Mutiple position
    'multi_pos09': '**,imei:359586018966098,C,1h',      # Mutiple position
    'multi_pos10': '**,imei:359586018966098,C,5h',      # Mutiple position
    'multi_pos11': '**,imei:359586018966098,C,10h',     # Mutiple position
    'multi_pos12': '**,imei:359586018966098,C,24h',     # Mutiple position
    'cancel_pos':  '**,imei:359586018966098,D',         # Position cancel
    'move_alarm':  '**,imei:359586018966098,G',         # Move alarm
    'move_cancel': '**,imei:359586018966098,E',         # Alarm cancel
#    'over_speed':  '**,imei:359586018966098,H,060',    # Over speed alarm(speed 60KM/hour,it has 10-300 for option)
    'over_speed':  '**,imei:359586018966098,H,#speed#', # Over speed alarm(speed xKM/hour,it has 10-300 for option)
    'time_setup':  '**,imei:359586018966098,I,-5',      # Time set up(Time zone+1,it has 1-12 for option,different from positive and negative)
    'sms_mode':    '**,imei:359586018966098,N',         # Back to SMS mode
}