from django.urls import path
from daftar_kontributor.views import getcontributors,getpenulis,getsutradara,getpemain

app_name = 'daftar_kontributor'

urlpatterns = [
    path('contributors/', getcontributors, name='contributors'),
    path('contributors/penulis/', getpenulis, name='penulis'),
    path('contributors/sutradara/', getsutradara, name='sutradara'),
    path('contributors/pemain/', getpemain, name='pemain'),

    ]