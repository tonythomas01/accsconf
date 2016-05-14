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
from django.views.generic import TemplateView, FormView, CreateView
from tickets.models import *
from tickets.forms import *
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.forms.formsets import BaseFormSet
from django.db import IntegrityError, transaction
from django.contrib import messages

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


def home(request):
    AttendeeFormSet = formset_factory(AttendeeForm, formset=BaseFormSet)
    ticket = Ticket()
    if request.method == 'POST':
        ticket_form = TicketBookingForm(request.POST)
        attendee_formset = AttendeeFormSet(request.POST)

        if ticket_form.is_valid() and attendee_formset.is_valid():
            # Save user info
            ticket.name = ticket_form.cleaned_data.get('name')
            ticket.institution = ticket_form.cleaned_data.get('institution')
            ticket.designation= ticket_form.cleaned_data.get('designation')
            ticket.email= ticket_form.cleaned_data.get('email')
            ticket.phone= ticket_form.cleaned_data.get('phone')
            ticket.tickets=ticket_form.cleaned_data.get('tickets')
            Ticket.save(ticket)

            # Now save the data for each form in the formset
            attendees_extra = []

            for attendee_form in attendee_formset:
                name = attendee_form.cleaned_data.get('name')
                email = attendee_form.cleaned_data.get('email')

                if name and email:
                    attendees_extra.append(Attendee(ticket=ticket.id, name=name, email=email))

            try:
                with transaction.atomic():
                    #Replace the old with the new
                    Attendee.objects.filter(ticket=Ticket.id).delete()
                    Attendee.objects.bulk_create(attendees_extra)

                    # And notify our users that it worked
                    messages.success(request, 'You have updated your profile.')

            except IntegrityError: #If the transaction failed
                messages.error(request, 'There was an error saving your profile.')
                return redirect(reverse('home'))

    else:
        ticket_form = TicketBookingForm()
        attendee_formset = AttendeeFormSet()

    context = {
        'ticket_form': ticket_form,
        'attendee_formset': attendee_formset,
    }

    return render(request, 'index.html', context)
