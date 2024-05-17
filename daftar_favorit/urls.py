from django.urls import path
from .views import film_favorit, favorite_details_view, add_to_favorites_view, create_favorite_list_view, remove_from_favorites_view, get_favorite_lists

app_name = 'daftar_favorit'

urlpatterns = [
    path('favorit/', film_favorit, name='film_favorit'),
    path('add/', add_to_favorites_view, name='add_to_favorites'),
    path('create/', create_favorite_list_view, name='create_favorite_list'),
    path('remove/', remove_from_favorites_view, name='remove_from_favorites'),
    path('lists/', get_favorite_lists, name='get_favorite_lists'),
    path('<int:tayangan_id>/', favorite_details_view, name='favorite_details'),
]
