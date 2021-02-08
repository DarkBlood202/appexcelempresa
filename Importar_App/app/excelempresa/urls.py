from django.urls import path
from . import views

app_name = 'empresa'
urlpatterns = [
    # path('', views.index, name='index'),

    # path('upload', views.upload, name='upload'),

    path('liquidacion/repartidor/<int:id_repartidor>', views.liquidacion_rp, name='liquidacion_rp'),
    path('liquidacion/restaurante/<int:id_restaurante>', views.liquidacion_rs, name='liquidacion_rs'),
]