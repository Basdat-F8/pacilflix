from django.urls import path
from langganan.views import langganan, premiumbuy, basicbuy, standardbuy

app_name = 'langganan'

urlpatterns = [
    path('langganan/', langganan, name='langganan'),
    path('langganan/premiumbuy/', premiumbuy, name='premiumbuy'),
    path('langganan/basicbuy/', basicbuy, name='basicbuy'),
    path('langganan/standardbuy/', standardbuy, name='standardbuy'),
]