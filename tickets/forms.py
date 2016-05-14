from django import forms
from django.utils.translation import ugettext_lazy as _

class TicketBookingForm(forms.Form):
    name = forms.CharField( widget=forms.TextInput( attrs={'placeholder':_('Your Name'), 'required': True}) )
    institution = forms.CharField( widget=forms.TextInput(attrs={'placeholder':_('Your Institution'), 'required': True}))
    designation = forms.CharField( widget=forms.TextInput(attrs={'placeholder':_('Your Designation'), 'required': True}))
    email = forms.CharField( widget=forms.TextInput(attrs={'placeholder':_('Your Email'), 'required': True}))
    phone = forms.CharField( widget=forms.TextInput(attrs={'placeholder':_('Your Phone'), 'required': True}))

class AttendeeForm(forms.Form):
    name = forms.CharField( widget=forms.TextInput(attrs={'placeholder':_('Your Name'), 'required': True}))
    email = forms.CharField( widget=forms.TextInput(attrs={'placeholder':_('Your Email'), 'required': True}))
