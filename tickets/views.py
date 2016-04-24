from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import redirect
from accsconf import settings
from braces.views import LoginRequiredMixin, AnonymousRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.http import Http404
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic import TemplateView
from tickets.models import *


# Create your views here.
class CurrentUserMixin(object):
    model = User

    def get_object(self, *args, **kwargs):
        try: obj = super(CurrentUserMixin, self).get_object(*args, **kwargs)
        except AttributeError: obj = self.request.user
        return obj


# Create your views here
def anonymous_required(func):
    def as_view(request, *args, **kwargs):
        redirect_to = kwargs.get('next', settings.LOGIN_REDIRECT_URL )
        if request.user.is_authenticated():
            return redirect(redirect_to)
        response = func(request, *args, **kwargs)
        return response
    return as_view


class HomePageView(TemplateView):
    template_name = "index.html"
