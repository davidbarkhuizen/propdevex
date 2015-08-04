from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
from django.conf import settings

from server.models import Site

import sitemodel.interface as site_interface

import sitemodel.frp.logic as frp_logic
import sitemodel.frp.model as frp_model

LOGIN_ROOT = '/admin'
SITE_ROOT = '/admin/sites'

# ---------------------------------------------------------------------------------------
# TODO - move to fx

def get_site_from_request(request):

	site_id = request.GET['id']
	return Site.objects.get(id=site_id)

def redirect_to_login_if_user_not_authed():

	def redirects_to_login_if_user_not_authed(f):

		def wrap(request, params = None):

			if not request.user.is_authenticated():
				return redirect(LOGIN_ROOT))

			return f(request, params)

		return wrap

	return redirects_to_login_if_user_not_authed

def redirect_to_login_if_user_not_super():

	def redirects_to_login_if_user_not_super(f):

		def wrap(request, params = None):

			if not request.user.is_superuser():
				return redirect(LOGIN_ROOT))

			return f(request, params)

		return wrap

	return redirects_to_login_if_user_not_super

def redirect_to_site_root_on_missing_parameter(parameter_names):

	def redirects_to_site_root_on_missing_parameter(f):

		def wrap(request, params = None):

			for param_name in parameter_names:
				if param_name not in request.GET.keys():
					return redirect(SITE_ROOT)	

			return f(request, params)

		return wrap

	return redirects_to_site_root_on_missing_parameter

# ###################################################################################
# ###################################################################################

@redirect_to_login_if_user_not_authed()
@redirect_to_login_if_user_not_super()
def init(request):

	db_site = get_site_from_request()
	site_interface.init(db_site.token)

	return redirect(SITE_ROOT)

@redirect_to_login_if_user_not_authed()
@redirect_to_login_if_user_not_super()
def randomly_populate_datamodel(request):

	db_site = get_site_from_request()
	site_interface.randomly_populate_datamodel(db_site.token)

	return redirect(SITE_ROOT)

@redirect_to_login_if_user_not_authed()
def get(request):

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
	return HttpResponse(template.render(context)

@redirect_to_login_if_user_not_authed()
@redirects_to_site_root_on_missing_parameter(['id'])
def update(request):

	site = get_site(request)

	# do not interfere with an in-progress update
	#
	if site.update is True:
		pass
	else:
		site_interface.update(site.token)
		site.update = True
		site.save()

	return redirect(SITE_ROOT)