from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import markdown2, random
from django.contrib import messages


from . import util


def index(request):
    query = request.GET
    search = query.get("q")
    entries = list()
    for x in util.list_entries():
        entries.append(x.casefold())
    if request.GET:
        if search.casefold() in entries:
            return HttpResponseRedirect(reverse("show", args=[search]))
        else:
            matches = list()
            for i in entries:
                if search.casefold() in i:
                    matches.append(i)
            return render(request, "encyclopedia/search.html", {
            "matches": matches
    })
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def show(request, name):
    entry = util.get_entry(name)
    
    if entry == None:
        return render(request, "encyclopedia/not_found.html", {
        "name": name
    })
    else:
        convert = markdown2.markdown(entry)
        return render(request, "encyclopedia/show.html", {
        "name": name , "show": convert
    })

def new_page(request):
    page = request.GET
    title = page.get("title")
    text = page.get("text")
    entries = list()
    for x in util.list_entries():
        entries.append(x.casefold())
    if title != None:
        if title.casefold() in entries:
            messages.error(request, "Title already exists")
            return render(request, "encyclopedia/new_page.html", {"title": title, "text": text })
        else:
            util.save_entry(title, text)
            return HttpResponseRedirect(reverse("show", args=[title]))
            
    else:
        return render(request, "encyclopedia/new_page.html")

def edit(request, name):
    req = request.GET
    text = req.get("text")
    if text != None:
        util.save_entry(name, text)
        return HttpResponseRedirect(reverse("show", args=[name]))
    else:
        return render(request, "encyclopedia/edit_page.html", { "name":name, "text": util.get_entry(name) })

def random_page(request):
    entries = util.list_entries()
    if len(entries) > 0:  
        page = random.choice(entries)
        return HttpResponseRedirect(reverse("show", args=[page]))
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })