from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProveedorForm
from .models import Proveedor
from django.contrib import messages
from crm.utils import queryset_proveedores_por_rol,obtener_owner
from usuario.models import Usuario
from time import time
from django.http import HttpResponse

def proveedor_list(request):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()
    owner = obtener_owner(request, usuario)

    if not owner:
        proveedores =Proveedor.activos.none()
    else:
        proveedores = queryset_proveedores_por_rol(usuario,owner)

    return render(request, "proveedor/lista_proveedores.html", {
        "proveedores": proveedores
    })

def proveedor_crear(request):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()
    owner = obtener_owner(request, usuario)

    if not owner:
        messages.error(request, "No hay negocio seleccionado.")
        return redirect("superusuario:listar_negocios")

    if request.method == "POST":
        form = ProveedorForm(request.POST)
        if form.is_valid():
            proveedor = form.save(commit=False)
            proveedor.usuario_registro = usuario
            proveedor.owner = owner#usuario if usuario.rol.nombre_rol == "Dueño" else usuario.owner_id
            proveedor.save()

            messages.success(request, "Proveedor registrado correctamente.")
            return redirect("proveedor:listar")
    else:
        form = ProveedorForm()

    return render(request, "proveedor/crear_proveedor.html", {
        "form": form,
        "timestamp": int(time())
    })

def proveedor_editar(request, pk):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()
    owner = obtener_owner(request, usuario)
    qs = queryset_proveedores_por_rol(usuario,owner)
    proveedor = get_object_or_404(qs, idproveedor=pk)

    if request.method == "POST":
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor actualizado correctamente.")
            return redirect("proveedor:listar")
    else:
        form = ProveedorForm(instance=proveedor)

    return render(request, "proveedor/editar_proveedor.html", {
        "form": form,
        "timestamp": int(time())
    })

def proveedor_eliminar(request, pk):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()
    owner = obtener_owner(request, usuario)
    qs = queryset_proveedores_por_rol(usuario,owner)
    proveedor = get_object_or_404(qs, idproveedor=pk)
    rol=usuario.rol.nombre_rol
     # Dueño y Administrador: pueden eliminar cualquiera en su negocio, superusuario en todos 
    if rol in ["Dueño", "Administrador", "Superusuario"]:
        proveedor.eliminar_logico()
        #proveedor.activo = False
        #proveedor.save()
        messages.success(request, "Proveedor eliminado correctamente.")
        return redirect("proveedor:listar")
    # Vendedor: solo si él lo registró
    if rol == "Vendedor":
        if proveedor.usuario_registro != usuario.idusuario:
            messages.error(
                request,
                "No tienes permiso para eliminar este proveedor."
            )
        proveedor.eliminar_logico()
        messages.success(request, "Proveedor eliminado correctamente.")
        return redirect("proveedor:listar")

def proveedor_detalle(request, pk):
    proveedor = Proveedor.activos.filter(idproveedor=pk).first()

    if not proveedor:
        return HttpResponse("Proveedor no encontrado", status=404)

    return render(request, "proveedor/consultar_proveedor.html", {
        "proveedor": proveedor
    })
