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
        user = login(username, password)
        
        if len(user) == 0:
            context = {'login_error': 'Invalid login credentials'}
            logger.debug('Invalid login credentials for username: %s', username)
            return render(request, 'login.html', context)

        logger.debug('User %s logged in successfully', username)
        response = HttpResponseRedirect(reverse('tayangan:tayangan'))
        response.set_cookie('username', user[0][0][0])
        response.set_cookie('negara_asal', user[0][0][2])
        logger.debug('Redirecting to %s', reverse('main:show_main'))
        return response

    context = {}
    return render(request, 'login.html', context)

@csrf_exempt
def logout_user(request):
    response = HttpResponseRedirect(reverse('main:show_main'))
    response.delete_cookie('username')
    response.delete_cookie('negara_asal')
    return response

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        negara_asal = request.POST.get('negara_asal')

        try:
            registration_successful = register(username, password, negara_asal)
            if registration_successful:
                return HttpResponseRedirect(reverse('authentication:login'))
        except psycopg2.errors.RaiseException as e:
            context = {'register_error': str(e)}
            return render(request, 'register.html', context)

    context = {}
    return render(request, 'register.html', context)