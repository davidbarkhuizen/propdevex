from ftplib import FTP
import os

class FtpClient(object):

	def __init__(self, host, port, user, pwd, ac = None):
		
		self.host = host
		self.port = port
		self.user = user
		self.pwd = pwd
		self.ac = ac

		self.ftp = FTP()
		self.ftp.connect(self.host, self.port)
		self.ftp.login(self.user, self.pwd, self.ac)

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		if self.ftp:
			self.close()

	def upload_text_file(self, source_path, dest_path, ignore_if_same_size = True):

		source_size = os.path.getsize(source_path)
		dest_file_size = self.ftp.size(dest_path)

		if ((source_size == dest_file_size) and (ignore_if_same_size == True)):
			print(source_path + ' - unchanged, ignoring')
			return

		with open(source_path) as source_text_file:
			resp = self.ftp.storlines("STOR " + dest_path, source_text_file)

	def upload_bin_file(self, source_path, dest_path, ignore_if_same_size = True):

		source_size = os.path.getsize(source_path)
		dest_file_size = self.ftp.size(dest_path)

		if ((source_size == dest_file_size) and (ignore_if_same_size == True)):
			print(source_path + ' - unchanged, ignoring')
			return

		with open(source_bin_file_path, 'rb') as source_bin_file:
			resp = ftp.storbinary("STOR " + dest_bin_file_name, source_bin_file, 1024)

	def close(self):
		if self.ftp:
			try:
				self.ftp.quit() # polite
			except:
				self.ftp.close() # unilateral

# -----------------------------------------------------------------------------------

source_text_file_path = '/home/david/code/propdevex/github/site_under_development/index.html'
dest_text_file_path = 'public_html/index.html'

source_bin_file_path = '/home/david/code/propdevex/github/site_under_development/under_development.jpg'
dest_bin_file_path = 'public_html/under_development.jpg'

host = 'frog'
port = 21
user = 'dog'
pwd = 'cat'
ac = None

with FtpClient(host, port, user, pwd) as client:
	client.upload_text_file(source_text_file_path, dest_text_file_path)
	client.upload_bin_file(source_bin_file_path, dest_bin_file_path)
