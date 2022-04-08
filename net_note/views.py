from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from upload.models import Content

def index(request):

    return render(request,'index.html')



