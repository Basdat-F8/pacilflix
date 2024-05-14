from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .queries import login, register
from django.views.decorators.csrf import csrf_exempt
import logging, psycopg2

logger = logging.getLogger(__name__)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        messages = []

        if not username or not password:
            messages.append('Username and password are required.')
        elif len(username) < 3:
            messages.append('Username is too short.')
        elif len(password) < 8:
            messages.append('Password is too short.')

        if messages:
            return render(request, 'login.html', {'messages': messages})

        user = login(username, password)
        
        if user:
            response = HttpResponseRedirect(reverse('tayangan:tayangan'))
            response.set_cookie('username', user[0])
            response.set_cookie('negara_asal', user[2])
            request.session['username'] = username
        else:
            messages.append('User not exists or incorrect password. Please try again.')
            return render(request, 'login.html', {'messages': messages})
        return response

    context = {}
    return render(request, 'login.html', context)

@csrf_exempt
def logout_user(request):
    response = HttpResponseRedirect(reverse('main:show_main'))
    request.session.flush()
    response.delete_cookie('username')
    response.delete_cookie('negara_asal')
    return response

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        negara_asal = request.POST.get('negara_asal')
        messages = []

        if not username:
            messages.append('Username are required.')
        elif len(username) < 3:
            messages.append('Username is too short.')
        if not password:
            messages.append('Password are required.')
        elif len(password) < 8:
            messages.append('Password is too short.')
        if not negara_asal:
            messages.append('Negara Asal are required.')

        if messages:
            return render(request, 'register.html', {'messages': messages})

        try:
            registration_successful = register(username, password, negara_asal)
            if registration_successful:
                return HttpResponseRedirect(reverse('authentication:login'))
        except psycopg2.errors.RaiseException as e:
            messages.append('Username already exists. Please choose another one.')
            return render(request, 'register.html', {'messages': messages})

    context = {}
    return render(request, 'register.html', context)