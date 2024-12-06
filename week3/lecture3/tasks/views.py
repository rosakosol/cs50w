from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")

# Create your views here.
def index(request):
    # Check if list of tasks already exists, else gen new list
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })
    
    
def add(request):
    if request.method == "POST":
        # Create a form variable and save user request
        form = NewTaskForm(request.POST)
        # If form is valid, add new task to list of tasks
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            # Else if form is not valid, return form submitted
            return render(request, "tasks/add.html", {
                "form": form
            })

            
    # Render empty form        
    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })