from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from time import time
from .models import Servicio
from .forms import ServicioForm
from usuario.models import Usuario
from crm.utils import queryset_servicios_por_rol

def servicios_list(request):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()

    servicios = queryset_servicios_por_rol(usuario)

    return render(request, "servicios/lista_servicios.html", {#servicios/servicios_list.html"
        "servicios": servicios
    })

def servicio_crear(request):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()

    if request.method == "POST":
        form = ServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.usuario_registro = usuario
            servicio.owner = usuario if usuario.rol.nombre_rol == "Dueño" else usuario.owner_id
            servicio.save()

            messages.success(request, "Servicio registrado correctamente.")
            return redirect("servicio:listar")
    else:
        form = ServicioForm()

    return render(request, "servicios/crear_servicio.html", {#"servicios/servicio_form.html"
        "form": form,
        "timestamp": int(time())
    })

def servicio_editar(request, pk):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()

    qs = queryset_servicios_por_rol(usuario)
    servicio = get_object_or_404(qs, idservicio=pk)

    if request.method == "POST":
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            messages.success(request, "Servicio actualizado correctamente.")
            return redirect("servicio:listar")
    else:
        form = ServicioForm(instance=servicio)

    return render(request, "servicios/editar_servicio.html", {#"servicios/servicio_editar.html
        "form": form,
        "timestamp": int(time())
    })

def servicio_eliminar(request, pk):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()

    qs = queryset_servicios_por_rol(usuario)
    servicio = get_object_or_404(qs, idservicio=pk)

    servicio.eliminar_logico()
    messages.success(request, "Servicio eliminado correctamente.")

    return redirect("servicio:listar")


def servicio_detalle(request, pk):
    servicio = Servicio.activos.filter(idservicio=pk).first()

    if not servicio:
        return HttpResponse("Servicio no encontrado", status=404)

    return render(request, "servicios/consultar_servicio.html", {#"servicios/servicio_detalle.html"
        "servicio": servicio
    })
