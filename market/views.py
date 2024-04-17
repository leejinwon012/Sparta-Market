from django.shortcuts import render
from .models import Post  # Post 모델을 임포트합니다.


def home(request):
    products = Post.objects.all()  # Post 모델을 사용합니다.
    return render(request, 'market.html', {'products': products})
