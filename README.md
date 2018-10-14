# CRUD blog-type app written in Django

## Installation guide

1. Install Python 3.x: https://www.python.org/downloads/

2. Install pip: https://pip.pypa.io/en/stable/installing/ and add directory/to/Python3x/Scripts folder to PATH

3. Install virtualenv via pip: 
```
pip install virtualenv
```
4. Create a directory and navigate in to it on command line
5. Create new virtual environment in current folder:
```
virtualenv ./
```
6. Activate virtualenv:
```
source bin/activate
```
Or on Windows:
```
cd Scripts
activate
```
7. Install Django:
```
pip install Django
```
If you did everything correctly, then this command should work:
```
python -m django --version
```

## Creating a project

Create a new project using following command ("blog" being your project name, use what you want): 
```
django-admin startproject blog
```
Navigate to the project and run this command to start a development server on http://localhost:8080
```
python manage.py runserver
```
## Create a new app

Create a new app inside project folder (app name must not be same as project name!)
```
python manage.py startapp app
```

## Writing your app

Open file app/views.py and add following code in:
```

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the blog index.")

```
To call the view, we need to map it to a URL, create urls.py in app folder:
```
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```
The next step is to point the root URLconf at the app.urls module. In blog/urls.py, add an import for django.urls.include and insert an include() in the urlpatterns list:

```
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
]
```
Start the development server(if its not running already):
```
python manage.py runserver
```
http://localhost:8000 should now display the view declared in app/views.py

## Database setup

Django uses SQLite as default database. All you need to do is run this command to set it up:
```
  python manage.py migrate
```
## Creating database models for the app

Open app/models.py and add the following code:
```
from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=500)
```

To include the app in our project, we need to add a reference to it in INSTALLED_APPS at blog/settings.py.
```
INSTALLED_APPS = [
    'app.apps.AppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
Now Django knows to include the polls app, run the following commands to say to Django that you have updated your models:
```
python manage.py makemigrations app
python manage.py migrate
```

### Create database user

```
python manage.py createsuperuser
```
You can access database at http://localhost:8000/admin/ (works like PhpMyAdmin)

To make the app modifiable in the admin, add this to app/admin.py:

```
from django.contrib import admin

from .models import BlogPost

admin.site.register(BlogPost)
```

## Using templates

Create view for displaying all posts and detailed view for one post:
```
#app/views.py

from django.shortcuts import render
from django.http import HttpResponse

from .models import BlogPost

def allPosts(request):
    blog_posts = BlogPost.objects.all()
    context = {'blog_posts': blog_posts}
    return render(request, 'index.html', context)
def postDetails(request, id):
    blog_post = BlogPost.objects.get(pk=id)
    context = {'blog_post': blog_post}
    return render(request, 'index.html', context)
```
Where blog_posts holds the result of the query and context is the object that is being used for rendering at index.html

And update app/urls.py accordingly...
```
from django.urls import path

from . import views

urlpatterns = [
    path('', views.allPosts, name='allPosts'),
    path('details/<int:id>', views.postDetails, name='details'),
]
```
Create a new file: app/templates/index.html that displays all blog posts
```
{% if blog_posts %}
<div>
    <ul>
    {% for post in blog_posts %}
        <li>
          <a href="/details/{{ post.id }}">{{ post.title }}</a>
          <p>{{ post.content }}</p>
        </li>
    {% endfor %}
    </ul>
</div>
{% endif %}
```
## Using forms

Create a form model in app/forms.py (need to create by yourself):

```
from django import forms

class BlogPostForm(forms.Form):
    title = forms.CharField(label='Title', max_length=200)
    content = forms.CharField(label='Content', max_length=500)
```
Inject the form model into index.html from app/views.py:

```
...
from .forms import BlogPostForm
...
def allPosts(request):
    blog_posts = BlogPost.objects.all()
    context = {
      'blog_posts': blog_posts,
      'form': BlogPostForm
    }
    return render(request, 'index.html', context)
def addPost(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            post = BlogPost(title=title, content=content).save()
    return redirect('/')

```

Update app/templates/index.html:

```
{% if form %}
<div class="add-post">
    <form action="/add" method="POST">
        {% csrf_token %}
        {{ form }}
        <input type="submit"></submit>
    </form>
</div>
{% endif %}

{% if blog_posts %}
<div>
    <ul>
    {% for post in blog_posts %}
        <li>
          <a href="/details/{{ post.id }}">{{ post.title }}</a>
          <p>{{ post.content }}</p>
        </li>
    {% endfor %}
    </ul>
</div>
{% endif %}

```
Create post edit view by making changes in index.html:

```
#app/templates/index.html

{% if blog_post %}
<div class="blog">
    <form action="/edit/{{ blog_post.id }}" method="POST">
        {% csrf_token %}
        <input type=text name="title" value="{{ blog_post.title }}"></input>
        <textarea name="content">{{ blog_post.content }}</textarea>
        <input type="submit">Edit</input>
        <a href="/delete/{{ blog_post.id }}">Delete</a>
    </form>
</div>
{% endif %}

{% if form %}
<div class="add-post">
    <form action="/add" method="POST">
        {% csrf_token %}
        {{ form }}
        <input type="submit"></submit>
    </form>
</div>
{% endif %}

{% if blog_posts %}
<div>
    <ul>
    {% for post in blog_posts %}
        <li>
          <a href="/details/{{ post.id }}">{{ post.title }}</a>
          <p>{{ post.content }}</p>
        </li>
    {% endfor %}
    </ul>
</div>
{% endif %}

```
Update and create additional views: 

```
#app/views.py

from django.shortcuts import render, redirect

def removePost(request, id): 
    BlogPost.objects.get(pk=id).delete()
    return redirect('/')      

def editPost(request, id):
    if request.method == 'POST':
      form = BlogPostForm(request.POST)
      if form.is_valid():
          title = form.cleaned_data['title']
          content = form.cleaned_data['content']
          post = BlogPost.objects.get(pk=id)
          post.title = title
          post.content = content
          post.save()
    return redirect('/')         
```

Update urls:

```
#app/urls.py

urlpatterns = [
    path('', views.allPosts, name='index'),
    path('details/<int:id>', views.postDetails, name='detail'),
    path('delete/<int:id>', views.removePost, name='remove'),
    path('edit/<int:id>', views.editPost, name='edit'),
    path('add', views.addPost, name='add')
]
```
## Importing CSS
Now you add CSS to your HTML templates, in order to add CSS we need to add the following lines to the top of the file (index.html)
```
{% load static %}
<link rel="stylesheet" type="text/css" href="{% static 'style.css' %}">
```
For that code to work you need to create a new folder 'static' in app root folder and add a new file style.css in there
