from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def contributors(request):
    return render(request, 'contributors.html')