from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import InventarioForm
from usuario.models import Usuario
from inventario.models import Inventario
from crm.utils import queryset_inventario_por_rol,obtener_owner
from time import time

def inventario_list(request):
    usuario = Usuario.activos.filter(idusuario=request.session.get("idusuario")).first()
    owner = obtener_owner(request, usuario)

    if not owner:
        inventario = Inventario.activos.none()
    else:
        inventario = queryset_inventario_por_rol(usuario,owner)

    return render(request, "inventario/lista_inventario.html", {
        "inventario": inventario
    })

def inventario_crear(request):
    usuario = Usuario.activos.filter(idusuario=request.session.get("idusuario")).first()
    owner = obtener_owner(request, usuario)

    if not owner:
        messages.error(request, "No hay negocio seleccionado.")
        return redirect("superusuario:listar_negocios")

    if request.method == "POST":
        form = InventarioForm(data=request.POST, owner = owner)#
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.usuario_registro = usuario
            articulo.owner = owner
            articulo.save()

            messages.success(request, "Artículo registrado correctamente.")
            return redirect("inventario:listar")
    else:
        form = InventarioForm(owner =owner)

    return render(request, "inventario/crear_inventario.html", {
        "form": form,
        "timestamp": int(time())
    })

def inventario_editar(request, pk):
    usuario = Usuario.activos.filter(idusuario=request.session.get("idusuario")).first()
    owner = obtener_owner(request, usuario)
    qs = queryset_inventario_por_rol(usuario,owner)
    articulo = get_object_or_404(qs, idinventario=pk)

    if request.method == "POST":
        form = InventarioForm(data = request.POST, instance=articulo,owner = owner)
        if form.is_valid():
            form.save()
            messages.success(request, "Artículo actualizado correctamente.")
            return redirect("inventario:listar")
    else:
        form = InventarioForm(instance=articulo,owner = owner)

    return render(request, "inventario/editar_inventario.html", {
        "form": form,
        "timestamp": int(time())
    })

def inventario_eliminar(request, pk):
    usuario = Usuario.activos.filter(idusuario=request.session.get("idusuario")).first()
    owner = obtener_owner(request, usuario)
    qs = queryset_inventario_por_rol(usuario,owner)
    articulo = get_object_or_404(qs, idinventario=pk)

    rol=usuario.rol.nombre_rol
     # Dueño y Administrador: pueden eliminar cualquiera en su negocio, superusuario en todos 
    if rol in ["Dueño", "Administrador", "Superusuario"]:
        articulo.eliminar_logico()
        messages.success(request, "Artículo eliminado correctamente.")
        return redirect("inventario:listar")
    
    if rol == "Vendedor":
        if articulo.usuario_registro != usuario.idusuario:
            messages.error(
                request,
                "No tienes permiso para eliminar este articulo."
            )
        articulo.eliminar_logico()
        messages.success(request, "Artículo eliminado correctamente.")
        return redirect("inventario:listar")

def inventario_detalle(request, pk):
    usuario = Usuario.activos.filter(idusuario=request.session.get("idusuario")).first()
    owner = obtener_owner(request, usuario)
    qs = queryset_inventario_por_rol(usuario,owner) 

    inventario = get_object_or_404(qs, idinventario=pk)

    return render(request, "inventario/consultar_inventario.html", {
        "inventario": inventario   
    })