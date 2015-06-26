from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.text import slugify


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    website = models.URLField()
    picture = models.ImageField(blank=True, upload_to="profile_images")

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
