from django.shortcuts import render, redirect
from django.urls import reverse

def langganan(request):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    return render(request, 'langganan.html')