from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def surgical_guide(request):
    return render(request, 'surgical_guide.html')
