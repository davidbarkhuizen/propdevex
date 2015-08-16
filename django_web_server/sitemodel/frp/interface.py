import random

from django.db import connection
from django.conf import settings
from sitemodel.interface import SiteInterface, SiteModel, random_str
from django.core.files import File

from server.models import Site, TextUpload, BinaryUpload

from sitemodel.frp.model import  FRP_Category, FRP_Contact, FRP_Property, FRP_PropertyImage, FRP_SubPropertyImage

SITE_NAME = 'FisherRoelandProperty' 
SITE_TOKEN = 'frp'
USER_EDITABLE_MODEL_NAMES = [ 'frp_contact', 'frp_property', 'frp_property_image', 'frp_sub_property', 'frp_sub_property_image']
SITE_USER_NAMES = [ 'frpjenny', 'frpmelissa' ]

CATEGORY_NAMES = [
	'commercial',
	'industrial',
	'residential',
	'business',
	'hotel',
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

	import_root_location = settings.SITE_DATA_IMPORT_ROOT_FOLDER + SITE_TOKEN + '/'

	if len(FRP_Contact.objects.all()) > 0:
		return

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

		props_to_import = None
		with open(import_root + category.name + '.json', 'rt') as source_file:
			json_str = source_file.read()
			props_to_import = json.loads(json_str)

		for prop in props_to_import:			

			db_property = FRP_Property(category=category, sold=False, name=prop['name'], areaSQM=prop['areaSQM'], description=prop['description'], shortLocation=prop['shortLocation'],longLocation=prop['longLocation'], latitude=prop['latitude'], longitude=prop['longitude'])
			
			db_property.save()

			for i in range(len(prop['images'])):

				prop_image_file_name = prop['images'][i]

				image_source_location = import_root_location  + category.name + '/' + prop_image_file_name

				image_source_django_file = None
				with open(image_source_location) as image_source_python_file:
					image_source_django_file = File(f)

				db_property_image = FRP_PropertyImage(property=db_property)
				db_property_image.file.save(prop_image_file_name, image_source_django_file)

				if i == 0:
					db_property_image.isprimary = True

				db_PropertyImage.save()

			for j in range(len(prop['subproperties'])):

				sub_prop = prop['subproperties'][j]				

				db_subproperty = FRP_SubProperty(property=db_Property, name=sub_prop['name'], areaSQM=sub_prop['areaSQM'], description=sub_prop['description'])

				db_subproperty.save()				

				for k in range(len(sub_prop['images'])):

					sub_prop_image_file_name = sub_prop['images'][k]

					image_source_location = import_root_location  + category.name + '/' + sub_prop_image_file_name

					image_source_django_file = None
					with open(image_source_location) as image_source_python_file:
						image_source_django_file = File(f)

					db_sub_property_image = FRP_SubPropertyImage(property=db_property)
					db_sub_property_image.file.save(sub_prop_image_file_name, image_source_django_file)

					if k == 0:
						db_sub_property_image.isprimary = True

					db_sub_property_image.save()


def render_site_model(site_token):
	
	data_model = {}
	db_text_uploads = []
	db_binary_uploads = []

	db_site = Site.objects.get(token=site_token)

	# CONTACTS
	#
	data_model['contacts'] = []
	for db_contact in FRP_Contact.objects.all():

		contact = { "name" : db_contact.name,
			"phone" : db_contact.phone,
			"email" : db_contact.email,
			"categories" : []
			}
		
		for db_category in db_contact.categories.all():
			contact['categories'].append(db_category.name)
		
		data_model['contacts'].append(contact)

	# PROPERTIES
	#
	data_model['properties'] = []
	for db_prop in FRP_Property.objects.all(): 

		source = None
		dest_path = None
		if (db_prop.udf.name is not None) and (len(db_prop.udf.name) > 0):

			source = settings.MEDIA_ROOT + '/' + db_prop.udf.name
			dest_path = '/'.join(db_prop.udf.name.split('/')[1:])

			db_binary_upload = BinaryUpload(source_path=source, destination_path=dest_path, site=db_site)
			db_binary_uploads.append(db_binary_upload)

		property =  { "category" : db_prop.category.name,
			"name": db_prop.name, 
			"title" : db_prop.title,
			"description" : [],
			'udf' : dest_path,
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

			property['stands'].append(stand)

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