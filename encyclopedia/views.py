from django.shortcuts import render
from django.http import HttpResponseRedirect
from markdown2 import Markdown
from django.urls import reverse
from django.contrib import messages
from random import choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    entry = util.get_entry(title)
    if entry == None:
        return render(request, "encyclopedia/error.html", {"entry": entry})
    markdowner = Markdown()
    html_entry = markdowner.convert(entry)
    return render(request, "encyclopedia/wiki.html", {
        "html" : html_entry,
        "entry": title   
    })

def search(request):
    if request.method == "POST":
        entries = util.list_entries()
        find_entries = list()
        query = request.POST["q"]

        entry = util.get_entry(query)  # Find the query in entries
        if not entry:
            #return render(request, "encyclopedia/error.html", {"entry": query})
            for entry in entries:
                if query.upper() in entry.upper():
                    find_entries.append(entry)
        if find_entries:
            return render(request, "encyclopedia/search.html", {
                "entries": find_entries,
                "query": query}
                )
        elif not find_entries:
            return render(request, "encyclopedia/error.html", {"entry": query})         
        markdowner = Markdown()
        html_entry = markdowner.convert(entry)
        return render(request, "encyclopedia/wiki.html", {
            "entry" : html_entry
        })
    else:
        return HttpResponseRedirect(reverse("index"))
    
def new(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        if not title or not content:
            messages.error(request, "PAGE NOT SAVED: Must has TITLE and CONTENT.")
            return HttpResponseRedirect(reverse("new"))
            
        elif util.get_entry(title):
            messages.error(request, "ERROR: Page already exists.")
            return HttpResponseRedirect(reverse("new"))
        
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}")
    else:
        return render(request, "encyclopedia/new.html")

def edit(request, title):
    if request.method == "POST":
        content = request.POST["content"]

        if not content:
            messages.error(request, "PAGE NOT UPDATED: Must has CONTENT.")
            return HttpResponseRedirect(reverse("index"))
        
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}")
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {"title": title, "markdown": content})

def random(request):
    entry = choice(util.list_entries())
    return HttpResponseRedirect(f"/wiki/{entry}")
