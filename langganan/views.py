from django.shortcuts import render, redirect
from django.urls import reverse
from .queries import getcurrent, gethistory, getpacks, whatbuy, buypremium,buystandard,buybasic
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

history_list=[]

def langganan(request):
    if 'username' not in request.COOKIES:
        return redirect(reverse('authentication:login'))
    username = request.COOKIES['username']
    current=getcurrent(username)
    if current is None:
        current = ["-", 0, '-', '-', '-', '-']
    packs = getpacks()
    pack_list = []
    
    history=gethistory(username)
    

    

    current_data = {
        'username': current[0],
        'total': current[1],
        'resolusi_layar': current[2],
        'dukungan_perangkat': current[3],
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
        
        newhistory=({
            'nama_paket': histories[0],
            'start_date_time': histories[1],
            'end_date_time': histories[2],
            'metode_pembayaran': histories[3],
            'timestamp_pembayaran': histories[4],
            'total': histories[5]
        })
        if newhistory not in history_list:
            history_list.append(newhistory)

    context = {
        'aktif':current_data,
        'paket': pack_list,
        'riwayat':history_list,
    }
    return render(request, 'langganan.html', context)

@csrf_exempt
def premiumbuy(request):
    if request.method == 'POST':
        username = request.COOKIES['username']
        pembayaran = request.POST.get('pembayaran')
        buypremium(username,pembayaran)
    return redirect(reverse('langganan:langganan'))

@csrf_exempt
def standardbuy(request):
    if request.method == 'POST':
        username = request.COOKIES['username']
        pembayaran = request.POST.get('pembayaran')
        buystandard(username,pembayaran)
    return redirect(reverse('langganan:langganan'))

@csrf_exempt
def basicbuy(request):
    if request.method == 'POST':
        username = request.COOKIES['username']
        pembayaran = request.POST.get('pembayaran')
        buybasic(username,pembayaran)
    return redirect(reverse('langganan:langganan'))
    

    