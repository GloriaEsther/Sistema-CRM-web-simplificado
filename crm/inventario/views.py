from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest,HttpResponse
from .models import Inventario
from .forms import InventarioForm
from usuario.models import Usuario
from crm.utils import queryset_inventario_por_rol

#@login_required
def inventario_list(request):
    usuario = Usuario.activos.filter(idusuario=request.session.get("idusuario")).first()
    inventario = queryset_inventario_por_rol(usuario)

    return render(request, "inventario/lista_inventario.html", {
        "inventario": inventario
    })

#@login_required
def inventario_crear(request):
    usuario = Usuario.activos.filter(idusuario=request.session.get("idusuario")).first()

    if request.method == "POST":
        form = InventarioForm(request.POST)
        if form.is_valid():
            articulo = form.save(commit=False)
            articulo.usuario_registro = usuario
            articulo.owner = usuario if usuario.rol.nombre_rol == "Dueño" else usuario.owner_id
            articulo.save()

            messages.success(request, "Artículo registrado correctamente.")
            return redirect("inventario:listar")
    else:
        form = InventarioForm()

    return render(request, "inventario/crear_inventario.html", {
        "form": form
    })

#@login_required
def inventario_editar(request, pk):
    usuario = Usuario.activos.filter(idusuario=request.session.get("idusuario")).first()
    qs = queryset_inventario_por_rol(usuario)

    articulo = get_object_or_404(qs, idinventario=pk)

    if request.method == "POST":
        form = InventarioForm(request.POST, instance=articulo)
        if form.is_valid():
            form.save()
            messages.success(request, "Artículo actualizado correctamente.")
            return redirect("inventario:listar")
    else:
        form = InventarioForm(instance=articulo)

    return render(request, "inventario/editar_inventario.html", {
        "form": form
    })

#@login_required
def inventario_eliminar(request, pk):
    usuario = Usuario.activos.filter(idusuario=request.session.get("idusuario")).first()
    qs = queryset_inventario_por_rol(usuario)

    articulo = get_object_or_404(qs, idinventario=pk)
    articulo.eliminar_logico()

    messages.success(request, "Artículo eliminado correctamente.")
    return redirect("inventario:listar")

#@login_required
def inventario_detalle(request, pk):
    usuario = Usuario.activos.filter(idusuario=request.session.get("idusuario")).first()
    qs = queryset_inventario_por_rol(usuario)  # si usas filtro por rol

    inventario = get_object_or_404(qs, idinventario=pk)

    return render(request, "inventario/consultar_inventario.html", {
        "inventario": inventario   
    })