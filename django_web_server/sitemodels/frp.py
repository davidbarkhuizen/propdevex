from django.db import models
from server.models import Site, BinaryUpload, TextUpload

import json

class FRP_Category(models.Model):
	class Meta:
		db_table = "frp_category"
		verbose_name = "category"
		verbose_name_plural = "categories"
		app_label = 'server'

	name = models.CharField(max_length=1024, unique=True, null=False)

	def __str__(self):
		return self.name

class FRP_Contact(models.Model):
	class Meta:
		db_table = "frp_contact"
		verbose_name = "contact"
		verbose_name_plural = "contacts"
		app_label = 'server'

	name = models.CharField(max_length=1024, unique=True, null=False)
	phone = models.CharField(max_length=1024, unique=True, null=False)
	email = models.CharField(max_length=1024, unique=True, null=False)
	categories = models.ManyToManyField(FRP_Category, null=True, blank=True)

	def __str__(self):
		return ','.join([self.name, self.phone, self.email])

class FRP_Property(models.Model):
	class Meta:
		db_table = "frp_property"
		verbose_name = "property"
		verbose_name_plural = "properties"
		app_label = 'server'

	category = models.ForeignKey(FRP_Category, null=False)
	name = models.CharField(max_length=1024, unique=True, null=False)
	title = models.CharField(max_length=1024, null=False)
	description = models.TextField(null=True)
	udf = models.FileField(upload_to='MEDIA', null=True)

	def __str__(self):
		return self.name

class FRP_Stand(models.Model):
	class Meta:
		db_table = "frp_stand"
		verbose_name = "stand"
		app_label = 'server'

	property = models.ForeignKey(FRP_Property, null=False)
	name = models.CharField(max_length=1024, unique=False, null=True)
	units = models.IntegerField(null=False)
	situationDescription = models.TextField(null=True)
	areaSQM = models.IntegerField(null=False)

	def __str__(self):
		return self.name + ' x ' + str(self.units) + ' @ ' + str(self.areaSQM) + ' SQM'

# ---------------------------

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType


from django.db import connection

def init_db_model():

	# create users

	usernames = ['FRP_jenny', 'FRP_melissa'] 
	default_password = 'password'

	users = []

	for username in usernames:
		user = User.objects.create_user(username=username, password=default_password)
		user.save()
		users.append(user)

	# create site

	site = Site(name='FisherRoelandProperty', ftp_host='host', ftp_port=21, ftp_user='user', ftp_password='password')
	site.save()

	david = User.objects.get(username='david')
	users.append(david)

	for user in users:
		site.users.add(user)

	site.save()

	cursor = connection.cursor() 	
	try:
		auth_group_name = 'FisherRoelandProperty'

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

		sql = "select id from django_content_type  as dct where dct.model in ('frp_contact', 'frp_property', 'frp_stand');" 

		cursor.execute(sql)
		content_type_ids = [str(row[0]) for row in cursor.fetchall()]

		print('content_type_ids')
		print(content_type_ids)

		# auth_permission.id

		sql = '''select id from auth_permission where content_type_id in ({0});
		'''.format(','.join(content_type_ids))
		cursor.execute(sql)
		auth_permission_ids = [row[0] for row in cursor.fetchall()]

		print('auth_permission_ids')
		print(auth_permission_ids)

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

			print(sql)
			cursor.execute(sql)

		# auth_user_groups

		for user in users:

			sql = '''
			insert into auth_user_groups
			(id, user_id, group_id)
			values ((1 + (select max(id) from auth_user_groups)), {0}, {1})
			'''.format(user.id, auth_group_id)

			cursor.execute(sql)

	finally:
		cursor.close()

def render_data_model():

	data_model = {}

	# CONTACTS
	#
	data_model['contacts'] = []
	for db in FRP_Contact.objects.all():

		contact = { "name" : db.name,
			"phone" : db.phone,
			"email" : db.email,
			"categories" : []
			}
		
		for category in db.categories:
			contact.categories.append(category)
		
		data_model['contacts'].append(contact)

	# PROPERTIES
	#
	data_model['properties'] = []
	for db_prop in FRP_Property.objects.all(): 

		property =  { "category" : db_prop.category.name,
			"name": db_prop.name, 
			"title" : db_prop.title,
			"description" : [],
			'udf' : '' if db_prop.udf is None else db_prop.udf,
			'stands' : []
			}

		# description
		#
		if db_prop.description is not None:
			property['description'] = db_prop.description.split('\n')

		# stands
		#
		for db_stand in FRP_Stand.objects.filter(property=db_prop):

			stand = { "name" : db_stand.name,
				"areaSQM" : db_stand.areaSQM,
				"units" : db_stand.units,
				"situationDescription" : []
				}

			if db_stand.situationDescription is not None:
				property['situationDescription'] = db_stand.situationDescription.split('\n')

			db_prop['stands'].append(stand)

		data_model['properties'].append(db_prop)

	print(json.dumps(data_model))