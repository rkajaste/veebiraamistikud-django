from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import BlogPost
from .forms import BlogPostForm

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

def postDetails(request, id):
    blog_post = BlogPost.objects.get(pk=id)
    context = {'blog_post': blog_post}
    return render(request, 'index.html', context)
