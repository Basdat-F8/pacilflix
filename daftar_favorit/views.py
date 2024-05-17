from django.shortcuts import render, redirect
from django.urls import reverse
from .queries import fetch_favorites, fetch_favorite_details, add_to_favorites, create_new_favorite_list, fetch_favorite_lists, remove_from_favorites, remove_tayangan_from_favorites
from django.views.decorators.csrf import csrf_exempt

def film_favorit(request):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    username = request.COOKIES['username']
    data_favorit = fetch_favorites(username)
    return render(request, 'favorit.html', {'data_favorit': data_favorit})

def favorite_details_view(request, judul_favorit):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    username = request.COOKIES['username']
    favorite_list_details = fetch_favorite_details(username, judul_favorit)
    if not favorite_list_details:
        return redirect(reverse('daftar_favorit:film_favorit'))
    context = {
        'judul_favorit': judul_favorit,
        'favorite_list_details': favorite_list_details
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
        judul = request.POST.get('judul')
        if not judul:
            return redirect(reverse('daftar_favorit:film_favorit'))
        try:
            remove_from_favorites(username, judul)
        except Exception as e:
            print(f"Error removing from favorites: {e}")
        return redirect(reverse('daftar_favorit:film_favorit'))

@csrf_exempt
def remove_tayangan_from_favorite_view(request):
    if request.method == 'POST':
        if 'username' not in request.COOKIES:
            return redirect(reverse('authentication:login'))
        username = request.COOKIES['username']
        judul_favorit = request.POST.get('judul_favorit')
        judul_tayangan = request.POST.get('judul_tayangan')
        if not judul_favorit or not judul_tayangan:
            return redirect(reverse('daftar_favorit:favorite_details', kwargs={'judul_favorit': judul_favorit}))
        try:
            remove_tayangan_from_favorites(username, judul_favorit, judul_tayangan)
        except Exception as e:
            print(f"Error removing tayangan from favorites: {e}")
        return redirect(reverse('daftar_favorit:favorite_details', kwargs={'judul_favorit': judul_favorit}))

def get_favorite_lists(request):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    username = request.COOKIES['username']
    favorite_lists = fetch_favorite_lists(username)
    return render(request, 'favorite_lists.html', {'favorite_lists': favorite_lists})
