from django.urls import path
from tayangan.views import *

app_name = 'tayangan'

urlpatterns = [
    path('trailer/', trailer, name='trailer'),
    path('tayangan/', tayangan, name='tayangan'),
    path('film/<uuid:id_film>', halaman_film, name='film'),
    path('series/<uuid:id_series>', halaman_series, name='series'),
    path('series/episode/', halaman_episode, name='episode'),
    path('trailer/query/', pencarian_trailer, name='pencarian_trailer'),
    path('tayangan/query/', pencarian_tayangan, name='pencarian_tayangan'),
]