from django.conf.urls import url

from ctrl import sites

urlpatterns = [
		url(r'^admin/sites/init', sites.init),
		url(r'^admin/sites/update', sites.update),

		url(r'^admin/sites/populate_datamodel', sites.populate_datamodel),
		
		url(r'^admin/sites', sites.get),
		url(r'^admin/sites$', sites.get),
	]
