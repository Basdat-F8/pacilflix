from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def trailer(request):
    return render(request, 'trailer.html')

@login_required
def tayangan(request):
    return render(request, 'tayangan.html')

@login_required
def halaman_film(request):
    return render(request, 'film.html')

@login_required
def halaman_series(request):
    return render(request, 'series.html')

@login_required
def halaman_episode(request):
    return render(request, 'episode.html')

def pencarian_trailer(request):
    return render(request, 'pencarian_trailer.html')

@login_required
def pencarian_tayangan(request):
    return render(request, 'pencarian_tayangan.html')
