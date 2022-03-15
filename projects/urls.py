from django.urls import path
from . import views

urlpatterns = [
    path("new/", views.ProjectCreateView.as_view(), name="project_create"),
    path("edit/<slug:slug>/", views.ProjectUpdateView.as_view(), name="project_update"),
    path(
        "delete/<slug:slug>/", views.ProjectDeleteView.as_view(), name="project_delete"
    ),
    path("<slug:slug>/", views.ProjectDetailView.as_view(), name="project"),
]
