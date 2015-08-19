import random

import json

from django.db import connection
from django.conf import settings
from sitemodel.interface import SiteInterface, SiteModel, random_str
from django.core.files import File

from server.models import Site, TextUpload, BinaryUpload

from sitemodel.frp.model import  FRP_Category, FRP_Contact, FRP_Property, FRP_PropertyImage, FRP_SubProperty, FRP_SubPropertyImage

SITE_NAME = 'FisherRoelandProperty' 
SITE_TOKEN = 'frp'
USER_EDITABLE_MODEL_NAMES = [ 'frp_contact', 'frp_property', 'frp_property_image', 'frp_sub_property', 'frp_sub_property_image']
SITE_USER_NAMES = [ 'frpjenny', 'frpmelissa' ]

CATEGORY_NAMES = [
	'commercial',
	'industrial',
	'residential',
	'business',
	'hospitality',
	'retail',
	'investment',
	'agricultural'
	]

def populate_model_constants():

	# category

	for category_name in CATEGORY_NAMES:
		
		if FRP_Category.objects.filter(name=category_name).exists():
			continue

		db_category = FRP_Category(name=category_name)
		db_category.save()

def populate_datamodel():

	print('FRP = populate_datamodel')

	import_root_location = settings.SITE_DATA_IMPORT_ROOT_FOLDER + SITE_TOKEN + '/'

	#if len(FRP_Contact.objects.all()) > 0:		
	#	return

	for category in FRP_Category.objects.all():

		# CONTACT

		name = random_str(8)
		email = random_str(8) + '@' + random_str(8) + '.com'  
		phone = random_str(8)
		
		db_contact = FRP_Contact(name=name, email=email,phone=phone)
		db_contact.save()
		db_contact.categories.add(category)
		db_contact.save()

		# PROPERTIES

		to_import = None
		try:
			with open(import_root_location + category.name + '.json', 'rt') as source_file:
				json_str = source_file.read()
				to_import = json.loads(json_str)
		except IOError as e:
			print(e)
			print('no source file found for category {0}'.format(category.name))
			continue

		for prop in to_import['properties']:			

			db_property = FRP_Property(category=category, sold=False, name=prop['name'], areaSQM=prop['areaSQM'], description=prop['description'], shortLocation=prop['shortLocation'],longLocation=prop['longLocation'], latitude=prop['latitude'], longitude=prop['longitude'])
			
			db_property.save()

			for i in range(len(prop['images'])):

				prop_image_file_name = prop['images'][i]

				image_source_location = import_root_location  + category.name + '/' + prop_image_file_name

				db_property_image = FRP_PropertyImage(property=db_property)

				image_source_django_file = None
				with open(image_source_location) as image_source_python_file:
					image_source_django_file = File(image_source_python_file)					
					db_property_image.file.save(prop_image_file_name, image_source_django_file)

				if i == 0:
					db_property_image.isprimary = True

				db_property_image.save()

			for j in range(len(prop['subproperties'])):

				sub_prop = prop['subproperties'][j]				

				db_subproperty = FRP_SubProperty(property=db_property, name=sub_prop['name'], areaSQM=sub_prop['areaSQM'], description=sub_prop['description'])

				db_subproperty.save()		

				print('subprop ', db_subproperty.name)		

				if ('images' in sub_prop.keys()):

					print('sub_prop[images]')
					print(sub_prop['images'])

					print('dir(sub_prop)')
					print(dir(sub_prop))

					if len(sub_prop['images']) > 0:
						print('has images')
					else:
						print('no image')

					for k in range(len(sub_prop['images'])):

						sub_prop_image_file_name = sub_prop['images'][k]

						image_source_location = import_root_location  + category.name + '/' + sub_prop_image_file_name

						db_sub_property_image = FRP_SubPropertyImage(subproperty=db_subproperty)
						image_source_django_file = None
						with open(image_source_location) as image_source_python_file:
							image_source_django_file = File(image_source_python_file)
							db_sub_property_image.file.save(sub_prop_image_file_name, image_source_django_file)

						if k == 0:
							db_sub_property_image.isprimary = True

						db_sub_property_image.save()

				else:
					print('no images')

def render_site_model(site_token):
	
	data_model = {}
	db_text_uploads = []
	db_binary_uploads = []

	db_site = Site.objects.get(token=site_token)

	# CONTACTS
	#
	data_model['contacts'] = []
	for db_contact in FRP_Contact.objects.all():

		contact = { 'name' : db_contact.name,
			'phone' : db_contact.phone,
			'email' : db_contact.email,
			'categories' : []
			}
		
		for db_category in db_contact.categories.all():
			contact['categories'].append(db_category.name)
		
		data_model['contacts'].append(contact)

	# PROPERTIES
	#
	data_model['properties'] = []
	for db_prop in FRP_Property.objects.all(): 

		property =  { 'category' : db_prop.category.name,
			'sold' : db_prop.sold,
			'name': db_prop.name,

			'areaSQM': db_prop.areaSQM,
			'description': [],
			'shortLocation': db_prop.shortLocation,
			'longLocation': db_prop.longLocation,
			'latitude': db_prop.latitude,
			'longitude': db_prop.longitude,

			'images' : [],
			'subproperties' : []
			}

		# description
		#
		if db_prop.description is not None:
			property['description'] = db_prop.description.split('\n')

		db_images = FRP_PropertyImage.objects.filter(property=db_prop)

		primary_db_images = [x for x in db_images if x.isprimary == True]
		secondary_db_images = [x for x in db_images if x.isprimary == False]
		
		ordered_db_images = []
		ordered_db_images.extend(primary_db_images)
		ordered_db_images.extend(secondary_db_images)

		for db_image in ordered_db_images:

			if (db_image.file.name is None) or (len(db_image.file.name) == 0):
				continue

			source = None
			dest_path = None

			source = settings.MEDIA_ROOT + '/' + db_image.file.name
			dest_path = '/'.join(db_image.file.name.split('/')[1:])

			db_binary_upload = BinaryUpload(source_path=source, destination_path=dest_path, site=db_site)
			db_binary_uploads.append(db_binary_upload)

			property['images'].append(dest_path)

		# sub property
		#
		for db_sub_property in FRP_SubProperty.objects.filter(property=db_prop):

			sub_property = { 'name' : db_sub_property.name,
				'areaSQM' : db_sub_property.areaSQM,
				'description' : [],
				'sold' : db_sub_property.sold,
				'images' : []
				}

			# description
			#
			if db_sub_property.description is not None:
				sub_property['description'] = db_sub_property.description.split('\n')

			db_images = FRP_SubPropertyImage.objects.filter(subproperty=db_sub_property)

			primary_db_images = [x for x in db_images if x.isprimary == True]
			secondary_db_images = [x for x in db_images if x.isprimary == False]
			
			ordered_db_images = []
			ordered_db_images.extend(primary_db_images)
			ordered_db_images.extend(secondary_db_images)

			for db_image in ordered_db_images:

				if (db_image.file.name is None) or (len(db_image.file.name) == 0):
					continue

				source = None
				dest_path = None

				source = settings.MEDIA_ROOT + '/' + db_image.file.name
				dest_path = '/'.join(db_image.file.name.split('/')[1:])

				db_binary_upload = BinaryUpload(source_path=source, destination_path=dest_path, site=db_site)
				db_binary_uploads.append(db_binary_upload)

				# append sub-property images to main property image list
				property['images'].append(dest_path)
				sub_property['images'].append(dest_path)

			property['subproperties'].append(sub_property)

		data_model['properties'].append(property)

	return SiteModel(data_model, 
		db_text_uploads=db_text_uploads, 
		db_binary_uploads=db_binary_uploads)

SiteInterface.register(
	SITE_NAME,
	SITE_TOKEN,
	SITE_USER_NAMES,
	USER_EDITABLE_MODEL_NAMES,
	populate_model_constants,
	render_site_model,
	populate_datamodel		   
	)