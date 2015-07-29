from django.http import HttpResponse
from django.template import RequestContext, loader

from server.models import Site

from sitemodels.frp import render_data_model

def routing(request):

	site_id = None
	if 'id' in request.GET.keys():
		site_id = request.GET['id']
		site = Site.objects.get(id=site_id)
		if site.update is False:
			site.update = True
			site.save()

	user_name = 'not authed'
	sites = []

	user = None
	if request.user.is_authenticated():

		user = request.user
		user_name = user.username

		for site in Site.objects.filter(users=user.id):
			sites.append(site)

	data = {
		'user_name' : user_name,
		'sites' : sites
	}

	render_data_model()

	template = loader.get_template('sites.html')
	context = RequestContext(request, data)
	return HttpResponse(template.render(context))