from django.urls import path
from .views import film_unduhan, hapus_unduhan_view, add_unduhan

app_name = 'daftar_unduhan'

urlpatterns = [
    path('unduhan/', film_unduhan, name='unduhan'),
    path('hapus_unduhan/', hapus_unduhan_view, name='hapus_unduhan'),
    path('tambah_unduhan/', add_unduhan, name='add_unduhan'),
]
