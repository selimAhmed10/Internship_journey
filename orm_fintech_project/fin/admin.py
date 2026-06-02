from django.contrib import admin
from .models import User, Account, Card, Merchant, Transaction

admin.site.register(User)
admin.site.register(Account)
admin.site.register(Card)
admin.site.register(Merchant)
admin.site.register(Transaction)
