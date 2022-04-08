from logging import exception
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User
import hashlib
# Create your views here.
def reg_view(request):
    if request.method == 'GET':
        return render(request,'user/register.html')
    elif request.method == 'POST':
        userName = request.POST['username']
        passWord = request.POST['password']
        re_password = request.POST['re_password']

        old_user = User.objects.filter(username=userName)
        if passWord != re_password:
            return HttpResponse('两次密码不一致')

        m = hashlib.md5()
        m.update(passWord.encode())
        passWord_m = m.hexdigest()
        
        try:
            user = User.objects.create(username=userName,password=passWord_m)
        except :
            print('create user error')
            return HttpResponse('用户名已存在')
        
        request.session['uname'] = userName
        request.session['uid'] = user.id
        return HttpResponseRedirect('/index')

def login_view(request):
    if request.method == 'GET':
        if request.session.get('uname') and request.session.get('uid'):
            return HttpResponseRedirect('/index')
        c_username = request.COOKIES.get('uname')
        c_userid = request.COOKIES.get('uid')
        if c_username and c_userid:
            request.session['uname'] = c_username
            request.session['uid'] = c_userid
            return HttpResponseRedirect('/index')

        return render(request,'user/login.html')
    elif request.method == 'POST':
        uname = request.POST['name']
        upassword = request.POST['password']
        
        m = hashlib.md5()
        #n = hashlib.md5()
        m.update(upassword.encode())
        upassword_m = m.hexdigest()
        try:
            user = User.objects.get(username=uname)
        except:
            print('用户不存在')
  
        if upassword_m != user.password:
            return HttpResponse('用户名不存在或密码错误')
        request.session['uname'] = uname
        request.session['uid'] = user.id
        resp = HttpResponseRedirect('/index')
        
        if 'remember' in request.POST:
            resp.set_cookie('uname',uname,3600*24*3)
            resp.set_cookie('uid',user.id,3600*24*3)

        return resp

def logout(request):
    response = HttpResponseRedirect('/index')
    if request.COOKIES.get('uname'):
        response.delete_cookie('uname')
        response.delete_cookie('uid')
    if request.session:
        request.session.flush()
    return response