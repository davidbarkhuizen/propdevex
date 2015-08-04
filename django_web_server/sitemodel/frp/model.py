from django.db import models

UDF_ROOT = 'udf'

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
	udf = models.FileField(upload_to=UDF_ROOT, null=True)

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