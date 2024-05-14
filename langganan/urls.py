from django.urls import path
from langganan.views import langganan

app_name = 'langganan'

urlpatterns = [
    path('langganan/', langganan, name='langganan'),
]