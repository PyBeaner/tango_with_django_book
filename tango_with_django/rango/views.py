from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from .models import Category


def index(request):
    # return HttpResponse("Rango says hey there world!")

    # context_dict = {'boldmessage': "I am bold font from the context"}
    # return render(request, "rango/index.html",context=context_dict)

    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "rango/index.html", context=context)
