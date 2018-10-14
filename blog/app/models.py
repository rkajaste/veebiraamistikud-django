from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=500)
