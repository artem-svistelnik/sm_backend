from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("account.urls", namespace="auth")),
    path("api/tasks/", include("tasks.urls", namespace="tasks")),
]
