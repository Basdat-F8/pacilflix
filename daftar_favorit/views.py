from django.shortcuts import render, redirect
from django.urls import reverse
from .queries import fetch_favorites, fetch_favorite_details, add_to_favorites, create_new_favorite_list, fetch_favorite_lists, remove_from_favorites
from django.views.decorators.csrf import csrf_exempt

def film_favorit(request):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    username = request.COOKIES['username']
    data_favorit = fetch_favorites(username)
    return render(request, 'favorit.html', {'data_favorit': data_favorit})

def favorite_details_view(request, tayangan_id):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    username = request.COOKIES['username']
    favorite_details = fetch_favorite_details(username, tayangan_id)
    if not favorite_details:
        return redirect(reverse('daftar_favorit:film_favorit'))
    context = {
        'judul': favorite_details[0],
        'sinopsis': favorite_details[1],
        'waktu_ditambahkan': favorite_details[2]
    }
    return render(request, 'favorite_details.html', context)

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
            add_to_favorites(username, tayangan_id, favorite_list_name)
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

def get_favorite_lists(request):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    username = request.COOKIES['username']
    favorite_lists = fetch_favorite_lists(username)
    return render(request, 'favorite_lists.html', {'favorite_lists': favorite_lists})
