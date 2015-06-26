from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Category, Page
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm


def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            # user = user_form.save() # directly save the raw password
            # user.set_password(user.password) # hash it
            # user.save()
            user = User.objects.create_user(request.POST.get("username"), request.POST.get("email"),
                                            request.POST.get("password"))
            profile = profile_form.save(commit=False)
            profile.user = user
            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]
            profile.save()
            registered = True
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, "rango/register.html",
                  {"user_form": user_form, "profile_form": profile_form, "registered": registered})


def user_login(request):
    if request.user:
        return HttpResponseRedirect("/rango")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/rango")
            else:
                return HttpResponse("Your account is disabled!")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, "rango/login.html")


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


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()  # By default: commit
            return index(request)
    else:
        form = CategoryForm()
    return render(request, "rango/add_category.html", {"form": form})


def add_page(request, category_name_slug):
    cat = get_object_or_404(Category, slug=category_name_slug)
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = cat
            page.save()
            return category(request, category_name_slug)
    else:
        form = PageForm()
    context = {"form": form, "category": cat}
    return render(request, "rango/add_page.html", context)
