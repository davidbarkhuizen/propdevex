from django.db import models

class Site(models.Model):
	class Meta:
		db_table = "site"
		app_label = 'server'

	Name = models.CharField(max_length=1024, unique=True, null=False)

	def __str__(self):
		return ','.join([self.Name, self.Phone, self.Email])

from sitemodels.frp import FRP_Contact
from sitemodels.frp import FRP_Category
from sitemodels.frp import FRP_Property
from sitemodels.frp import FRP_Stand

__all__ = [ 
    'FRP_Contact',
    'FRP_Category',
    'FRP_Property',
    'FRP_Stand',
]