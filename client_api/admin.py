from django.contrib import admin
from .models import Address, BankAccount, Client

admin.site.register(Address)
admin.site.register(BankAccount)
admin.site.register(Client)
