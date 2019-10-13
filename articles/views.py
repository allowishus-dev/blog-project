from django.shortcuts import render, redirect
from .models import Article
from django.shortcuts import get_object_or_404;
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseForbidden;
from django.contrib.auth.decorators import login_required
# for login
from django.contrib.auth.decorators import login_required
# for creating article form
from . import forms

# Create your views here.


def article_list(request):
    articles = Article.objects.all().order_by('date')
    return render(request, 'articles/article_list.html', {'articles': articles})


def article_detail(request, slug):
    # return HttpResponse(slug)
    article = Article.objects.get(slug=slug)
    return render(request, 'articles/article_detail.html', {'article': article})


@login_required(login_url='/loginapp/login/')
def article_create(request):
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST)
        if form.is_valid():
            # save article to db
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('articles:list')
    else:
        form = forms.CreateArticle()
    return render(request, 'articles/article_create.html', {'form': form})

@login_required(login_url='/loginapp/login/')
def article_edit(request, slug=None):
    if slug:
        article = get_object_or_404(Article, slug=slug)
        if article.author != request.user:
            return HttpResponseForbidden()
    else:
        return HttpResponseBadRequest()
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST or None, instance=article)
        if form.is_valid():
            # save article to db
            form.save()
            return redirect('articles:list')
    else:
        form = forms.CreateArticle(instance=article)
        return render(request, 'articles/article_edit.html', {'form': form, 'article': article})

@login_required(login_url='/loginapp/login/')
def article_delete(request, slug=None):
    if slug:
        article = get_object_or_404(Article, slug=slug)
        if article.author != request.user:
            return HttpResponseForbidden()
    else:
        return HttpResponseBadRequest()
    if request.method == 'POST':
        article.delete()

    return redirect('articles:list')