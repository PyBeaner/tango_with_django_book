from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
    if request.user.is_authenticated():
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


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/rango")


@login_required
def restricted(request):
    return HttpResponse("Hello you're logged in")


def index(request):
    # return HttpResponse("Rango says hey there world!")

    # context_dict = {'boldmessage': "I am bold font from the context"}
    # return render(request, "rango/index.html",context=context_dict)

    categories = Category.objects.all()
    context = {"categories": categories}

    reset_last_visit_time = False
    visits = int(request.COOKIES.get("visits", 1))
    if "last_visit" in request.COOKIES:
        last_visit = request.COOKIES.get("last_visit")
        # 2015-01-01 00:00:00.123456
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        # more than one day since the last visit
        if (datetime.now() - last_visit_time).seconds > 5:
            visits += 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True
        
    response = render(request, "rango/index.html", context)
    if reset_last_visit_time:
        response.set_cookie("last_visit", datetime.now())
        response.set_cookie("visits", visits)
    return response
    # return render(request, "rango/index.html", context=context)


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


def about(request):
    return render(request, 'rango/about.html', {})
