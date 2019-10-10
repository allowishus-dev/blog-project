from django import forms
from .import models


class CreateArticle(forms.ModelForm):
    class Meta:
        model = models.Article  # our own models.py
        fields = ['title', 'body', 'slug']  # from models > Article
