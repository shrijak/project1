from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from markdown2 import Markdown
from . import util
import re
import numpy as np


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "page": 'All Pages'
    })


def page(request, name):
    return render(request, "encyclopedia/page.html", {'title': name, 'string': Markdown().convert(util.get_entry(name))})


def search(request):
    li = []
    name = request.POST.get('q')
    if name in util.list_entries():
        return HttpResponseRedirect(reverse("enc:page", kwargs={"name": name}))
    else:
        pattern = re.compile(name.lower())
        for word in util.list_entries():
            if pattern.search(word.lower()):
                li.append(word)
        if not len(li):
            return HttpResponse("<h1>No results found</h1>")
        else:
            return render(request, "encyclopedia/index.html", {"entries": li, "page": 'Search Results'})


def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title in util.list_entries():
            return HttpResponse("<h1>Page with same title already exists!!</h1>")
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("enc:page", kwargs={"name": title}))
    else:
        return render(request, "encyclopedia/create.html")


def random(request):
    list = util.list_entries()
    num = np.random.randint(len(list))
    val = list[num]
    return HttpResponseRedirect(reverse("enc:page", kwargs={"name": val}))


def edit(request, name):
    if request.method == 'POST':
        content = request.POST.get('content')
        util.save_entry(name, content)
        return HttpResponseRedirect(reverse("enc:page", kwargs={"name": name}))
    else:
        return render(request, "encyclopedia/edit.html", {'title': name, 'content': util.get_entry(name)})
