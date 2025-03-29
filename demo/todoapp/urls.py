from django.urls import path

from todoapp import views

urlpatterns = [
    path("", views.partial_rendering, name="list-todo-items"),
    path("favicon.ico", views.favicon),
    path("todo-item/<int:id>", views.edit_todo_item, name="edit-todo-item"),
    path("todo-item/add", views.add_todo_item, name="add-todo-item"),
]
