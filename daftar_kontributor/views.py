from django.shortcuts import render, redirect
from django.urls import reverse
from .queries import contributors,sutradara,pemain,penulis
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

def getcontributors(request):
    # mengambil film list dari queries.py
    contributor = contributors()
    contributor_list = []

    for contributora in contributor:
        contributor_list.append({
            'nama': contributora[0],
            'type': contributora[1],
            'jenis_kelamin': contributora[2],
            'kewarganegaraan': contributora[3]
        })

    context = {
        'list': contributor_list,
    }
    return render(request, 'contributors.html', context)

def getsutradara(request):
    # mengambil film list dari queries.py
    sutradaras = sutradara()
    sutradara_list = []

    for contributora in sutradaras:
        sutradara_list.append({
            'nama': contributora[0],
            'type': contributora[1],
            'jenis_kelamin': contributora[2],
            'kewarganegaraan': contributora[3]
        })

    context = {
        'list': sutradara_list,
    }
    return render(request, 'sutradara.html', context)

def getpenulis(request):
    # mengambil film list dari queries.py
    contributor = penulis()
    contributor_list = []

    for contributora in contributor:
        contributor_list.append({
            'nama': contributora[0],
            'type': contributora[1],
            'jenis_kelamin': contributora[2],
            'kewarganegaraan': contributora[3]
        })

    context = {
        'list': contributor_list,
    }
    return render(request, 'penulis.html', context)

def getpemain(request):
    # mengambil film list dari queries.py
    contributor = pemain()
    contributor_list = []

    for contributora in contributor:
        contributor_list.append({
            'nama': contributora[0],
            'type': contributora[1],
            'jenis_kelamin': contributora[2],
            'kewarganegaraan': contributora[3]
        })

    context = {
        'list': contributor_list,
    }
    return render(request, 'pemain.html', context)