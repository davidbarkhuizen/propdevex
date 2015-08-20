import logging

from ftpclient import FtpClient 

from dal.site import get_ids_of_sites_marked_for_update 
from dal.site import get_ftp_credentials_for_site
from dal.site import get_binary_uploads_for_site
from dal.site import get_text_uploads_for_site
from dal.site import mark_site_as_updated

# -----------------------------------------------------------------------------------

def update_site(db, id):

	logging.info('id ' + str(id))

	# preferred to an extra db call
	#
	ftp_creds, site_name = get_ftp_credentials_for_site(db, id)

	logging.info(site_name)

	binary_uploads = get_binary_uploads_for_site(db, id)
	logging.info('{0} binary uploads'.format(len(binary_uploads)))	

	text_uploads = get_text_uploads_for_site(db, id)
	logging.info('{0} text uploads'.format(len(text_uploads)))	

	with FtpClient(
		ftp_creds['host'], ftp_creds['port'], 
		ftp_creds['user'], ftp_creds['password']
		) as client:

		uploads = []
		uploads.extend(binary_uploads)
		uploads.extend(text_uploads)

		for binary_upload in uploads:
			dest_path = ftp_creds['upload_root'] + '/' + binary_upload['destination_path'] 
			client.upload_bin_file(
				binary_upload['source_path'], 
				dest_path
				)	

		logging.info(site_name + ' done.')

def update_all_sites(db):
	
	site_ids = get_ids_of_sites_marked_for_update(db)
	if len(site_ids) == 0:
		logging.info('no site marked for update')
		return
	
	for id in site_ids:
		update_site(db, id)
		mark_site_as_updated(db, id, 'update succeeded')