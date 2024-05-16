from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .queries import hapus_unduhan, fetch_unduhan
from django.views.decorators.csrf import csrf_exempt

import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def hapus_unduhan_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        messages = []

        if not username:
            messages.append('Username is required.')

        if messages:
            return render(request, 'modal_unduhan.html', {'messages': messages})

        try:
            hapus_unduhan(username)
            messages.append(f"Tayangan untuk {username} yang sudah lebih dari 1 hari telah dihapus.")
        except Exception as e:
            messages.append('GAGAL MENGHAPUS TAYANGAN DARI DAFTAR UNDUHAN\n\nTayangan minimal harus berada di daftar unduhan selama 1 hari agar bisa dihapus.')
            return render(request, 'modal_unduhan.html', {'messages': messages, 'show_modal': True})

        return render(request, 'modal_unduhan.html', {'messages': messages})

    return render(request, 'modal_unduhan.html')

def film_unduhan(request):
    username = request.session.get('username')  # Get the logged-in user's username from the session
    if not username:
        return HttpResponseRedirect(reverse('authentication:login'))  # Redirect to login if not authenticated

    data_unduhan = fetch_unduhan(username)
    context = {'data_unduhan': data_unduhan}
    return render(request, 'unduhan.html', context)
