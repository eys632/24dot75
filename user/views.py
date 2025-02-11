# user/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages

def index(request):
    if request.user.is_authenticated:
        return redirect('board:chat')
    else:
        return redirect('user:login')

def login(request):
    if request.user.is_authenticated:
        return redirect('board:chat')
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('board:chat')
        else:
            messages.error(request, "로그인 정보가 올바르지 않습니다.")
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

def signup(request):
    if request.user.is_authenticated:
        return redirect('board:chat')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "회원가입이 완료되었습니다. 로그인 해주세요.")
            return redirect('user:login')
    else:
        form = UserCreationForm()
    return render(request, 'user/signup.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('user:login')

def admin_request_view(request):
    if request.method == 'POST':
        messages.success(request, "관리자 권한 요청이 제출되었습니다.")
        return redirect('user:index')
    return render(request, 'user/admin_request.html')
