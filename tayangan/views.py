from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from tayangan.queries import *

def trailer(request):
    # mengambil film list dari queries.py
    films = get_film_list()
    films_data = []

    series = get_series_list()
    series_data = []

    for film in films:
        films_data.append({
            'judul': film[1],
            'sinopsis': film[2],
            'url_video_trailer': film[3],
            'release_date_trailer': film[4]
        })

    for seri in series:
        series_data.append({
            'judul': seri[1],
            'sinopsis': seri[2],
            'url_video_trailer': seri[3],
            'release_date_trailer': seri[4]
        })

    context = {
        'films': films_data,
        'series': series_data
    }
    return render(request, 'trailer.html', context)

def tayangan(request):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    films = get_film_list()
    films_data = []

    series = get_series_list()
    series_data = []

    for film in films:
        films_data.append({
            'id_film' : film[0],
            'judul': film[1],
            'sinopsis': film[2],
            'url_video_trailer': film[3],
            'release_date_trailer': film[4]
        })

    for seri in series:
        series_data.append({
            'id_series' : seri[0],
            'judul': seri[1],
            'sinopsis': seri[2],
            'url_video_trailer': seri[3],
            'release_date_trailer': seri[4]
        })

    # print(films)

    context = {
        'films': films_data,
        'series': series_data
    }
    # print(films)
    # print(series)

    # return render(request, 'tayangan.html')
    return render(request, 'tayangan.html', context)

def halaman_film(request, id_film):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    
    if request.method == 'POST':
        deskripsi = request.POST.get('deskripsiUlasan')
        rating = request.POST.get('ratingUlasan')
        username = request.COOKIES.get('username')
        
        if deskripsi and rating and username:
            add_ulasan(id_film, username, rating, deskripsi)
            return redirect(reverse('tayangan:film', args=[id_film]))
            
    film = get_film_by_id(id_film)

    ratings = get_rating(id_film)
    rating_avg = 0

    if len(ratings) > 0:
        rating_sum = 0
        for rating in ratings:
            rating_sum += rating[0]
        rating_avg = rating_sum / len(ratings)
    rating_avg = round(rating_avg, 2)
    
    pemain_data = [aktor[0] for aktor in get_pemain_list(id_film)]
    penulis_skenario_data = [penulis_skenario[0] for penulis_skenario in get_penulis_skenario_list(id_film)]
    genre = [g[0] for g in get_genre(id_film)]
        
    ulasan = get_ulasan(id_film)
    ulasan_data = []
    for u in ulasan:
        ulasan_data.append({
            'nama': u[0],
            'rating': u[1],
            'deskripsi': u[2]
        })    
        
    # print(ulasan_data)
# judul
# total view
# rating rata2
# synopsis
# durasifilm
# tanggal rilis film
# url film
# genre
# asal negara
# pemain
# penulis scenario
# sutradara

    film_data = {
        'id_film': id_film,
        'judul': film[1],
        'sinopsis': film[2],
        'url_video_film': film[3],
        'release_date_film': film[4],
        'asal_negara': film[5],
        'id_sutradara': film[6],
        'durasi_film': film[7],
        'rating_avg': rating_avg,
        'sutradara': get_sutradara(film[6]),
        'pemain': pemain_data,
        'penulis_skenario': penulis_skenario_data,
        'ulasan': ulasan_data,
        'genre': genre
        # genre blm
        # total view
    }
    
    context = {
        'film': film_data
    }
    return render(request, 'film.html', context)

def halaman_series(request, id_series):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    if request.method == 'POST':
        deskripsi = request.POST.get('deskripsiUlasan')
        rating = request.POST.get('ratingUlasan')
        username = request.COOKIES.get('username')
        
        if deskripsi and rating and username:
            add_ulasan(id_series, username, rating, deskripsi)
            return redirect(reverse('tayangan:series', args=[id_series]))
    
    serial = get_series_by_id(id_series)
    ratings = get_rating(id_series)
    rating_avg = 0
        
    if len(ratings) > 0:
        rating_sum = 0
        for rating in ratings:
            rating_sum += rating[0]
        rating_avg = rating_sum / len(ratings)
    rating_avg = round(rating_avg, 2)
        
    ulasan = get_ulasan(id_series)
    ulasan_data = []
    for u in ulasan:
        ulasan_data.append({
            'nama': u[0],
            'rating': u[1],
            'deskripsi': u[2],
        })  
        
    pemain_data = [aktor[0] for aktor in get_pemain_list(id_series)]
    penulis_skenario_data = [penulis_skenario[0] for penulis_skenario in get_penulis_skenario_list(id_series)]
    genre = [g[0] for g in get_genre(id_series)]
    
    print(genre)

    
    series_data = {
        'judul': serial[1],
        'sinopsis': serial[2],
        'asal_negara': serial[3],
        'id_sutradara': serial[4],
        'rating_avg': rating_avg,
        'sutradara': get_sutradara(serial[4]),
        'pemain': pemain_data,
        'penulis_skenario': penulis_skenario_data,
        'ulasan': ulasan_data,
        'genre': genre
    }
    
    return render(request, 'series.html', {'series': series_data})

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
