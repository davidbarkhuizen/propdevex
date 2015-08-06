import json

from dal.db import db_connection_factory
from siteupdater.ftpupdater import update_all_sites

def run():

	credentials = json.load(open('config.json'))

	get_new_db_connection = db_connection_factory(
		credentials['db_host'],
		credentials['db_name'],
		credentials['db_user'],
		credentials['db_password']
		)

	update_all_sites(get_new_db_connection)

if __name__ == "__main__":
	run()   