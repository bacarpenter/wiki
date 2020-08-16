from django.shortcuts import render
# Taken from lecture code, tasks/views.py
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse  # Taken from lecture code, tasks/views.py
from . import util
import random as ran
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    entry = util.get_entry(title)

    if entry == None:
        return render(request, "encyclopedia/noEntry.html", {
            "title": title,
        })

    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(),
            "entry": markdown2.markdown(util.get_entry(title))
        })


def search(request):
    query = request.GET['q']
    entries = util.list_entries()
    pos = []

    for e in entries:
        if query.lower() == e.lower():
            return HttpResponseRedirect(f"wiki/{query}")

        elif query.lower() in e.lower():
            pos.append(e)

        # help with 'in' from https://www.afternerd.com/blog/python-string-contains/ and from my own CS50x code, for 'homepage'. Please include it's included citations.

    # If no match found
    print(pos)
    return render(request, "encyclopedia/search.html", {
        "pos": pos
    })


def new_entry(request):
    if request.method == "POST":

        title = request.POST['t']
        content = request.POST['c']
        print(util.get_entry(title))

        # Insure the title is distinct:
        if util.get_entry(title) != None:
            return render(request, "encyclopedia/badTitle.html", {
                "title": title
            })

        # Save entry to disk:
        util.save_entry(title, content)

        # Redirect user to new page:
        return HttpResponseRedirect(f'/wiki/{title}')

    else:
        return render(request, "encyclopedia/newEntry.html")


def edit(request, title):
    content = util.get_entry(title)
    if request.method == 'POST':
        # Update the entry with new content:
        util.save_entry(title, request.POST['c'])

        # Redirect user:
        return HttpResponseRedirect(f"/wiki/{title}")

    else:
        if content != None:
            return render(request, 'encyclopedia/edit.html', {
                "orgContent": content
            })
        else:
            return render(request, "encyclopedia/noEntry.html", {
                "title": title
            })


def random(request):
    #   Help with random (imported as ran) from https://docs.python.org/3/library/random.html
    entries = util.list_entries()
    num = ran.randint(0, (len(entries) - 1))
    return HttpResponseRedirect(f"/wiki/{entries[num]}")
