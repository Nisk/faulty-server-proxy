from http.client import RemoteDisconnected
from json import JSONDecodeError
from urllib import request
from urllib.error import URLError, HTTPError
import json
from socket import timeout
import logging

class SanitizeProxy():
    url = None
    timeout = 4.9

    def __init__(self, api_url, maximum_timeout=4.9):
        self.url = api_url + "/%d"
        self.timeout = maximum_timeout

    def getVIP(self, point_in_time):
        success_code = 503
        rtn = { "lat" : 0.0, "long" : 0.0 }

        try:
            response = request.urlopen(url=self.url % point_in_time, timeout=self.timeout)
            valid, data = self._parseJson(response.read())
            if valid:
                if 'latitude' in data and 'longitude' in data:
                    rtn['lat'] = data['latitude']
                    rtn['long'] = data['longitude']
                    success_code = 200
            else:
                success_code = 502

            response.close()

        except URLError as e:
            logging.error("URL Error: %s" % e.reason)
        except HTTPError as e:
            logging.error("HTTP Error: %s - %s" % e.code, e.read())
        except timeout as e:
            logging.error( str(e) )
            success_code = 504
        except RemoteDisconnected as e:
            logging.error( str(e) )
            success_code = 502

        return success_code, rtn

    def _parseJson(self, rawdata):
        success = False
        result = None

        try:
            result = json.loads(rawdata)
        except JSONDecodeError as e:
            logging.error("Failed to process json from backend: ")
        except Exception as e:
            logging.error("unspecified error occurred: ", str(e))
        else:
            success = True

        return success, result