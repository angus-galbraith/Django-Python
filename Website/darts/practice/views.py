from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def rtb(request):
    return render(request, 'rtb.html')

def finishes(request):
    return render(request, 'finishes.html')