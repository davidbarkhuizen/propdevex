from django.db import connection
from sitemodel.interface import SiteInterface, SiteModel

from sitemodel.frp.model import  FRP_Category, FRP_Contact, FRP_Property, FRP_Stand

SITE_NAME = 'FisherRoelandProperty' 
SITE_TOKEN = 'frp'
USER_EDITABLE_MODEL_NAMES = ['frp_contact', 'frp_property', 'frp_stand']
SITE_USER_NAMES = [ 'frpjenny', 'frpmelissa' ]

CATEGORY_NAMES : [
	'commercial',
	'industrial',
	'residential',
	'business',
	'hotel',
	'retail',
	'investment',
	'sold'
	]

def populate_model_constants():

	# category

	for category_name in CATEGORY_NAMES:
		
		if FRP_Category.objects.filter(name=category_name).exists():
			continue

		db_category = FRP_Category(name=category_name)
		db_category.save()

def randomly_populate_datamodel():

	if len(FRP_Contact.objects.all()) > 0:
		return

	for category in FRP_Category.objects.all():

		# contact

		name = random_str(8)
		email = random_str(8) + '@' + random_str(8) + '.com'  
		phone = random_str(8)
		
		db_contact = FRP_Contact(name=name, email=email,phone=phone)
		db_contact.save()
		db_contact.categories.add(category)
		db_contact.save()

		# properties

		name = random_str(20)
		title = random_str(50)
		description = '\r\n'.join([random_str(20) for i in range(5)])
		udf = None

		db_Property = FRP_Property(category=category, name=name, title=title, description=description, udf=udf)
		db_Property.save()

		for i in range(random.randint(0,3)):

			name = random_str(20)
			units = random.choice(range(100))
			situationDescription = '\r\n'.join([random_str(20) for i in range(5)])
			areaSQM = random.randint(10000,100000)

			stand = FRP_Stand(property=db_Property, name=name, units=units, situationDescription=situationDescription, areaSQM=areaSQM)
			stand.save()

def render_site_model():
	
	data_model = {}
	db_text_uploads = []
	db_binary_uploads = []

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
		dest = None
		if (db_prop.udf.name is not None) and (len(db_prop.udf.name) > 0):

			source = source_root + '/' + db_prop.udf.name
			dest = db_prop.udf.name

			db_binary_upload = BinaryUpload(source_path=source, destination_path=dest, site=db_site)
			db_binary_uploads.append(db_binary_upload)

		property =  { "category" : db_prop.category.name,
			"name": db_prop.name, 
			"title" : db_prop.title,
			"description" : [],
			'udf' : dest,
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
	SITE_TOKEN
	SITE_USER_NAMES,
	USER_EDITABLE_MODEL_NAMES,
	populate_model_constants,
	render_site_model,
	randomly_populate_datamodel		   
	)