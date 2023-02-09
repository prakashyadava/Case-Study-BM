

# Register your models here.

from django.contrib import admin
from .models import Credential,Customer,contact_us,Transaction

admin.site.register(Credential)
admin.site.register(Customer)
admin.site.register(contact_us)
admin.site.register(Transaction)