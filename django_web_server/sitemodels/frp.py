from django.db import models

class FRP_Contact(models.Model):
	class Meta:
		db_table = "frp_contact"
		verbose_name = "contact"
		verbose_name_plural = "contacts"
		app_label = 'server'

	Name = models.CharField(max_length=1024, unique=True, null=False)
	Phone = models.CharField(max_length=1024, unique=True, null=False)
	Email = models.CharField(max_length=1024, unique=True, null=False)

	def __str__(self):
		return ','.join([self.Name, self.Phone, self.Email])

class FRP_Category(models.Model):
	class Meta:
		db_table = "frp_category"
		verbose_name = "category"
		verbose_name_plural = "categories"
		app_label = 'server'

	Name = models.CharField(max_length=1024, unique=True, null=False)

	def __str__(self):
		return self.Name

class FRP_Property(models.Model):
	class Meta:
		db_table = "frp_property"
		verbose_name = "property"
		verbose_name_plural = "properties"
		app_label = 'server'

	Category = models.ForeignKey(FRP_Category, null=False)
	Name = models.CharField(max_length=1024, unique=True, null=False)
	Title = models.CharField(max_length=1024, null=False)
	Description = models.TextField(null=True)
	UDF = models.FileField(upload_to='MEDIA', null=True)

	def __str__(self):
		return self.Name

class FRP_Stand(models.Model):
	class Meta:
		db_table = "frp_stand"
		verbose_name = "stand"
		app_label = 'server'

	Property = models.ForeignKey(FRP_Property, null=False)
	Name = models.CharField(max_length=1024, unique=False, null=True)
	Units = models.IntegerField(null=False)
	SituationDescription = models.TextField(null=True)

	def __str__(self):
		return self.Name + ' x ' + str(self.Units)