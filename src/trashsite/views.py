from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'trashsite/index.html')

def map(request):
    return render(request, 'trashsite/map.html')
