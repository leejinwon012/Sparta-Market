from django.shortcuts import redirect, render
from django.contrib.auth.models import User


def home(request):
    return redirect('products:product_list')


def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})
