from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('create-todo/', views.create_todo, name='create-todo'),
    path('todo-detail/<id>/', views.todo_detail, name='todo-detail'),
    path('delete-todo/<id>/', views.delete_todo, name='delete-todo'),
    path('update-todo/<id>/', views.update_todo, name='update-todo'),
]
