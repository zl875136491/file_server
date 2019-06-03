from django.shortcuts import render, redirect
from .forms import UserForm
from .forms import RegisterForm
from . import models


def page404(request):
    request.session.flush()
    return render(request, 'users/404.html')


def index(request):
    if not request.session.get('is_login', None):
        # 如果未登录
        return redirect("/login/")
    elif request.session['user_type'] == 'Student':
        # 如果学生Session
        return render(request, 'users/index.html')
    elif request.session['user_type'] == 'Teacher':
        # 如果教师Session
        return render(request, 'users/teacherindex.html')
    else:
        return render(request, 'users/404.html')


def teacherindex(request):
    if not request.session.get('is_login', None):
        # 如果未登录
        return redirect("/login/")
    elif request.session['user_type'] == 'Teacher':
        return render(request, 'users/teacherindex.html')
    elif request.session['user_type'] == 'Student':
        return render(request, 'users/index.html')
    else:
        return render(request, 'users/404.html')


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
                    request.session['user_type'] = user.user_type
                    if user.user_type == 'Student':
                        return redirect('/index')
                    if user.user_type == 'Teacher':
                        return redirect('/teacherindex')
                    else:
                        message = "用户未激活，请联系管理员！"
                        request.session.flush()
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
    return redirect("/login/")


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            name = register_form.cleaned_data['name']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:
                message = "两次输入的密码不同！"
                return render(request, 'users/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(username=username)
                if same_name_user:
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'users/register.html', locals())
                # 创建新用户
                new_user = models.User.objects.create()
                new_user.username = username
                new_user.name = name
                new_user.user_pwd = password1
                new_user.user_email = email
                new_user.save()
                message = "注册成功！"
                return render(request, 'users/register.html', locals())
        else:
            message = "无效的验证码！"
            return render(request, 'users/register.html', locals())
    register_form = RegisterForm()
    return render(request, 'users/register.html', locals())

