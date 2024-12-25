from django.urls import path, re_path
from . import views

appname = "taskapp"

urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.register, name="register"),
    path("switch_user", views.switch_user, name="switch_user"),
    path("add_task", views.add_task, name="add_task"),
    path("view_tasks", views.view_tasks, name="view_tasks"),
    path("update_task/<int:id>/", views.update_task, name="update_task"),
    path("update_status/<int:id>/<str:old_status>/", views.update_status, name="update_status"),
    path("delete_task/<int:id>/", views.delete_task, name="delete_task"),
    path("task_history/<int:id>/", views.task_history, name="task_history"),
]