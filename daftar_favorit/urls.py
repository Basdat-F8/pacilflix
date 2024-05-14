from django.urls import path
from daftar_favorit.views import film_favorit

app_name = 'daftar_favorit'

urlpatterns = [
    path('favorit/', film_favorit, name='favorit'),
]