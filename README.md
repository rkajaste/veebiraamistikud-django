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
Run this command to start a development server on http://localhost:8080
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
    return HttpResponse("Hello, world. You're at the polls index.")

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
    path('/', include('app.urls')),
    path('admin/', admin.site.urls),
]
```
Start the development server(if its not running already):
```
python manage.py runserver
```
http://localhost:8080 should now display the view declared in app/views.py