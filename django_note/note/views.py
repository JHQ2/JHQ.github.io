from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Note
# Create your views here.

def check_login(fn):
    def wrap(request,*args,**kwargs):
        if 'uname' not in request.session:
            c_uname = request.COOKIES.get('uname')
            c_uid = request.COOKIES.get('uid')
            if not c_uname or not c_uid:
                return HttpResponseRedirect('/user/login')
            else:
                request.session['uname'] = c_uname
                request.session['uid'] = c_uid
        return fn(request,*args,**kwargs)
    return wrap

@check_login
def all_note(request,uid):
    allnote = Note.objects.filter(user_id=uid)
    return render(request,'note/all_note.html',locals())

@check_login
def add_note(request):
    if request.method == 'GET':
        return render(request,'note\add_note.html')
    elif request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        uid = request.session['uid']
        Note.objects.create(title=title,content=content,user_id=uid)
        return HttpResponseRedirect(f'/note/all/{uid}')

def note_content(request,note_id):
    note = Note.objects.get(id=note_id)
    return HttpResponse(note.content)

def update_note(request,note_id):
    uid = request.session['uid']
    if request.method == 'GET':
        note = Note.objects.get(id=note_id)
        return render(request,'note/update.html',locals())
    elif request.method == 'POST':
        new_content = request.POST['content']
        note = Note.objects.get(id=note_id)
        note.content = new_content
        note.save()
        return HttpResponseRedirect(f'/note/all/{uid}')

def delete_note(request,note_id):
    uid = request.session['uid']
    note = Note.objects.get(id=note_id)
    note.delete()
    return HttpResponseRedirect(f'/note/all/{uid}')