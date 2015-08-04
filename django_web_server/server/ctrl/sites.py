from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
from django.conf import settings

from fx.httpfx import redirect_if_user_not_authed, redirect_if_user_not_super, redirect_on_missing_parameter

from server.models import Site
import sitemodel.interface as site_interface

# register site interfaces here
import sitemodel.frp.interface

LOGIN_ROOT = '/admin'
SITE_ROOT = '/admin/sites'

def get_db_site_from_request(request):
	site_id = request.GET['id']
	return Site.objects.get(id=site_id)

@redirect_if_user_not_authed(LOGIN_ROOT)
@redirect_if_user_not_super(LOGIN_ROOT)
@redirect_on_missing_parameter(['token'], SITE_ROOT)
def init(request, params):

	site_token = request.GET['token']
	site_interface.init(site_token)
	site_interface.populate_model_constants(site_token)

	return redirect(SITE_ROOT)

@redirect_if_user_not_authed(LOGIN_ROOT)
@redirect_if_user_not_super(LOGIN_ROOT)
@redirect_on_missing_parameter(['token'], SITE_ROOT)
def randomly_populate_datamodel(request, params):

	site_token = request.GET['token']
	site_interface.randomly_populate_datamodel(site_token)

	return redirect(SITE_ROOT)

@redirect_if_user_not_authed(LOGIN_ROOT)
def get(request, params):

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

@redirect_if_user_not_authed(LOGIN_ROOT)
@redirect_on_missing_parameter(['id'], SITE_ROOT)
def update(request, params):

	site = get_db_site_from_request(request)

	# do not interfere with an in-progress update
	#
	if site.update is True:
		pass
	else:
		site_interface.update(site.token)
		site.update = True
		site.save()

	return redirect(SITE_ROOT)