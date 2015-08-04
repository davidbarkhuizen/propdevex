from django.shortcuts import redirect

def redirect_if_user_not_authed(url):

	def redirects_if_user_not_authed(f):

		def wrap(request, params = None):

			if not request.user.is_authenticated():
				return redirect(url)

			return f(request, params)

		return wrap

	return redirects_if_user_not_authed

def redirect_if_user_not_super(url):

	def redirects_if_user_not_super(f):

		def wrap(request, params = None):

			if not request.user.is_superuser:
				return redirect(url)

			return f(request, params)

		return wrap

	return redirects_if_user_not_super

def redirect_on_missing_parameter(parameter_names, url):

	def redirects_on_missing_parameter(f):

		def wrap(request, params = None):

			for param_name in parameter_names:
				if param_name not in request.GET.keys():
					return redirect(url)	

			return f(request, params)

		return wrap

	return redirects_on_missing_parameter