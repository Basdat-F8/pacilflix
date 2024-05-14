from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def film_unduhan(request):
    # Data favorit film statis
    data_unduhan = [ #contoh
        {"judul": "Film A", "waktu_ditambahkan": "2024-04-27 14:30:00"},
        {"judul": "Film B", "waktu_ditambahkan": "2024-04-26 12:45:00"},
        {"judul": "Film C", "waktu_ditambahkan": "2024-04-25 10:15:00"},
    ]
    # Render template dengan data favorit film
    return render(request, 'unduhan.html', {'data_unduhan': data_unduhan})
