import logging

from Sanity import get_instance

logging.basicConfig(filename='logs/server.log', level=logging.INFO)
app = get_instance()
