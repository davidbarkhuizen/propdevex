from datetime import datetime
import logging
LOG_FILE_PATH = '/var/log/sdmm/'
LOG_FILENAME = 'site_updater.log'
LOG_FORMAT = "%(asctime)-15s - %(message)s"

def init_logging():
  fname = LOG_FILE_PATH + LOG_FILENAME  
  logging.basicConfig(filename=fname, level=logging.INFO, format=LOG_FORMAT)  

# --------------------------------------------------------------------

import json

from dal.db import db_connection_factory
from siteupdater.ftpupdater import update_all_sites

def connect():

	credentials = None
	try:
		credentials = json.load(open('config.json'))
	except Exception as e:
		logging.info('config load failed: {0}'.format(str(e)))
		return

	get_new_db_connection = None
	try:
		get_new_db_connection = db_connection_factory(
			credentials['db_host'],
			credentials['db_name'],
			credentials['db_user'],
			credentials['db_password']
			)
	except Exception as e:
		logging.info('failed to establish a connection to the database: {0}'.format(str(e)))
		return None

def run():

	get_new_db_connection = connect()
	if get_new_db_connection is None:
		return

	try:
		update_all_sites(get_new_db_connection)
	except Exception as e:
		logging.info('site update failed: {0}'.format(str(e)))
		return

if __name__ == "__main__":
	init_logging()
	logging.info('started')
	run()   