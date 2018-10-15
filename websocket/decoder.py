 #!/usr/bin/python
 # -*- coding: utf-8 -*

import re
import connect

def decode(gps_data):
    latitude = ""
    longitude = ""
    local_date = ""
    imei = ""

    # e.g. ##,imei:865328021048409,A;
    re_init = '^##,imei:(?P<imei>\d{15}),A'

    # e.g. 865328021048409;
    re_heartbeat = '^(?P<imei>\d{15})'
 
    # e.g. imei:865328021048409,tracker,141210110820,,F,030823.000,A,3745.9502,S,14458.2049,E,1.83,119.35,,0,0,0.0%,,;
    """
            'imei_unparsed',        # imei:865328021048409
            'source',               # tracker
            'local_date',           # 141210110820
            'local_time',           # ''
            'type',                 # F - full / L - low
            'time',                 # 030823, UTC (HHMMSS.SSS)
            'validity',             # A / V
            'latitude',             # DDMM.MMMM
            'latitude_direction',   # N / S
            'longitude',            # DDDMM.MMMM
            'longitude_direction',  # E / W
            'speed',                # 1.83
            'course',               # 119.35
            'altitude',             # ''
            'unknown_1',            # 0
            'unknown_2',            # 0
            'gasoline',             # 0.0% GAS
            'unknown_4',            # ''
            'end_delimiter',        # ''
    """

    re_location_full = '^imei:(?P<imei>\d{15}),' + \
        'tracker,' + \
        '(?P<local_date>\d*),' + \
        '(?P<local_time>\d*),' + \
        'F,' + \
        '(?P<time_utc>\d+\.\d+)?,' + \
        '(?P<validity>[AV]),' + \
        '(?P<latitude>\d+\.\d+),' + \
        '(?P<latitude_hemisphere>[NS]),' + \
        '(?P<longitude>\d+\.\d+),' + \
        '(?P<longitude_hemisphere>[EW]),' + \
        ''
    """
        '(?P<speed>\d+\.\d+)?,' + \
        '(?P<course>\d+\.\d+)?,' + \
        '(?P<altitude>\d+\.\d+)?,' + \
        '.*;'
    """

    # e.g. imei:865328021048409,tracker,141210172556,0411959136,L,,,0BD4,,7A78,,,,,0,0,0.0%,,;
    re_location_low = '^imei:(?P<imei>\d{15}),' + \
        'tracker,' + \
        '(?P<local_date>\d*),' + \
        '(?P<local_time>\d*),' + \
        'L,' + \
        '[^,]*,' + \
        '[^,]*,' + \
        '(?P<unknown_1>\w*),' + \
        '[^,]*,' + \
        '(?P<unknown_2>\w*),' + \
        ''

    if re.match(re_init, gps_data):
        imei = re.match(re_init, gps_data).group('imei')
        local_date = re.match(re_init, gps_data).group('local_date')
    elif re.match(re_heartbeat, gps_data):
        imei = re.match(re_heartbeat, gps_data).group('imei')
        local_date = re.match(re_heartbeat, gps_data).group('local_date')
    elif re.match(re_location_full, gps_data):
        match = re.match(re_location_full, gps_data)
        imei = match.group('imei')

        local_date = match.group('local_date')
        latitude = match.group('latitude')
        latitude_hemisphere = match.group('latitude_hemisphere')
        longitude = match.group('longitude')
        longitude_hemisphere = match.group('longitude_hemisphere')

        # Latitude and Longitude need to be converted from this proto's spec to standard decimal
        # Locations come as HHHHMM.MMMM
        # hours are any number of digits, followed by
        # seconds which are 2-digit integer part, period, fractional part
        re_location = '^(\d+)(\d{2}\.\d+)$'

        (h, m) = re.match(re_location, latitude).groups()
        h = float(h)
        m = float(m)
        latitude = h + m/60
        if 'S' == latitude_hemisphere:
            latitude = -latitude

        (h, m) = re.match(re_location, longitude).groups()
        h = float(h)
        m = float(m)
        longitude = h + m/60
        if 'W' == longitude_hemisphere:
            longitude = -longitude

        # TODO - set other message properties
    elif re.match(re_location_low, gps_data):
        imei = re.match(re_location_low, gps_data).group('imei')
        # TODO - set other message properties
    else:
        return None

    # Ninggún campo debe ir vacio
    if imei!="" and latitude!="" and longitude!="" and local_date!="":
        # Se extraerá el ID del usuario para guardarlo en la Referencia Coordenadas
        return connect.consultarVehiculo(imei, latitude, longitude, local_date)
    else:
        return None

