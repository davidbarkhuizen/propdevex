from django.conf.urls import url

from ctrl import sites

urlpatterns = [
		url(r'^admin/sites/init', sites.init),
		url(r'^admin/sites/update', sites.update),

		url(r'^admin/sites/randomly_populate_datamodel', sites.randomly_populate_datamodel),
		
		url(r'^admin/sites', sites.get),
		url(r'^admin/sites$', sites.get),
	]
