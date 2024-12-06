from django.shortcuts import render
from . import util
import markdown




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Function that renders the page for each entry
def entry(request, title):
    content = util.get_entry(title)
    if content:
        html_content = markdown.markdown(content)
        return render(request, 'encyclopedia/entry.html', {
            'title': title, 
            'content': html_content
        })
    # If entry does not exist, render custom 404 error page
    return render(request, 'encyclopedia/404.html', {
        'title': title.capitalize()
    })
