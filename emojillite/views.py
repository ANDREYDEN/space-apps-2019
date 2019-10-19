from django.shortcuts import render

def index(request):
    person = "Nigr person"
    return render(request, "index.html", {'lastname': person})