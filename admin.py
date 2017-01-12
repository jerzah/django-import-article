from django.contrib import admin

from .models import Article, Domain

admin.site.register(Article)
admin.site.register(Domain)
