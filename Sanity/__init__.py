from flask import Flask, json, abort
from werkzeug.exceptions import HTTPException #what a great module name, just rolls off the tongue
from datetime import datetime
import time
import logging

from Sanity.proxy import SanitizeProxy

def get_instance():
    app = Flask("SanitizeProxy")
    proxy = SanitizeProxy(api_url="http://localhost:8088/v1/coords")

    @app.route('/v1/now', methods=['GET'])
    def now():
        logging.info("[ %s ] - Received request for current unix time -", time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.localtime()))
        now = datetime.now().isoformat() #in case I want to adjust
        logging.info("[ %s ] - Completed request for current unix time -", time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.localtime()))
        return { "now" : now }


    @app.route('/v1/VIP/<int:point_in_time>', methods=['GET'])
    def index(point_in_time):
        start = time.time()
        logging.info("[ %s ] - Received request for VIP location -", time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.localtime()))

        response = {
            "source" : "vip-db"
        }

        success_code, coord = proxy.getVIP(point_in_time)
        if success_code != 200:
            logging.info("completed in %f seconds." % (time.time()-start))
            abort(success_code) #throw error

        response["gpsCoords"] = coord

        logging.info("[ %s ] - Completed request for VIP location in %f seconds." % (time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.localtime()), (time.time()-start)))
        return response

    @app.errorhandler(HTTPException)
    def exceptionhandler(e):
        """
        Since we have a JSON API, return JSON errors
        :param e: exception
        :return: json representation of the error
        """
        response = e.get_response()
        response.data = json.dumps({
            "code" : e.code,
            "name": e.name,
            "description": e.description
        })
        response.content_type = "application/json"

        return response

    return app