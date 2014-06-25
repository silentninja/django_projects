from django.contrib import admin
from list.models import Category, Anime, CategoryToAnime, AnimeList

admin.site.register(Category)
admin.site.register(Anime)
admin.site.register(CategoryToAnime)
admin.site.register(AnimeList)