from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,SignatureExpired
from django.conf import settings
from django.http import HttpResponse
import re

from apps.user.models import *
from celery_task import tasks
# Create your views here.


# /user/register
def register(request):
    """跳转到注册页面"""
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        # 获取参数
        user_name = request.POST.get('user_name')
        cpwd = request.POST.get('cpwd')
        pwd = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 表单验证
        if not all([user_name, cpwd, pwd, email, allow]):
            return render(request, 'register.html', {'errormsg': '请把表单填写完整'})
        if not pwd == cpwd:
            return render(request, 'register.html', {'errormsg': '两次密码不一致'})
        if allow != 'on':
            return render(request, 'register.html', {'errormsg': '请同意协议'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errormsg': '邮箱格式不正确'})
        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request, 'register.html', {'errormsg': '用户名已存在'})
        user = User.objects.create_user(user_name, email, pwd, )
        user.is_active = False
        user.save()
        return redirect(reverse('goods:index'))


# /user/register_handler
def register_handler(request):
    # 获取参数
    user_name = request.POST.get('user_name')
    cpwd = request.POST.get('cpwd')
    pwd = request.POST.get('pwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')
    # 表单验证
    if not all([user_name, cpwd, pwd, email, allow]):
        return render(request, 'register.html', {'errormsg': '请把表单填写完整'})
    if not pwd == cpwd:
        return render(request, 'register.html', {'errormsg': '两次密码不一致'})
    if allow != 'on':
        return render(request, 'register.html', {'errormsg': '请同意协议'})
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, 'register.html', {'errormsg': '邮箱格式不正确'})
    try:
        user = User.objects.get(username=user_name)
    except User.DoesNotExist:
        user = None
    if user:
        return render(request, 'register.html', {'errormsg': '用户名已存在'})
    user = User.objects.create_user(user_name, email, pwd,)
    user.is_active = False
    user.save()

    return redirect(reverse('goods:index'))


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        # 获取参数
        user_name = request.POST.get('user_name')
        cpwd = request.POST.get('cpwd')
        pwd = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 表单验证
        if not all([user_name, cpwd, pwd, email, allow]):
            return render(request, 'register.html', {'errormsg': '请把表单填写完整'})
        if not pwd == cpwd:
            return render(request, 'register.html', {'errormsg': '两次密码不一致'})
        if allow != 'on':
            return render(request, 'register.html', {'errormsg': '请同意协议'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errormsg': '邮箱格式不正确'})
        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request, 'register.html', {'errormsg': '用户名已存在'})
        user = User.objects.create_user(user_name, email, pwd, )
        user.is_active = False
        user.save()
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)
        token = token.decode()
        # subject = '注册激活'
        # message = ''
        # from_email = settings.EMAIL_FROM
        # recipient_list = [user.email]
        # html_message = '<h1>%s,欢迎您!</h1><br>激活请点击<a href="http://127.0.0.1:8000/user/active/%s">' \
        #                'http://127.0.0.1:8000/user/active/%s</a>' % (user_name, token, token)
        # # subject, message, from_email, recipient_list,
        # try:
        #     send_mail(subject, message, from_email, recipient_list, html_message=html_message)
        # except Exception as e:
        #     print(e)
        #     return HttpResponse('发送邮件失败')
        to_email = email
        username = user.username
        try:
            tasks.send_register_active_email(to_email, username, token).dely()
        except Exception as e:
            print(e)
        return redirect(reverse('goods:index'))


class ActiveView(View):
    def get(self, request, token):
        try:
            serializer = Serializer(settings.SECRET_KEY, 3600)
            info = serializer.loads(token)
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse('激活码已过期')


class LoginView(View):
    def get(self, request):
        # 返回登录页面
        return render(request, 'login.html')





