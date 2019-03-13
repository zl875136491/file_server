from django.shortcuts import render, redirect

from .forms import UserForm
from .forms import RegisterForm
from . import models


def index(request):
    pass
    return render(request, 'users/index.html')


def index(request):
    pass
    return render(request, 'users/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(username=username)
                if user.user_pwd == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.username
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'users/login.html', locals())

    login_form = UserForm()
    return render(request, 'users/login.html', locals())



def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    return redirect("/index/")


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            name = register_form.cleaned_data['name']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'users/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(username=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'users/register.html', locals())

                # 当一切都OK的情况下，创建新用户
                new_user = models.User.objects.create()
                new_user.username = username
                new_user.name = name
                new_user.user_pwd = password1
                new_user.user_email = email
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面

    register_form = RegisterForm()
    return render(request, 'users/register.html', locals())

