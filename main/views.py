from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout

def show_main(request):
    return render(request, "main.html")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:login')
        else:
            print(form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"- {error}")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_user(request ):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:show_main') 
        else:
            print("error")
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('main:login')

def film_favorit(request):
    # Data favorit film statis
    data_favorit = [ #contoh
        {"judul": "Film A", "waktu_ditambahkan": "2024-04-27 14:30:00"},
        {"judul": "Film B", "waktu_ditambahkan": "2024-04-26 12:45:00"},
        {"judul": "Film C", "waktu_ditambahkan": "2024-04-25 10:15:00"},
    ]
    # Render template dengan data favorit film
    return render(request, 'favorit.html', {'data_favorit': data_favorit})

def film_unduhan(request):
    # Data favorit film statis
    data_unduhan = [ #contoh
        {"judul": "Film A", "waktu_ditambahkan": "2024-04-27 14:30:00"},
        {"judul": "Film B", "waktu_ditambahkan": "2024-04-26 12:45:00"},
        {"judul": "Film C", "waktu_ditambahkan": "2024-04-25 10:15:00"},
    ]
    # Render template dengan data favorit film
    return render(request, 'unduhan.html', {'data_unduhan': data_unduhan})

def contributors(request):
    return render(request, 'contributors.html')

def langganan(request):
    return render(request, 'langganan.html')

def trailer(request):
    return render(request, 'trailer.html')

def tayangan(request):
    return render(request, 'tayangan.html')

def halaman_film(request):
    return render(request, 'film.html')

def halaman_series(request):
    return render(request, 'series.html')

def halaman_episode(request):
    return render(request, 'episode.html')

def pencarian_trailer(request):
    return render(request, 'pencarian_trailer.html')

def pencarian_tayangan(request):
    return render(request, 'pencarian_tayangan.html')