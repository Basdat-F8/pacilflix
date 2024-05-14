from django.urls import path
from daftar_kontributor.views import contributors

app_name = 'daftar_kontributor'

urlpatterns = [
    path('contributors/', contributors, name='contributors'),
]