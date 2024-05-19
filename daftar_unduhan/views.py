from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .queries import hapus_unduhan, fetch_unduhan
from django.views.decorators.csrf import csrf_exempt

import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def hapus_unduhan_view(request):
    if request.method == 'POST':
        username = request.COOKIES.get('username')
        tayangan_id = request.POST.get('tayangan_id')
        judul = request.POST.get('judul')
        messages = []
        show_modal = False

        if not tayangan_id:
            messages.append('Username, Judul, and Timestamp are required.')
            show_modal = True
        else:
            try:
                hapus_unduhan(username, tayangan_id)
                messages.append(f"Tayangan {judul} untuk {username} telah dihapus.")
            except Exception as e:
                messages.append('GAGAL MENGHAPUS TAYANGAN DARI DAFTAR UNDUHAN\n\nTayangan minimal harus berada di daftar unduhan selama 1 hari agar bisa dihapus.')
                show_modal = True

        if show_modal:
            data_unduhan = fetch_unduhan(username)
            return render(request, 'unduhan.html', {'messages': messages, 'show_modal': show_modal, 'data_unduhan': data_unduhan})

        return redirect(reverse('daftar_unduhan:unduhan'))

    return render(request, 'unduhan.html')


def film_unduhan(request):
    username = request.session.get('username')  
    if not username:
        return HttpResponseRedirect(reverse('authentication:login'))  

    data_unduhan = fetch_unduhan(username)
    context = {'data_unduhan': data_unduhan}
    return render(request, 'unduhan.html', context)
