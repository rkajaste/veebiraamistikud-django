from django.urls import path

from . import views

urlpatterns = [
    path('', views.allPosts, name='index'),
    path('details/<int:id>', views.postDetails, name='details'),
    path('delete/<int:id>', views.removePost, name='remove'),
    path('edit/<int:id>', views.editPost, name='edit'),
    path('add', views.addPost, name='add')
]