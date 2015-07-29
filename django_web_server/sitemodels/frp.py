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










