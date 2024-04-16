from django.shortcuts import render

from django.shortcuts import render
from .models import Post


def home(request):
    posts = Post.objects.all()
    return render(request, 'market.html', {'posts': posts})
