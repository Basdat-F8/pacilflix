from datetime import timedelta
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
    
    top_ten = get_top_ten()
    top_ten_data = []
    
    for i in range(10):
        if i < len(top_ten):
            top_ten_data.append({
                'id_tayangan': top_ten[i][0],
                'judul': top_ten[i][1],
                'sinopsis': top_ten[i][2],
                'url_video_trailer': top_ten[i][3],
                'release_date_trailer': top_ten[i][4],
                'jumlah_view': top_ten[i][5],
                'type': top_ten[i][6]
            })
        else:
            break

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
        'series': series_data,
        'top_ten': top_ten_data
    }
    return render(request, 'trailer.html', context)

def tayangan(request):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    
    top_ten = get_top_ten()
    top_ten_data = []
    
    films = get_film_list()
    films_data = []

    series = get_series_list()
    series_data = []
    
    # for loop 10 kali dari top_ten
    for i in range(10):
        if i < len(top_ten):
            top_ten_data.append({
                'id_tayangan': top_ten[i][0],
                'judul': top_ten[i][1],
                'sinopsis': top_ten[i][2],
                'url_video_trailer': top_ten[i][3],
                'release_date_trailer': top_ten[i][4],
                'jumlah_view': top_ten[i][5],
                'type': top_ten[i][6]
            })
        else:
            break

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

    context = {
        'films': films_data,
        'series': series_data,
        'top_ten': top_ten_data
    }
    
    return render(request, 'tayangan.html', context)

def halaman_film(request, id_film):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
            
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
    total_viewers = get_viewers_film(id_film)
            
    ulasan = get_ulasan(id_film)
    ulasan_data = []
    for u in ulasan:
        ulasan_data.append({
            'nama': u[0],
            'rating': u[1],
            'deskripsi': u[2]
        })    

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
        'genre': genre,
        'total_viewers': total_viewers[0],
    }
    
    context = {
        'film': film_data
    }
    
    if request.method == 'POST':
        if 'set_video_minute' in request.POST:
            data = request.POST.get('videoMinute')
            username = request.COOKIES.get('username')
            id_tayangan = film_data['id_film']
            durasi = film_data['durasi_film']
            if data and username and id_tayangan:
                insert_riwayat(int(data), id_tayangan, username, durasi)
                
        deskripsi = request.POST.get('deskripsiUlasan')
        rating = request.POST.get('ratingUlasan')
        username = request.COOKIES.get('username')
        
        if deskripsi and rating and username:
            error_message = add_ulasan(id_film, username, rating, deskripsi)
            if error_message == None:
                return redirect(reverse('tayangan:film', args=[id_film]))
        
    return render(request, 'film.html', context)

def halaman_series(request, id_series):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    if request.method == 'POST':
        deskripsi = request.POST.get('deskripsiUlasan')
        rating = request.POST.get('ratingUlasan')
        username = request.COOKIES.get('username')
        
        if deskripsi and rating and username:
            error_message = add_ulasan(id_series, username, rating, deskripsi)
            if error_message == None:
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
        
    episode = get_episode(id_series)
    episode_data = []
    for e in episode:
        episode_data.append({
            'id_episode': e[0],
            'judul': e[1],
        })
            
    pemain_data = [aktor[0] for aktor in get_pemain_list(id_series)]
    penulis_skenario_data = [penulis_skenario[0] for penulis_skenario in get_penulis_skenario_list(id_series)]
    genre = [g[0] for g in get_genre(id_series)]
    total_viewers = get_viewers_series(id_series)
    
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
        'genre': genre,
        'total_viewers': total_viewers[0],
        'episode': episode_data
    }
    
    return render(request, 'series.html', {'series': series_data})

def halaman_episode(request, sub_judul):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    eps_detail = get_eps_detail(sub_judul)
    
    episode = get_episode(eps_detail[6])
    episode_data = []
    for e in episode:
        if (e[1] != eps_detail[0]):
            episode_data.append({
                'id_episode': e[0],
                'judul': e[1],
            })
    
    context = {
        'sub_judul': eps_detail[0],
        'sinopsis': eps_detail[1],
        'durasi': eps_detail[2],
        'url_video': eps_detail[3],
        'release_date': eps_detail[4],
        'judul': eps_detail[5],
        'id_series': eps_detail[6],
        'episode': episode_data,
    }
    
    if request.method == 'POST':
        data = request.POST.get('videoMinute')
        username = request.COOKIES.get('username')
        id_tayangan = context['id_series']
        durasi = get_durasi_series(context['id_series'])[0]
        if data and username and id_tayangan:
            insert_riwayat(int(data), id_tayangan, username, durasi)
    
    return render(request, 'episode.html', context)

def pencarian_trailer(request):
    query = request.GET.get('query')
    result = search_tayangan(query)
    result_data = []
    for r in result:
        result_data.append({
            'id_tayangan': r[0],
            'judul': r[1],
            'sinopsis': r[4],
            'url_video_trailer': r[5],
            'release_date_trailer': r[6],
            'type': r[8]
        })
        
    context = {
        'result': result_data,
        'query': query
    }
    return render(request, 'pencarian_trailer.html', context)

def pencarian_tayangan(request):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    query = request.GET.get('query')
    result = search_tayangan(query)
    result_data = []
    for r in result:
        result_data.append({
            'id_tayangan': r[0],
            'judul': r[1],
            'sinopsis': r[4],
            'url_video_trailer': r[5],
            'release_date_trailer': r[6],
            'type': r[8]
        })
        
    context = {
        'result': result_data,
        'query': query
    }
    return render(request, 'pencarian_tayangan.html', context)

def insert_riwayat(value, id_tayangan, username, durasi):
    print(value, id_tayangan, username, durasi)
    end_time = datetime.now()
    elapsed_time = timedelta(minutes=(value / 100) * durasi)
    start_time = end_time - elapsed_time
    
    end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
    insert_riwayat_nonton(id_tayangan, username, start_time_str, end_time_str)
