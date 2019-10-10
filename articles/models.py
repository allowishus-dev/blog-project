from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete='Article', default=None)

    def snippet(self):
        return self.body[:50]+'...'  # get 50 first characters

    def __str__(self):  # text in data table rows
        return self.title
