from django.shortcuts import render, redirect
from django.urls import reverse
from .queries import fetch_favorites, fetch_favorite_details, add_to_favorites, create_new_favorite_list, fetch_tipe, remove_from_favorites, add_tayangan_to_favorite,remove_from_list_favorite
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

def film_favorit(request):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    username = request.COOKIES['username']
    data_favorit = fetch_favorites(username)
    return render(request, 'favorit.html', {'data_favorit': data_favorit})

def favorite_details_view(request,nama_fav):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    username = request.COOKIES['username']
    favorite_details = fetch_favorite_details(username,nama_fav)

    print(favorite_details)
    context = {
        "data_favorit" : favorite_details,
        "nama_fav":nama_fav
    }
    return render(request, 'favorite_details.html', context)

def favorite_details_to_tayangan(request,judul):
    tipe_judul = fetch_tipe(judul)
    print(tipe_judul[0])

    # INI TOLONG DI UNCOMMENT YAAA BOYY
    # if tipe_judul[1] == "Series":
    #     return redirect(reverse('tayangan:series',kwargs={'id_series': tipe_judul[0]}))
    # else:
    #     return redirect(reverse('tayangan:film',kwargs={'id_film': tipe_judul[0]}))
    

@csrf_exempt
def add_to_favorites_view(request):
    if request.method == 'POST':
        if 'username' not in request.COOKIES:
            return redirect(reverse('authentication:login'))
        username = request.COOKIES['username']
        tayangan_id = request.POST.get('tayangan_id')
        favorite_list_name = request.POST.get('favorite_list_name')
        if not tayangan_id or not favorite_list_name:
            return redirect(reverse('daftar_favorit:film_favorit'))
        try:
            add_to_favorites(username, favorite_list_name)
            add_tayangan_to_favorite(tayangan_id, username, favorite_list_name)
        except Exception as e:
            print(f"Error adding to favorites: {e}")
        return redirect(reverse('daftar_favorit:film_favorit'))

@csrf_exempt
def create_favorite_list_view(request):
    if request.method == 'POST':
        if 'username' not in request.COOKIES:
            return redirect(reverse('authentication:login'))
        username = request.COOKIES['username']
        favorite_list_name = request.POST.get('favorite_list_name')
        if not favorite_list_name:
            return redirect(reverse('daftar_favorit:film_favorit'))
        try:
            create_new_favorite_list(username, favorite_list_name)
        except Exception as e:
            print(f"Error creating new favorite list: {e}")
        return redirect(reverse('daftar_favorit:film_favorit'))

@csrf_exempt
def remove_from_favorites_view(request):
    if request.method == 'POST':
        if 'username' not in request.COOKIES:
            return redirect(reverse('authentication:login'))
        username = request.COOKIES['username']
        tayangan_id = request.POST.get('tayangan_id')
        if not tayangan_id:
            return redirect(reverse('daftar_favorit:film_favorit'))
        try:
            remove_from_favorites(username, tayangan_id)
        except Exception as e:
            print(f"Error removing from favorites: {e}")
        return redirect(reverse('daftar_favorit:film_favorit'))
    
@csrf_exempt
def remove_from_list_favorite_view(request):
    if request.method == 'POST':
        if 'username' not in request.COOKIES:
            return redirect(reverse('authentication:login'))
        username = request.COOKIES['username']
        tayangan_id = request.POST.get('tayangan_id')
        nama_fav = request.POST.get('nama_fav')
        if not tayangan_id:
            return redirect(reverse('daftar_favorit:favorite_details',kwargs={'nama_fav':nama_fav}))
        try:
            remove_from_list_favorite(username, tayangan_id)
        except Exception as e:
            print(f"Error removing from favorites: {e}")
        return redirect(reverse('daftar_favorit:favorite_details',kwargs={'nama_fav':nama_fav}))

