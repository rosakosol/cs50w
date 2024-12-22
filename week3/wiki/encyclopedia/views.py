from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import sys
import markdown


class NewTaskForm(forms.Form):
    title = forms.CharField(
        label="Entry Title",
        required=False
    )
    edit_content = forms.CharField(
        label='Content',
        widget=forms.Textarea(attrs={
            'rows': 10,
            'cols': 80
        })
    )
        

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
    
def search(request):
    query = request.POST.get("q")
    entries = util.list_entries()
    
    # If query read
    if query:
        # If query matches entry 
        if any(query.lower() == entry.lower() for entry in entries):
            
            # Render the matching entry
            content = util.get_entry(query)
            if content:
                html_content = markdown.markdown(content)
                return render(request, 'encyclopedia/entry.html', {
                    "entries": util.list_entries(),
                    "content": html_content,
                    "title": query
                })
            
        # Otherwise if query doesn't match entry, show results page for substring
        else:
            results = []
            
            # Add entry that has substring to results
            for entry in entries:
                if query.lower() in entry.lower():
                    results.append(entry)
            
            return render(request, "encyclopedia/search.html", {
            "entries": results
            })
    else:     
        # If no query
        sys.exit("No query read.")
    
    
# Function to create a new entry page
def new(request):
    # If POST request, then use the submitted form data
    if request.method == "POST":
        # Create a form variable and save user content
        form = NewTaskForm(request.POST, initial={'title': None, 'edit_content': None})
        # If form is valid, save new entry
        if form.is_valid():
            title = form.cleaned_data["title"]
            new_content = form.cleaned_data["edit_content"]
            
            # Remove extra new lines
            new_content = "\n".join([line.lstrip() for line in new_content.splitlines() if line.strip()])
            
            # Save the new markdown file
            if util.new_entry(title, new_content) != False:
                # Redirect to updated entry page
                return HttpResponseRedirect(reverse("entry", args=[title]))
            else:
                # If entry does not exist, render custom 404 error page
                return render(request, 'encyclopedia/exist.html', {
                    'title': title.capitalize(),
                    "entries": util.list_entries(),
                })
            
        # Else if form invalid, return the submitted form
        else:
            return render(request, 'encyclopedia/new.html', {
                "entries": util.list_entries(),
                "title": title,
                "content": content,
                "form": form
            })
    # Render empty form        
    form = NewTaskForm(initial={'title': None, 'edit_content': None})
    
    return render(request, "encyclopedia/new.html", {
        "entries": util.list_entries(),
        "form": form
    })
    

# Function that allows user to edit entry
def edit(request, title):
    content = util.get_entry(title)
    if content:
        # If POST request, then use the submitted form data
        if request.method == "POST":
            # Create a form variable and save user content
            form = NewTaskForm(request.POST, initial={'title': title, 'edit_content': content})
            # If form is valid, save new entry
            if form.is_valid():
                new_content = form.cleaned_data["edit_content"]
                
                # Remove extra new lines
                new_content = "\n".join([line.lstrip() for line in new_content.splitlines() if line.strip()])
                
                util.save_entry(title, new_content)
                
                # Redirect to updated entry page
                return HttpResponseRedirect(reverse("entry", args=[title]))
                
            # Else if form invalid, return the submitted form
            else:
                return render(request, 'encyclopedia/edit.html', {
                    "entries": util.list_entries(),
                    "title": title,
                    "content": content,
                    "form": form
                })
        # Render empty form        
        form = NewTaskForm(initial={'title': title, 'edit_content': content})
        
        return render(request, "encyclopedia/edit.html", {
            "entries": util.list_entries(),
            "title": title,
            "content": content,
            "form": form
        })
            
        
    # If entry does not exist, render custom 404 error page
    return render(request, 'encyclopedia/404.html', {
        'title': title.capitalize()
    })

# Function that renders the page for each entry
def entry(request, title):
    content = util.get_entry(title)
    if content:
        html_content = markdown.markdown(content)
        return render(request, 'encyclopedia/entry.html', {
            "entries": util.list_entries(),
            "content": html_content,
            "title": title
        })
    else:
        # If entry does not exist, render custom 404 error page
        return render(request, 'encyclopedia/404.html', {
            'title': title.capitalize(),
            "entries": util.list_entries(),
        })