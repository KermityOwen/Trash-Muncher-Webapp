from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'trashsite/index.html')

def map(request):
    return render(request, 'trashsite/map.html')

def imageapprove(request):
    return render(request, 'trashsite/imageapprove.html')

def mapselect(request):
    return render(request, 'trashsite/mapselect.html')
