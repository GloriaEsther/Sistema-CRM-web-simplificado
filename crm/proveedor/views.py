from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProveedorForm
from .models import Proveedor
from django.contrib import messages
from crm.utils import queryset_proveedores_por_rol
from usuario.models import Usuario
from time import time
from django.http import HttpResponse

def proveedor_list(request):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()

    proveedores = queryset_proveedores_por_rol(usuario)

    return render(request, "proveedor/lista_proveedores.html", {
        "proveedores": proveedores
    })

def proveedor_crear(request):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()

    if request.method == "POST":
        form = ProveedorForm(request.POST)
        if form.is_valid():
            proveedor = form.save(commit=False)
            proveedor.usuario_registro = usuario
            proveedor.owner = usuario if usuario.rol.nombre_rol == "Dueño" else usuario.owner_id
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

    qs = queryset_proveedores_por_rol(usuario)
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

    qs = queryset_proveedores_por_rol(usuario)
    proveedor = get_object_or_404(qs, idproveedor=pk)

    proveedor.activo = False
    proveedor.save()

    messages.success(request, "Proveedor eliminado correctamente.")
    return redirect("proveedor:listar")

def proveedor_detalle(request, pk):
    proveedor = Proveedor.todos.filter(
        idproveedor=pk,
        activo=True
    ).first()

    if not proveedor:
        return HttpResponse("Proveedor no encontrado", status=404)

    return render(request, "proveedor/consultar_proveedor.html", {
        "proveedor": proveedor
    })
