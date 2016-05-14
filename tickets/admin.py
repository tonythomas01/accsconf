from django.contrib import admin
from .models import *


class TicketAdmin(admin.ModelAdmin):
    pass
admin.site.register(Ticket, TicketAdmin)


class AttendeeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Attendee,AttendeeAdmin)


# Register your models here.
