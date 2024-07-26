from django.urls import path
from tasks.api import views

app_name = "tasks"

urlpatterns = [
    path("", views.TaskView.as_view(), name="tasks"),
    path("<pk>/", views.RetrieveTaskView.as_view(), name="task_detail"),
    path("statuses", views.TaskStatusesView.as_view(), name="task-status"),
    path(
        "<pk>/change-status", views.ChangeStatusesView.as_view(), name="change-status"
    ),
    path(
        "<pk>/planned-spare-part",
        views.UpdatePlannedSparePartView.as_view(),
        name="change-status",
    ),
]
