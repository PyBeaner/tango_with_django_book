from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name="category"),
    url(r'^add_category/$', views.add_category, name="add_category"),
]
