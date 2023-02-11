from django.shortcuts import render

# Create your views here.

"""
Example view that displays Hello World
"""


def dummy(request):
    return render(request, 'trashmunch/dummy.html')
