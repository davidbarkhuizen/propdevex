def get_ids_of_sites_marked_for_update(db):

	sql = 'select id from site where update = true;'

	ids = []
	connection = db()
	try:
		for row in connection.fetchall(sql):
			ids.append(row[0])
	finally:
		connection.close()

	return ids

def get_ftp_credentials_for_site(db, id):
	"""returns { host, port, user, password, upload_root }"""

	sql = '''
	select ftp_host, ftp_port, ftp_user, ftp_password, ftp_upload_root
	from site
	where id = {0}'''.format(id)

	ftp_creds = None
	connection = db()
	try:
		row = connection.fetchone(sql)
		ftp_creds = { "host" : row[0],
			"port" : row[1],
			"user" : row[2],
			"password" : row[3],
			"upload_root" : row[4] }
	finally:
		connection.close()

	return ftp_creds

def get_text_uploads_for_site(db, id):
	"""returns [ { source_path, destination_path } ]"""

	sql = '''
	select source_path, destination_path 
	from textupload
	where site_id = {0}'''.format(id)

	connection = db()

	text_uploads = []
	try:
		for row in connection.fetchall(sql):
			text_upload = { "source_path" : row[0], "destination_path" : row[1] } 
			text_uploads.append(text_upload)
	finally:
		connection.close()

	return text_uploads

def get_binary_uploads_for_site(db, id):
	"""returns [ { source_path, destination_path } ]"""

	sql = '''
	select source_path, destination_path 
	from binaryupload
	where site_id = {0}'''.format(id)

	binary_uploads = []
	connection = db()
	try:
		for row in connection.fetchall(sql):
			binary_upload = { "source_path" : row[0], "destination_path" : row[1] } 
			binary_uploads.append(binary_upload)
	finally:
		connection.close()

	return binary_uploads

def mark_site_as_updated(db, id, msg):

	# sanitize
	msg = msg.replace('\'', '').replace('\"', '')

	sql = '''
	update site
	set
		update = false,
		last_updated_at = now(),
		update_log_message = '{1}' 
	where
		id = {0};
	'''.format(id, msg)

	connection = db()
	try:
		connection.execute(sql)
	except Exception as e:
		print(e)
	finally:
		connection.close()