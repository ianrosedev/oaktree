from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("<uuid:pk>/", views.PostDetailView.as_view(), name="post"),
    path("new/", views.PostCreateView.as_view(), name="post_create"),
    path("edit/<uuid:pk>", views.PostUpdateView.as_view(), name="post_update"),
    path("delete/<uuid:pk>", views.PostDeleteView.as_view(), name="post_delete"),
]
