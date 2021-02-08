from django.shortcuts import redirect, reverse, render
from django.core.mail import send_mail, EmailMessage
from django.contrib import messages
from django.template.loader import get_template

from . import views
from .models import Repartidor, Restaurante, Pedido, Envio
from .models import Constants
from .functions import render_to_file
from .forms import UploadFileForm

from app.settings import EMAIL_HOST_USER


def download_liquidacion_rp(modeladmin, request, queryset):
    obj = queryset.first()
    url = reverse('empresa:liquidacion_rp', args=[obj.id]) + "?download=0"
    return(redirect(url))

download_liquidacion_rp.short_description = "Descargar hoja de liquidación"


def download_liquidacion_rs(modeladmin, request, queryset):
    obj = queryset.first()
    url = reverse('empresa:liquidacion_rs', args=[obj.id]) + "?download=0"
    return(redirect(url))

download_liquidacion_rs.short_description = "Descargar hoja de liquidación"


def enviar_liquidacion_rp(modeladmin, request, queryset):
    template_src = 'excelempresa/liquidacion_rp.html'
    template = get_template(template_src)
    for rp in queryset:
        asunto = "Hoja de liquidación de repartidor."
        mensaje = "Hola, {}. Adjuntamos su hoja de liquidación de repartidor.".format(rp.nombre)
        remitente = EMAIL_HOST_USER
        destino = [rp.email]

        e = EmailMessage(asunto, mensaje, remitente, destino)

        pp = Pedido.objects.filter(repartidor=Repartidor.objects.get(id=rp.id))
        ee = Envio.objects.filter(repartidor=Repartidor.objects.get(id=rp.id))

        try:
            fecha_inicio = Constants.objects.get(id=1).fecha_inicio
            fecha_fin = Constants.objects.get(id=1).fecha_fin
        except:
            c = Constants()
            c.save()

        importe_recaudado = 0
        cantidad_repartos = 0
        for env in ee:
            if env.pedido.fecha >= fecha_inicio and env.pedido.fecha <= fecha_fin:
                importe_recaudado += e.coste_envio
                cantidad_repartos += 1

        importe_iva = round(float(importe_recaudado) * 0.21,2)
        importe_sin_iva = round(float(importe_recaudado) - importe_iva,2)
     
        context = {'repartidor': rp, 'lista_pedidos': pp, 'lista_envios': ee,
            'importe_recaudado': importe_recaudado, 'importe_iva': importe_iva,
            'importe_sin_iva': importe_sin_iva, 'cantidad_repartos': cantidad_repartos, 
            'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}
        html = template.render(context)
        pdf = render_to_file(template_src, context)

        # /excel/liquidacion/repartidor/<int:id>?download=0
        e.attach("Hoja de liquidacion de {}.pdf".format(rp.nombre), pdf, 'application/pdf')

        e.send(fail_silently=False)

    n = queryset.count()
    msg = "{} email(s) enviados correctamente.".format(str(n))
    modeladmin.message_user(request, msg, messages.SUCCESS)

enviar_liquidacion_rp.short_description = "Enviar hoja de liquidación vía email"


def enviar_liquidacion_rs(modeladmin, request, queryset):
    template_src = 'excelempresa/liquidacion_rs.html'
    template = get_template(template_src)
    for rs in queryset:
        asunto = "Hoja de liquidación de restaurante."
        mensaje = "Adjuntamos la hoja de liquidación de su restaurante {}".format(rs.nombre)
        remitente = EMAIL_HOST_USER
        destino = [rs.email]

        e = EmailMessage(asunto, mensaje, remitente, destino)
        pp = Pedido.objects.filter(restaurante=Restaurante.objects.get(id=rs.id))
        ee = Envio.objects.all()

        er = []
        for env in ee:
            if env.pedido in pp:
                er.append(env)

        try:
            fecha_inicio = Constants.objects.get(id=1).fecha_inicio
            fecha_fin = Constants.objects.get(id=1).fecha_fin
        except:
            c = Constants()
            c.save()  

        total_recaudado = 0
        cantidad_pedidos = 0
        gastos_envio = 0
        for p in pp:
            if p.fecha >= fecha_inicio and p.fecha <= fecha_fin:
                total_recaudado += p.subtotal_pedido
                cantidad_pedidos += 1

        for envio in er:
            if envio.pedido.fecha >= fecha_inicio and envio.pedido.fecha <= fecha_fin:
                gastos_envio += (envio.coste_envio - envio.pedido.restaurante.precio_base_envio)

        importe_final = total_recaudado - gastos_envio
        importe_sin_iva = round(float(importe_final) / 1.1,2)
        importe_iva = round(float(importe_final) - importe_sin_iva,2)

        porcentaje_gastos = "{:.2%}".format(gastos_envio / total_recaudado)

        fecha_inicio = Constants.objects.get(id=1).fecha_inicio
        fecha_fin = Constants.objects.get(id=1).fecha_fin

        context = {'restaurante': rs, 'lista_pedidos': pp, 'lista_envios': er,
            'total_recaudado': total_recaudado, 'cantidad_pedidos': cantidad_pedidos,
            'gastos_envio': gastos_envio, 'importe_final': importe_final,
            'importe_sin_iva': importe_sin_iva, 'importe_iva': importe_iva,
            'porcentaje_gastos': porcentaje_gastos,
            'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}
        html = template.render(context)
        pdf = render_to_file(template_src, context)

        e.attach("Hoja de liquidacion de {}.pdf".format(rs.nombre), pdf, 'application/pdf')

        e.send(fail_silently=False)

    n = queryset.count()
    msg = "{} email(s) enviados correctamente.".format(str(n))
    modeladmin.message_user(request, msg, messages.SUCCESS)

enviar_liquidacion_rs.short_description = "Enviar hoja de liquidación vía email"