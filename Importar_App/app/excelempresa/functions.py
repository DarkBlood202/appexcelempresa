import openpyxl
import os, shutil

from django.core.exceptions import ObjectDoesNotExist
from .models import Repartidor, Restaurante, Pedido, Envio

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.conf import settings
from django.contrib.staticfiles import finders

def handle_uploaded_file(file,storage_path):
    with open(storage_path + file.name, 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)

def remove_uploaded_file_on(dirpath):
    for filename in os.listdir(dirpath):
        fp = os.path.join(dirpath,filename)
        try:
            if os.path.isfile(fp) or os.path.islink(fp):
                os.unlink(fp)
            elif os.path.isdir(fp):
                shutil.rmtree(fp)
        except Exception as ex:
            print("Failed to delete %s: %s"%(fp,ex))

def cells_to_dict(wksheet, entradas, campos, f_row=2, f_column=1):
    dict_rows = {}
    for i in range(entradas):
        for row in wksheet.iter_rows(min_row=i+f_row, min_col=f_column, max_col=campos+f_column-1, max_row=i+f_row, values_only=True):
            dict_rows["entrada {}".format(i+1)] = list(row)
    return dict_rows

########## FUNCIONES DE INSERCION DE DATOS A MODELOS ##########
def insertar_repartidores(num_filas, indices, llaves, data_dict):
    dict_args = {}
    for i in range(num_filas):
        for ii in indices:
            dict_args[llaves[ii]] = data_dict["entrada {}".format(i+1)][ii]
        
        rp = Repartidor(**dict_args)
        rp.save()
        dict_args.clear()

def insertar_restaurantes(num_filas, indices, llaves, data_dict):
    dict_args = {}
    for i in range(num_filas):
        for ii in indices:
            dict_args[llaves[ii]] = data_dict["entrada {}".format(i+1)][ii]
        
        rs = Restaurante(**dict_args)
        rs.save()
        dict_args.clear()

def insertar_pedidos(num_filas, indices, llaves, data_dict):
    dict_args = {}
    for i in range(num_filas):
        for ii in indices:
            if llaves[ii] == "restaurante":
                try:
                    q = Restaurante.objects.get(id=data_dict["entrada {}".format(i+1)][ii])
                except:
                    q = None
                dict_args[llaves[ii]] = q
            # elif llaves[ii] == "task_id":
            #     try:
            #         q = Envio.objects.get(task_id=data_dict["entrada {}".format(i+1)][ii])
            #     except:
            #         q = None
            elif llaves[ii] == "repartidor":
                try:
                    q = Repartidor.objects.get(id=data_dict["entrada {}".format(i+1)][ii])
                except:
                    q = None
                dict_args[llaves[ii]] = q
            else:
                dict_args[llaves[ii]] = data_dict["entrada {}".format(i+1)][ii]

        p = Pedido(**dict_args)
        p.save()
        dict_args.clear()

def insertar_envios(num_filas, indices, llaves, data_dict):
    dict_args = {}
    for i in range(num_filas):
        for ii in indices:
            if llaves[ii] == "pedido":
                try:
                    q = Pedido.objects.get(numero=data_dict["entrada {}".format(i+1)][ii])
                except:
                    q = None
                dict_args[llaves[ii]] = q
            elif llaves[ii] == "repartidor":
                try:
                    q = Repartidor.objects.get(id=data_dict["entrada {}".format(i+1)][ii])
                except:
                    q = None
                dict_args[llaves[ii]] = q
            else:
                dict_args[llaves[ii]] = data_dict["entrada {}".format(i+1)][ii]

        e = Envio(**dict_args)
        e.save()
        dict_args.clear()

########## RENDERIZADO DE HOJAS EN PDF ##########
def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL     # Typically /static/
    #static Root
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

def render_to_pdf(template_src, context):
    template = get_template(template_src)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, link_callback=link_callback)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def render_to_file(template_src, context):
    template = get_template(template_src)
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, link_callback=link_callback)

    if not pdf.err:
        return result.getvalue()
    return None