from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Anime(models.Model):
    anime = models.CharField(max_length=200)
    category = models.ManyToManyField(Category, through='CategoryToAnime')
    user = models.ManyToManyField(User, through='AnimeList')

    def __unicode__(self):
        return self.anime


class CategoryToAnime(models.Model):
    anime = models.ForeignKey(Anime)
    category = models.ForeignKey(Category)


class AnimeList(models.Model):
    user = models.ForeignKey(User)
    anime_list = models.ForeignKey(Anime)

    class Meta:
        unique_together = ('user', 'anime_list')
