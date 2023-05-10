from django.shortcuts import render,redirect

def init(request):
    return redirect('articles:index')

def index(request):
    return render(request,'boss/index.html')