from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Category, Page


def index(request):
    # return HttpResponse("Rango says hey there world!")

    # context_dict = {'boldmessage': "I am bold font from the context"}
    # return render(request, "rango/index.html",context=context_dict)

    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "rango/index.html", context=context)


def category(request, category_name_slug):
    category_name_slug = category_name_slug.lower()
    context = {}
    cat = get_object_or_404(Category, slug=category_name_slug)
    pages = Page.objects.filter(category=cat)
    context["pages"] = pages
    context["category"] = cat
    return render(request, "rango/category.html", context)
