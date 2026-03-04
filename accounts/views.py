from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "密碼不一致！")
            return redirect('accounts:register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "使用者名稱已被註冊！")
            return redirect('accounts:register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email 已被註冊！")
            return redirect('accounts:register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.save()

        messages.success(request, "註冊成功！請登入")
        return redirect('accounts:login')

    return render(request, "accounts/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')  # 登入成功跳首頁
        else:
            messages.error(request, "帳號或密碼錯誤！")
            return redirect('accounts:login')

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect('accounts:login')
