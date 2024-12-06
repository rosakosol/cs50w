import datetime
from django.shortcuts import render

# Create your views here.
def index(request):
    now = datetime.datetime.now()
    return render(request, "newyear/index.html", {
        # Check if month is January and day is 1
        "newyear": now.month == 1 and now.day == 1
    })