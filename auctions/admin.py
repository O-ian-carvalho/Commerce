from django.contrib import admin
from .models import User, Auctions, Comments, Bids, Categories, Watchlist

# Register your models here.
admin.site.register(Categories)
admin.site.register(User)
admin.site.register(Auctions)
admin.site.register(Comments)
admin.site.register(Bids)
admin.site.register(Watchlist)
