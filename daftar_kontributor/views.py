from django.shortcuts import render, redirect
from django.urls import reverse

def contributors(request):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    return render(request, 'contributors.html')