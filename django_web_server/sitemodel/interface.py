from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from server.models import Site, BinaryUpload, TextUpload

import random, string
def random_str(len):
	return ''.join(random.choice(string.letters) for i in xrange(len))

import json

DATA_MODEL_FILE_NAME = 'datamodel.json'
DEFAULT_PASSWORD = 'password'

# ---------------------------

DEFAULT_FTP_HOST = 'host'
DEFAULT_FTP_PORT = 21
DEFAULT_FTP_USER = 'user'
DEFAULT_FTP_PWD = 'password'

# ---------------------------

from django.db import connection

class SiteModel(object):

	def __init__(self, model_dict, db_text_uploads = None, db_binary_uploads = None):
		self.model = model_dict
		self.db_text_uploads = db_text_uploads
		self.db_binary_uploads = db_binary_uploads

class SiteInterface(object):

	interfaces = []
	
	def __init__(self,
		name, token,
		user_names,
		user_editable_model_names,
		populate_model_constants,
		render_site_model,
		populate_datamodel):
		
		self.name = name
		self.token = token
		self.user_names = user_names
		self.user_editable_model_names = user_editable_model_names
		self.populate_model_constants = populate_model_constants
		self.render_site_model = render_site_model
		self.populate_datamodel = populate_datamodel

	def get_json_source_root(self):
		return settings.MEDIA_ROOT + '/' + self.token + '/json/'

	def get_json_dest_root(self):
		return ''

	@classmethod
	def register(cls, 
		name, token,
		user_names,
		user_editable_model_names,
		populate_model_constants,
		render_site_model,
		populate_datamodel):

		si = SiteInterface(name, token, 
			user_names, 
			user_editable_model_names,
			populate_model_constants,
			render_site_model,
			populate_datamodel
			)

		cls.interfaces.append(si)

	@classmethod
	def get(cls, token):

		for interface in cls.interfaces:
			if interface.token == token:
				return interface

		raise KeyError(token)

def create_site(name, token):

	site = Site(
		name=name,
		token=token,
		ftp_host=DEFAULT_FTP_HOST, ftp_port=DEFAULT_FTP_PORT, 
		ftp_user=DEFAULT_FTP_USER, ftp_password=DEFAULT_PASSWORD)
	
	site.save()

	return site

def add_create_site_users(site_token, usernames):
	"""always adds root"""

	site = Site.objects.get(token=site_token)	

	# create

	existing = ['root']
	to_create = []
		
	for username in usernames:
		if User.objects.filter(username=username).exists():
			if username not in existing:
				existing.append(username)
		else:
			if username not in to_create:
				to_create.append(username)

	users = []

	for username in to_create:
		user = User.objects.create_user(username=username, password=DEFAULT_PASSWORD)
		user.save()
		users.append(user)

	for username in existing:
		user = User.objects.get(username=username)
		users.append(user)

	# add

	for user in users:
		site.users.add(user)

	site.save()

def create_auth_group_permissions(site_token, user_editable_model_names):

	cursor = connection.cursor()
	try:
		auth_group_name = site_token

		# get unused auth_group.id 

		sql = 'select 1 + coalesce((select max(id) from auth_group), 0)'
		cursor.execute(sql)
		rows = cursor.fetchone()
		auth_group_id = rows[0]

		# create auth_group
		
		sql = '''
		insert into auth_group
		(id, name) 
		values ({0}, '{1}')
		'''.format(auth_group_id, auth_group_name)

		cursor.execute(sql)

		# django_content_type.id for user-editable models 

		model_names_str = ', '.join("\'" + model_name + "\'" for model_name in user_editable_model_names) 

		sql = "select id from django_content_type  as dct where dct.model in ({0});".format(model_names_str) 

		cursor.execute(sql)
		content_type_ids = [str(row[0]) for row in cursor.fetchall()]

		# auth_permission.id

		sql = '''select id from auth_permission where content_type_id in ({0});
		'''.format(','.join(content_type_ids))
		cursor.execute(sql)
		auth_permission_ids = [row[0] for row in cursor.fetchall()]

		# auth_group_permissions

		for auth_permission_id in auth_permission_ids:

			sql = '''
			insert into auth_group_permissions
			(
				id, 
				group_id, 
				permission_id
			) 
			values 
			(
				(select 1 + coalesce((select max(id) from auth_group_permissions), 0)),
				{0}, 
				{1}
			)
			'''.format(auth_group_id, auth_permission_id)

			cursor.execute(sql)
	finally:
		cursor.close()

def add_site_users_to_auth_group(site_token):

	cursor = connection.cursor()
	try:
		site = Site.objects.get(token = site_token)
		
		sql = """select id from auth_group where name = '{0}'""".format(site_token)
		cursor.execute(sql)
		auth_group_id = cursor.fetchone()[0]

		for user in site.users.all(): 

			sql = '''
			insert into auth_user_groups
			(id, user_id, group_id)
			values
			(
				(select 1 + coalesce((select max(id) from auth_user_groups), 0)), 
				{0}, {1}
			)
			'''.format(user.id, auth_group_id)

			cursor.execute(sql)
	finally:
		cursor.close()

def update_data_model(site_token, site_model):

	site = SiteInterface.get(site_token)	

	db_site = Site.objects.get(token=site_token)
	db_site.json_data_model = json.dumps(site_model.model)

	db_text_uploads = site_model.db_text_uploads
	db_binary_uploads = site_model.db_binary_uploads

	source_root = settings.MEDIA_ROOT

	json_source_location = site.get_json_source_root() + DATA_MODEL_FILE_NAME 
	with open(json_source_location, 'wt') as json_file:
		json_file.write(db_site.json_data_model)

	json_dest_location = site.get_json_dest_root() + DATA_MODEL_FILE_NAME

	text_upload = TextUpload(
		site=db_site, 
		source_path=json_source_location, 
		destination_path=json_dest_location)

	db_text_uploads.append(text_upload)

	# binary uploads - delete all old, save from SiteModel

	for to_delete in BinaryUpload.objects.filter(site=db_site):
		to_delete.delete()

	for db_binary_upload in db_binary_uploads:
		db_binary_upload.save()

	# text uploads - delete all old, save from SiteModel

	for to_delete in TextUpload.objects.filter(site=db_site):
		to_delete.delete()

	for db_text_upload in db_text_uploads:
		db_text_upload.save()

	db_site.save()

# -----------------------------------------------------------------------------
# IMPLEMENTATION-SPECIFIC

def init(site_token):

	interface = SiteInterface.get(site_token)
	
	create_site(interface.name, interface.token)
	add_create_site_users(interface.token, interface.user_names)
	create_auth_group_permissions(interface.token, interface.user_editable_model_names)
	add_site_users_to_auth_group(interface.token)

def populate_model_constants(site_token): 

	interface = SiteInterface.get(site_token)

	interface.populate_model_constants()

def update(site_token):

	interface = SiteInterface.get(site_token)

	site_model = interface.render_site_model(site_token)
	update_data_model(site_token, site_model)

def populate_datamodel(site_token):
	
	interface = SiteInterface.get(site_token)
	interface.populate_datamodel()
