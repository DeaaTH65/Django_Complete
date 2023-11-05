from django.shortcuts import render, redirect
from .models import Article, ArticleSeries
from .decorators import user_is_superuser
from .forms import SeriesCreateForm, SeriesUpdateForm, ArticleCreateForm, ArticleUpdateForm


# Create your views here.
def homepage(request):
    matching_series = ArticleSeries.objects.all()

    return render(
        request=request,
        template_name='main/home.html',
        context={"objects": matching_series, "type": 'series'}
    )


def series(request, series:str):
    matching_series = Article.objects.filter(series__slug=series).all()

    return render(
        request=request,
        template_name='main/home.html',
        context={"objects": matching_series, 'type': 'article'}
    )
    
    
def article(request, series:str, article:str):
    matching_article = Article.objects.filter(series__slug=series, article_slug=article).first()

    return render(
        request=request,
        template_name='main/article.html',
        context={"object": matching_article}
    )
    
    
@user_is_superuser
def new_series(request):
    if request.method == "POST":
        form = SeriesCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("homepage")

    else:
         form = SeriesCreateForm()

    return render(
        request=request,
        template_name='main/new_record.html',
        context={
            "object": "Series",
            "form": form
            }
        )


@user_is_superuser
def new_post(request):
    if request.method == "POST":
        form = ArticleCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(f"{form.cleaned_data['series'].slug}/{form.cleaned_data.get('article_slug')}")

    else:
         form = ArticleCreateForm()

    return render(
        request=request,
        template_name='main/new_record.html',
        context={
            "object": "Article",
            "form": form
            }
        )


@user_is_superuser
def series_update(request, series):
    return redirect('/')


@user_is_superuser
def series_delete(request, series):
    return redirect('/')


@user_is_superuser
def article_update(request, series, article):
    return redirect('/')


@user_is_superuser
def article_delete(request, series, article):
    return redirect('/')