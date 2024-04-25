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