from x import X
from point import Point
from track import Track
from waypoint import WayPoint
from segment import Segment
from gpx import GPX

def def_log_fn(s):
    pass

# ---------------------------------------------------------------
# TIME

import datetime
DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

# https://docs.python.org/2.4/lib/datetime-tzinfo.html
#
class UTC(datetime.tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return datetime.timedelta(0)

# Garmin GPX 1.1 Date Format 
# 2012-09-16T10:024306
# http://www.w3.org/TR/NOTE-datetime
# ISO 8601, specif7e19in UTC @ resolution = Complete date plus hours, minutes and seconds
# YYYY-MM-DDThh:mm:ssZ (eg 1997-07-16T19:20:30Z)

def parseGarmin11DateTimeString(s):

    # YYYY-MM-DDThh:mm:ssZ

    year = s[0:4]
    month = s[5:7]
    day = s[8:10]

    # http://www.w3.org/TR/NOTE-datetime
    hours = s[11:13]
    mins = s[14:16]
    secs = s[17:19]

    dt = datetime.datetime(int(year), int(month), int(day), int(hours), int(mins), int(secs), tzinfo=UTC())

    return dt

# ---------------------------------------------------------------

def blank_metadata():

    #'author' : None,
    #'linkURL' : None,
    #'linkText' : None,
    #'keywords' : None,
    #'minLat' : None,
    #'minLon' : None,
    #'maxLat' : None,
    #'maxLon' : None 

    return { 'name' : None, 'desc' : None, 'time' : None }

def parse_metadata(find, findall):
    '''
    '''

    metadata = blank_metadata()

    # time

    try:
        metadata_time_string = find('metadata/time').text
        metadata_time = datetime.datetime.strptime(metadata_time_string, DATE_TIME_FORMAT)    
        metadata['time'] = metadata_time
    except Exception, e:
        pass

    # simple fields

    simpleFields = ['name', 'desc', 'author']

    for field in simpleFields:
        try:
            metadata[field] = find('metadata/' + field).text
        except Exception, e:
            pass

    return metadata

def parse_tracks(find, findall, ns):

    tracks = []

    for raw_track in findall('trk'):

        try:
            name = raw_track.find(ns + 'name').text
        except Exception, e:
            name = 'unnamed track'

        segments = []

        for raw_segment in raw_track.findall(ns + 'trkseg'):

            points = []
            
            for raw_point in raw_segment:
              
                try: lat = float(raw_point.get('lat'))
                except Exception, e:
                    print(e)
                    lat = None

                try: lon = float(raw_point.get('lon'))
                except Exception, e:
                    print(e)
                    lon = None

                try: elevation = float(raw_point.find(ns + 'ele').text)
                except Exception, e: 
                    print(e) 
                    elevation = None

                try: time = datetime.datetime.strptime((raw_point.find(ns + 'time').text), DATE_TIME_FORMAT)
                except Exception, e: 
                    print(e) 
                    time = None

                if len([x for x in [lat, lon, elevation, time] if x != None]) != 0:
                    try:
                        point = Point(lat, lon, elevation, time)     
                        points.append(point) 
                    except Exception, e: 
                        print(e)
                        pass

            points = sorted(points, key=lambda x : x.time)
            segment = Segment(points)

            segments.append(segment)

        try:
            track = Track(name, segments)
            tracks.append(track)
        except Exception, e: 
            print(e)
            pass

    return tracks

def parse_waypoints(find, findall, ns):

    waypoints = []

    xml_waypoints = findall('wpt')

    for xml_waypoint in xml_waypoints:       
          
        name = str(xml_waypoint.find(ns + 'name').text)
        lat = float(xml_waypoint.get('lat'))
        lon = float(xml_waypoint.get('lon'))
        elevation = float(xml_waypoint.find(ns + 'ele').text)
        time = parseGarmin11DateTimeString(xml_waypoint.find(ns + 'time').text)
        
        waypoint = WayPoint(name, lat, lon, elevation, time)
        
        waypoints.append(waypoint) 

    return waypoints 

def parse_gpx_xml(xml_string, log = def_log_fn):

    x = X(xml_string)
    ns = x.ns

    def find(path): return x.find(path)
    def findall(path): return x.findall(path)

    metadata = parse_metadata(find, findall)
    tracks = parse_tracks(find, findall, ns)
    waypoints = parse_waypoints(find, findall, ns)

    return GPX(metadata, tracks, waypoints)