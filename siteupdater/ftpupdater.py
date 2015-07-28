from ftplib import FTP
import os

def upload_text_file(ftp, source_path, dest_path, ignore_if_same_size = True):

	source_size = os.path.getsize(source_path)
	dest_file_size = ftp.size(dest_path)

	if ((source_size == dest_file_size) and (ignore_if_same_size == True)):
		print(source_path + ' - unchanged, ignoring')
		return

	with open(source_path) as source_text_file:
		resp = ftp.storlines("STOR " + dest_path, source_text_file)

def upload_bin_file(ftp, source_path, dest_path, ignore_if_same_size = True):

	source_size = os.path.getsize(source_path)
	dest_file_size = ftp.size(dest_path)

	if ((source_size == dest_file_size) and (ignore_if_same_size == True)):
		print(source_path + ' - unchanged, ignoring')
		return

	with open(source_bin_file_path, 'rb') as source_bin_file:
		resp = ftp.storbinary("STOR " + dest_bin_file_name, source_bin_file, 1024)

# -----------------------------------------------------------------------------------

source_text_file_path = '/home/david/code/propdevex/github/site_under_development/index.html'
dest_text_file_path = 'public_html/index.html'

source_bin_file_path = '/home/david/code/propdevex/github/site_under_development/under_development.jpg'
dest_bin_file_path = 'public_html/under_development.jpg'

host = 'frprop.com'
port = 21
user = 'frprolfe'
pwd = 'utEbvUtb'
ac = None

ftp = FTP()
ftp.connect(host, port)
ftp.login(user, pwd, ac)

upload_text_file(ftp, source_text_file_path, dest_text_file_path)
upload_bin_file(ftp, source_bin_file_path, dest_bin_file_path)

ftp.quit()