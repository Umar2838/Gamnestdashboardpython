from django.shortcuts import render

def login(request):
    return render(request,'login.html')
def index(request):
    return render(request,'index.html')
def venues(request):
    return render(request,'venues.html')
def new_venue(request):
    return render(request,'new-venue.html')
def edit_venue(request):
    return render(request,'edit-venue.html')
def games(request):
    return render(request,'games.html')
def tickets(request):
    return render(request,'tickets.html')
def units(request):
    return render(request,'units.html')
def new_headset(request):
    return render(request,'new-headset.html')
def new_tablet(request):
    return render(request,'new-tablet.html')
def statistics(request):
    return render(request,'statistics.html')
def users(request):
    return render(request,'users.html')
def support(request):
    return render(request,'support.html') 
def settings(request):
    return render(request,'settings.html')

