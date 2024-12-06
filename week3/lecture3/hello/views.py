from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# Return a response that says Hello World
def index(request):
    return render(request, "hello/index.html")

def main(request):
    return HttpResponse("You're at the main page.")

def greet(request, name):
    return render(request, "hello/greet.html", {
        "name": name.capitalize()
    })

