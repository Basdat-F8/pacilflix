from django.shortcuts import render, redirect
from django.urls import reverse

def film_favorit(request):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    # Data favorit film statis
    data_favorit = [ #contoh
        {"judul": "Film A", "waktu_ditambahkan": "2024-04-27 14:30:00"},
        {"judul": "Film B", "waktu_ditambahkan": "2024-04-26 12:45:00"},
        {"judul": "Film C", "waktu_ditambahkan": "2024-04-25 10:15:00"},
    ]
    # Render template dengan data favorit film
    return render(request, 'favorit.html', {'data_favorit': data_favorit})
