from django.shortcuts import render

# Create your views here.
def template(request):
    return render(request, 'trashsite/template.html')

def index(request):
    return render(request, 'trashsite/index.html')

def about(request):
    return render(request, 'trashsite/about.html')

def register(request):
    return render(request, 'trashsite/register.html')

def login(request):
    return render(request, 'trashsite/login.html')

def map(request):
    return render(request, 'trashsite/map.html')

def imageapprove(request):
    return render(request, 'trashsite/imageapprove.html')

def mapselect(request):
    return render(request, 'trashsite/mapselect.html')
