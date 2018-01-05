from django.contrib import admin


from .models import Stock, OwnedStock, Trader

admin.site.register(Stock)
admin.site.register(OwnedStock)
admin.site.register(Trader)

