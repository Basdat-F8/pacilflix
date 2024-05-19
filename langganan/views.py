from django.shortcuts import render, redirect
from django.urls import reverse
from .queries import getcurrent, gethistory, getpacks, whatbuy, buy
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

def langganan(request):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    username = request.COOKIES['username']
    current=getcurrent(username)
    packs = getpacks()
    pack_list = []
    
    history=gethistory(username)
    history_list=[]

    current_data = {
        'username': current[0],
        'total': current[1],
        'nama_paket': current[2],
        'metode_pembayaran': current[3],
        'start_date_time': current[4],
        'end_date_time': current[5],
    }
    for packages in packs:
        pack_list.append({
            'nama': packages[0],
            'harga': packages[1],
            'resolusi_layar': packages[2],
            'dukungper': packages[3]
        })

    for histories in history:
        history_list.append({
            'nama_paket': histories[0],
            'start_date_time': histories[1],
            'end_date_time': histories[2],
            'metode_pembayaran': histories[3],
            'timestamp_pembayaran': histories[4],
            'total': histories[5]
        })

    context = {
        'aktif':current_data,
        'paket': pack_list,
        'riwayat':history,
    }
    return render(request, 'langganan.html', context)