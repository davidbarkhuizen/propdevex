from django.db import models

from django.contrib.auth.models import User

class Site(models.Model):
	class Meta:
		db_table = "site"
		app_label = 'server'

	name 					= models.CharField(max_length=1024, unique=True, null=False)
	users 					= models.ManyToManyField(User)

	datamodel_json_string	= models.TextField()
	dest_file_path			= models.CharField(max_length=1024, unique=True, null=False)
	updated					= models.BooleanField(default=True, null=False)

	ftp_host 				= models.CharField(max_length=1024, unique=True, null=False)
	ftp_port 				= models.IntegerField(null=False)
	ftp_user 				= models.CharField(max_length=1024, unique=True, null=False)
	ftp_password			= models.CharField(max_length=1024, unique=True, null=False)
	ftp_account				= models.CharField(max_length=1024, unique=True, null=False)
	ftp_secure				= models.BooleanField(default=False, null=False)

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