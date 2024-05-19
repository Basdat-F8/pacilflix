from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .queries import hapus_unduhan, fetch_unduhan, tambah_unduhan
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.utils import timezone

import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def hapus_unduhan_view(request):
    if request.method == 'POST':
        username = request.COOKIES.get('username')
        tayangan_id = request.POST.get('tayangan_id')
        judul = request.POST.get('judul')
        timestamp = request.POST.get('timestamp')
        messages = []
        show_modal = False

        print(f"Received timestamp: {timestamp}")

        if not username or not tayangan_id or not judul or not timestamp:
            messages.append('Username, Judul, and Timestamp are required.')
            show_modal = True
        else:
            try:
                added_time = datetime.strptime(timestamp, "%B %d, %Y, %I:%M %p")
                added_time = timezone.make_aware(added_time, timezone.get_current_timezone())
                current_time = timezone.now()

                print(f"Current time: {current_time}, Added time: {added_time}")

                if current_time - added_time > timedelta(days=1):
                    hapus_unduhan(username, tayangan_id)
                    return redirect(reverse('daftar_unduhan:unduhan'))
                else:
                    messages.append('GAGAL MENGHAPUS TAYANGAN DARI DAFTAR UNDUHAN\n\nTayangan minimal harus berada di daftar unduhan selama 1 hari agar bisa dihapus.')
                    show_modal = True
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

@csrf_exempt
def add_unduhan(request):
    if request.method == 'POST':
        username = request.COOKIES.get('username')
        tayangan_id = request.POST.get('id_tayangan')

        try:
            tambah_unduhan(username, tayangan_id)
            return redirect(reverse('daftar_unduhan:show_daftar_unduhan'))
        except Exception as e:
            # Handle error accordingly
            print(f"Error: {e}")
            return render(request, 'error_page.html', {'error': str(e)})
    return redirect(reverse('daftar_unduhan:show_daftar_unduhan'))