from django.contrib import admin

# Register your models here.
from .models import Game, Photo

admin.site.register(Game)

admin.site.register(Photo)