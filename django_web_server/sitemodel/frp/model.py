from django.db import models

IMAGE_ROOT = 'frp/image'

class FRP_Category(models.Model):
	class Meta:
		db_table = "frp_category"
		verbose_name = "category"
		verbose_name_plural = "categories"
		app_label = 'server'

	name 			= models.CharField(max_length=1024, unique=True, null=False)

	def __str__(self):
		return self.name

class FRP_Contact(models.Model):
	class Meta:
		db_table = "frp_contact"
		verbose_name = "contact"
		verbose_name_plural = "contacts"
		app_label = 'server'

	name 			= models.CharField(max_length=1024, unique=True, null=False)
	phone 			= models.CharField(max_length=1024, null=False)
	email 			= models.CharField(max_length=1024, null=False)
	categories 		= models.ManyToManyField(FRP_Category, blank=True)
	isprimary 		= models.BooleanField(null=False, default=False)
	iscc 			= models.BooleanField(null=False, default=False)

	def __str__(self):
		return self.name

class FRP_Property(models.Model):
	class Meta:
		db_table = "frp_property"
		verbose_name = "property"
		verbose_name_plural = "properties"
		app_label = 'server'

	category 		= models.ForeignKey(FRP_Category, null=False)

	sold 			= models.BooleanField(null=False, default=False)

	name 			= models.CharField(max_length=1024, unique=False, null=False)
	areaSQM 		= models.IntegerField(null=True, blank=True)
	description 	= models.TextField(null=True, blank=True)
	
	shortLocation 	= models.CharField(max_length=1024, unique=False, null=False)
	longLocation 	= models.CharField(max_length=1024, unique=False, null=False)
	
	latitude 		= models.DecimalField(decimal_places=6, max_digits=9, null=True, blank=True)
	longitude 		= models.DecimalField(decimal_places=6, max_digits=9, null=True, blank=True)

	def __str__(self):
		return "({0}) {1}".format(self.category.name, self.name)

class FRP_PropertyImage(models.Model):
	class Meta:
		db_table = "frp_property_image"
		verbose_name = "propertyimage"
		verbose_name_plural = "propertyimages"
		app_label = 'server'

	property		= models.ForeignKey(FRP_Property, null=False)	
	file 			= models.FileField(upload_to=IMAGE_ROOT, null=False)
	isprimary 		= models.BooleanField(null=False, default=False)

class FRP_SubProperty(models.Model):
	class Meta:
		db_table = "frp_sub_property"
		verbose_name = "subproperty"
		verbose_name_plural = "subproperties"
		app_label = 'server'

	property 		= models.ForeignKey(FRP_Property, null=False)

	sold 			= models.BooleanField(null=False, default=False)

	name 			= models.CharField(max_length=1024, unique=False, null=True)
	description 	= models.TextField(null=True, blank=True)
	areaSQM			= models.IntegerField(null=True, blank=True)

	def __str__(self):
		return "({0}) {1}".format(self.property.name, self.name)

class FRP_SubPropertyImage(models.Model):
	class Meta:
		db_table = "frp_sub_property_image"
		verbose_name = "subpropertyimage"
		verbose_name_plural = "subpropertyimages"
		app_label = 'server'

	subproperty 	= models.ForeignKey(FRP_SubProperty, null=False)	
	file 			= models.FileField(upload_to=IMAGE_ROOT, null=False)
	isprimary 		= models.BooleanField(null=False, default=False)