from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
from django.conf import settings

from server.models import Site

import sitemodel.frp.logic as frp_logic
import sitemodel.frp.model as frp_model

LOGIN_ROOT = '/admin'
SITE_ROOT = '/admin/sites'

def get_site(request):
	site_id = request.GET['id']
	return Site.objects.get(id=site_id)

def update(request):
	if (not request.user.is_authenticated()) or ('id' not in request.GET.keys()):
		return redirect(LOGIN_ROOT)
	site = get_site(request)

	if site.update is False:

		site.update_data_model()

		frp_logic.update_data_model(site)

		site.update = True
		site.save()

	return redirect(SITE_ROOT)

def init_db(request):

	if (not request.user.is_authenticated()) or (not request.user.is_superuser):
		return redirect(LOGIN_ROOT)

	frp_logic.create_site_w_users_and_categories()

	return redirect(SITE_ROOT)

def randomly_populate_datamodel(request):

	if (not request.user.is_authenticated()) or (not request.user.is_superuser):
		return redirect(LOGIN_ROOT)

	frp.randomly_populate_datamodel()
	return redirect(SITE_ROOT)

def get(request):

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