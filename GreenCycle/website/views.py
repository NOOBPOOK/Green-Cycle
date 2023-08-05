from django.shortcuts import render, HttpResponse

def home(request):
    return HttpResponse("This is my home page")

def paper(request):
    return HttpResponse("This is my paper")

def clothes(request):
    return HttpResponse("This is my colthes")

def plastic(request):
    return HttpResponse("This is my plastic")

def ewaste(request):
    return HttpResponse("This is my ewaste")

def metal(request):
    return HttpResponse("This is my metal")

def glass(request):
    return HttpResponse("This is my ewaste")

# Create your views here.
