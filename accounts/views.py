from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('home')  # 메인 홈페이지에 연결 해야됌
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('home')  # 메인 홈페이지에 연결해야됌


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    is_following = user_profile.followers.filter(pk=request.user.pk).exists()

    if request.method == 'POST':
        if is_following:
            user_profile.followers.remove(request.user)
        else:
            user_profile.followers.add(request.user)
        return redirect('profile', username=username)
    
    # 내가 등록한 물품
    owned_items = Product.objects.filter(author=user)

    # 내가 찜한 물품들
    liked_items = user.liked_products.all()

    # 팔로우/팔로워 수
    followers_count = user_profile.followers.count()
    following_count = user.following.count()

    return render(request, 'profile.html', {
        'user': user,
        'owned_items': owned_items,
        'liked_items': liked_items,
        'followers_count': followers_count,
        'following_count': following_count,
        'user': user,
        'is_following': is_following,
    })
