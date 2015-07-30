from django.db import models

from django.contrib.auth.models import User

def defaultCharField(unique=False, null=True):
	return models.CharField(max_length=1024, unique=unique, null=null) 

class TextUpload(models.Model):
	
	class Meta:
		db_table = 'textupload'
		app_label = 'server'

	source_path				= defaultCharField(null=False)
	destination_path		= defaultCharField(null=False)

class BinaryUpload(models.Model):
	
	class Meta:
		db_table = 'binaryupload'
		app_label = 'server'

	source_path				= defaultCharField(null=False)
	destination_path		= defaultCharField(null=False)

class Site(models.Model):
	class Meta:
		db_table = 'site'
		app_label = 'server'

	name 					= defaultCharField(unique=True, null=False)
	users 					= models.ManyToManyField(User)

	textuploads				= models.ManyToManyField(TextUpload, null=True, blank=True)
	binaryuploads			= models.ManyToManyField(BinaryUpload, null=True, blank=True)

	update					= models.BooleanField(default=False, null=False)
	last_updated_at			= models.DateTimeField(null=True, blank=True)

	ftp_host 				= defaultCharField(null=False)
	ftp_port 				= models.IntegerField(null=False)
	ftp_user 				= defaultCharField(null=False)
	ftp_password			= defaultCharField(null=False)
	ftp_account				= defaultCharField()

	# log_message				= defaultCharField()

	def __str__(self):
		return self.name

# -------------------------------------------------------------
# FRP FisherRoelandProperties

from sitemodels.frp import FRP_Contact
from sitemodels.frp import FRP_Category
from sitemodels.frp import FRP_Property
from sitemodels.frp import FRP_Stand

# -------------------------------------------------------------

__all__ = [ 
	# framework
	#'Site',

	# FRP FisherRoelandProperties
    'FRP_Contact',
    'FRP_Category',
    'FRP_Property',
    'FRP_Stand',
]