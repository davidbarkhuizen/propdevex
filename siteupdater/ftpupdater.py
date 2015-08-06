from ftpclient import FtpClient 

from dal.site import get_ids_of_sites_marked_for_update 
from dal.site import get_ftp_credentials_for_site
from dal.site import get_binary_uploads_for_site
from dal.site import get_text_uploads_for_site
from dal.site import mark_site_as_updated

# -----------------------------------------------------------------------------------

def update_site(db, id):

	ftp_creds = get_ftp_credentials_for_site(db, id)

	binary_uploads = get_binary_uploads_for_site(db, id)
	text_uploads = get_text_uploads_for_site(db, id)

	with FtpClient(
		ftp_creds['host'], ftp_creds['port'], 
		ftp_creds['user'], ftp_creds['password']
		) as client:

		# binary_uploads
		#
		for binary_upload in binary_uploads:
			dest_path = ftp_creds['upload_root'] + '/' + binary_upload['destination_path'] 
			client.upload_bin_file(
				binary_upload['source_path'], 
				dest_path
				)	
			print('uploaded ' + dest_path)

		# text_uploads
		#
		for text_upload in text_uploads:
			dest_path = ftp_creds['upload_root'] + '/' + text_upload['destination_path'] 
			client.upload_text_file(
				text_upload['source_path'], 
				dest_path
				)
			print('uploaded ' + dest_path)	

def update_all_sites(db):
	for id in get_ids_of_sites_marked_for_update(db):
		update_site(db, id)