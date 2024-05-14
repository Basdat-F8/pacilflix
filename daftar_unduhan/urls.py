from django.urls import path
from daftar_unduhan.views import film_unduhan

app_name = 'daftar_unduhan'

urlpatterns = [
    path('unduhan/', film_unduhan, name='unduhan'),
]