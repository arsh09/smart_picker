import threading
import gps
from gps import *
import time

class GPS(threading.Thread):
    def __init__(self, gps_data_callback = None):
        super(GPS, self).__init__()
        self.gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
        self.callback = gps_data_callback
        #               (lat, lon, epx, epy, ts)
        self.last_data = (-1, -1, -1, -1, -1)
        self.has_more_data = True
        self.stop_event = threading.Event()

    def _getData(self):
        nx = None
        try:
            nx = self.gpsd.next() # this is blocking
        except StopIteration:
            print("ERROR no more data from gpsd")
            self.has_more_data = False
            # TODO maybe stop the thread here?
        
        return nx

    def _getPositionData(self):
            lat = -1
            lon = -1
            epx = -1
            epy = -1
            
            data = self._getData()
            
            while not(data['class'] == 'TPV'):
                data = self._getData()
            
            lat = getattr(data, 'lat', -1)
            lon = getattr(data, 'lon', -1)
                    #print ("Your position: lat = " + str(lat) + ", lon = " + str(lon))
                    
            epx = getattr(data, 'epx', -1)
            epy = getattr(data, 'epy', -1)
            print ("lat error = " + str(epy) + "m" + ", lon error = " + str(epx) + "m") 

            return lat, lon, epx, epy, time.time()

    def set_callback(self, cb):
        self.callback = cb        

    def get_latest_data(self):
        return self.last_data

    def has_more_data(self):
        return self.has_more_data

    def run(self):
        while not self.stop_event.is_set():
            # get latest postion
            lat, lon, epx, epy, ts = self._getPositionData() # blocking

            self.last_data = (lat, lon, epx, epy, ts)
            
            # call callback 
            if self.callback is not None:
                self.callback(lat, lon, epx, epy, ts)

    def stop(self):
        self.stop_event.set()
