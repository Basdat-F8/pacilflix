from django.shortcuts import render, redirect
from django.urls import reverse

def trailer(request):
    return render(request, 'trailer.html')

def tayangan(request):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    return render(request, 'tayangan.html')

def halaman_film(request):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    return render(request, 'film.html')

def halaman_series(request):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    return render(request, 'series.html')

def halaman_episode(request):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    return render(request, 'episode.html')

def pencarian_trailer(request):
    return render(request, 'pencarian_trailer.html')

def pencarian_tayangan(request):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    return render(request, 'pencarian_tayangan.html')
