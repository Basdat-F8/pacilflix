from django.urls import path
from main.views import show_main, register, login_user, logout_user, film_favorit, film_unduhan, contributors,langganan, trailer, tayangan, halaman_film, halaman_series, halaman_episode, pencarian_tayangan, pencarian_trailer


app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('favorit/', film_favorit, name='favorit'),
    path('unduhan/', film_unduhan, name='unduhan'),
    path('contributors/', contributors, name='contributors'),
    path('langganan/', langganan, name='langganan'),
    path('trailer/', trailer, name='trailer'),
    path('tayangan/', tayangan, name='tayangan'),
    path('film/', halaman_film, name='film'),
    path('series/', halaman_series, name='series'),
    path('series/episode/', halaman_episode, name='episode'),
    path('trailer/query/', pencarian_trailer, name='pencarian_trailer'),
    path('tayangan/query/', pencarian_tayangan, name='pencarian_tayangan'),
]