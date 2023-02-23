from django.shortcuts import render

# Create your views here.
def template(request):
    return render(request, 'trashsite/template.html')

def index(request):
    return render(request, 'trashsite/index.html')

def about(request):
    return render(request, 'trashsite/about.html')

def map(request):
    return render(request, 'trashsite/map.html')
