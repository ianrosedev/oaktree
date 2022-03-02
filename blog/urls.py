from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("new/", views.PostCreateView.as_view(), name="post_create"),
    path("edit/<slug:slug>/", views.PostUpdateView.as_view(), name="post_update"),
    path("delete/<slug:slug>/", views.PostDeleteView.as_view(), name="post_delete"),
    path("<slug:slug>/", views.PostDetailView.as_view(), name="post"),
]
