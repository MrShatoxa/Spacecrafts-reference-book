from django.shortcuts import render
from django.http import HttpResponse
from ReferenceBook.models import Spacecrafts, Article
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    space_crafts = Spacecrafts.objects.all()
    paginator = Paginator(space_crafts, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, поставим первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, доставить последнюю страницу результатов
        posts = paginator.page(paginator.num_pages)
    return render(request, 'index.html', { 'page': page, 'posts': posts, "page_obj": page_obj})

def info(request, spacecrafts_id):
    article = Article.objects.get(pk=spacecrafts_id)
    return render(request, 'info.html', {'article': article})

def edit(request):
    return render(request, 'edit.html')

def create(request):

    if request.method == "POST":
        spacecraft = Spacecrafts()
        spacecraft.name = request.POST.get("name")
        spacecraft.country = request.POST.get("country")
        spacecraft.manufacturer = request.POST.get("manufacturer")
        spacecraft.purpose = request.POST.get("purpose")
        spacecraft.orbit = request.POST.get("orbit")
        spacecraft.year = request.POST.get("year")
        spacecraft.save()
        #Создание объекта статьи вместе с КА и привязка ID
        article = Article()
        article.spacecrafts_id = spacecraft.id
        article.title = ""
        article.content = ""
        article.save()
    return HttpResponseRedirect("/")


def fix(request, id):
    try:
        spacecraft = Spacecrafts.objects.get(id=id)

        if request.method == "POST":

            spacecraft.name = request.POST.get("name")
            spacecraft.country = request.POST.get("country")
            spacecraft.manufacturer = request.POST.get("manufacturer")
            spacecraft.purpose = request.POST.get("purpose")
            spacecraft.orbit = request.POST.get("orbit")
            spacecraft.year = request.POST.get("year")
            spacecraft.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "fixes.html", {"spacecraft": spacecraft})
    except Spacecrafts.DoesNotExist:
        return HttpResponseNotFound("<h2>Такого обьекты нет</h2>")

def delete(request, id):
    try:
        spacecraft = Spacecrafts.objects.get(id=id)
        spacecraft.delete()
        return HttpResponseRedirect("/")
    except Spacecrafts.DoesNotExist:
        return HttpResponseNotFound("<h2>Такого объекта нет:)</h2>")


def edit_article(request, spacecrafts_id):
    try:
        article = Article.objects.get(pk=spacecrafts_id)

        if request.method == "POST":
            article.title = request.POST.get("title")
            article.content = request.POST.get("content")
            article.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "index.html", {"article": article})
    except Article.DoesNotExist:
        return HttpResponseNotFound("<h2>Статьи нет</h2>")