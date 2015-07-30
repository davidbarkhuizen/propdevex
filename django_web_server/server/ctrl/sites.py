from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
from django.conf import settings

from server.models import Site

import sitemodels.frp as frp

LOGIN_ROOT = '/admin'
SITE_ROOT = '/admin/sites'

def update(request):

	if not request.user.is_authenticated():
		return redirect(LOGIN_ROOT)

	site_id = None
	if 'id' in request.GET.keys():
		site_id = request.GET['id']
		site = Site.objects.get(id=site_id)

		if site.update is False:

			frp.update_data_model(site)

			site.update = True
			site.save()

	return redirect(SITE_ROOT)

def init_db(request):

	if (not request.user.is_authenticated()) or (not request.user.is_superuser):
		return redirect(LOGIN_ROOT)

	frp.init_db()

	return redirect(SITE_ROOT)

def randomly_populate_datamodel(request):

	if (not request.user.is_authenticated()) or (not request.user.is_superuser):
		return redirect(LOGIN_ROOT)

	frp.randomly_populate_datamodel()
	return redirect(SITE_ROOT)

def get(request):

	print(settings.MEDIA_ROOT)

	if not request.user.is_authenticated():
		return redirect(LOGIN_ROOT)

	user = request.user
	user_name = user.username

	sites = []
	for site in Site.objects.filter(users=user.id):
		sites.append(site)

	data = {
		'user_name' : user_name,
		'sites' : sites
	}

	template = loader.get_template('sites.html')
	context = RequestContext(request, data)
	return HttpResponse(template.render(context))