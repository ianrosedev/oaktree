from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("contact/", views.ContactPageView.as_view(), name="contact"),
]
