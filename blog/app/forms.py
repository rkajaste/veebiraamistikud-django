from django import forms

class BlogPostForm(forms.Form):
    title = forms.CharField(label='Title', max_length=200)
    content = forms.CharField(label='Content', max_length=500)