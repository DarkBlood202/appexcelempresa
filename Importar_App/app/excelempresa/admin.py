from django.contrib import admin
from django.urls import path

from .models import Repartidor, Restaurante, Pedido, Envio
from .actions import *

from .views import vista_importar_repartidores, vista_importar_restaurantes, vista_importar_pedidos, vista_importar_envios
from .views import vista_definir_fecha

# Models
@admin.register(Repartidor)
class RepartidorAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display_links = ("id","nombre", "email",)
    list_display = ("id", "nombre", "email",
                    "telefono",
                    "cuenta_bancaria",
                    "direccion",
                    "provincia",
                    "poblacion",
                    "codigo_postal",
                    "nif_cif",
                    "cantidad_repartos",
                    "cantidad_transferir",
                    "precio_base",
                    "precio_extra")
    list_filter=("poblacion","provincia")
    search_fields = ['nombre', 'email', 'id', ]
    actions = [
        download_liquidacion_rp,
        enviar_liquidacion_rp,
        ]

    change_list_template = 'excelempresa/change_list_con_fecha.html'
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import/', vista_importar_repartidores),
            path('defineFecha/', vista_definir_fecha),
        ]
        return my_urls + urls


@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    ordering = ['id']
    actions = [
        download_liquidacion_rs,
        enviar_liquidacion_rs
        ]
    search_fields = ['nombre', 'email', 'id', "razon_social" ]
    list_display = ("id", "nombre", "razon_social", "email", "telefono",
                   "cuenta_bancaria",
                   "direccion",
                   "provincia",
                   "poblacion",
                   "codigo_postal",
                   "nif_cif",
                   "cantidad_pedidos",
                   "cantidad_recaudada",
                   "gastos_envio",
                   "cantidad_transferir",
                   "importe_iva",
                   "importe_sin_iva",
                   "tarifa_mensual",)

    list_filter=("poblacion","provincia")
    list_display_links = ("id", "nombre", "razon_social", "email",)
    
    change_list_template = 'excelempresa/change_list_con_fecha.html'
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import/', vista_importar_restaurantes),
            path('defineFecha/', vista_definir_fecha),
        ]
        return my_urls + urls


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    ordering = ['numero']
    list_display = (
        '__str__',
        'restaurante',
        'estado',
        "subtotal_pedido",
        "total_pedido",
        "tipo",
        "repartidor",
    )
    search_fields = ["numero", 'restaurante__nombre','restaurante__email','restaurante__id','restaurante__razon_social','repartidor__nombre','repartidor__email','repartidor__id',]
    list_display_links = ('__str__',
        'restaurante',
        )
    list_filter=("estado","restaurante", "repartidor","tipo",)
    
    change_list_template = 'excelempresa/change_list.html'
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import/', vista_importar_pedidos),
        ]
        return my_urls + urls

@admin.register(Envio)
class EnvioAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ("id",
        'pedido',
        'repartidor',
        "coste_envio",
        "distancia_metros",
    )
    search_fields = ['repartidor__nombre','repartidor__email','repartidor__id',]

    list_display_links = ("id", 'pedido',
        'repartidor',
        "coste_envio",)
    
    change_list_template = 'excelempresa/change_list.html'
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import/', vista_importar_envios),
        ]
        return my_urls + urls