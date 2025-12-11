from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClienteForm
from .models import Cliente,EstadoClienteCat,FrecuenciaClienteCat
from django.contrib import messages
from crm.utils import queryset_clientes_por_rol
from usuario.models import Usuario
from django.db import models
from django.utils import timezone
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

def clientes_list(request):
    usuario = Usuario.activos.filter(idusuario=request.session.get("idusuario")).first()
    clientes = queryset_clientes_por_rol(usuario)

    return render(request, "clientes/clientes_list.html", {
        "clientes": clientes
    })


def cliente_crear(request):
    usuario = Usuario.activos.filter(idusuario=request.session.get("idusuario")).first()

    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.usuario_registro = usuario
            cliente.owner = usuario if usuario.rol.nombre_rol == "Dueño" else usuario.owner
            cliente.save()

            messages.success(request, "Cliente registrado correctamente.")
            return redirect("cliente:listar")

    else:
        form = ClienteForm()

    return render(request, "clientes/cliente_form.html", {"form": form})


def cliente_editar(request, pk):
    usuario = Usuario.activos.filter(idusuario=request.session.get("idusuario")).first()
    qs = queryset_clientes_por_rol(usuario)

    cliente = get_object_or_404(qs, idcliente=pk)

    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente actualizado correctamente.")
            return redirect("cliente:listar")

    else:
        form = ClienteForm(instance=cliente)

    return render(request, "clientes/cliente_form.html", {"form": form})


def cliente_eliminar(request, pk):
    usuario = Usuario.activos.filter(idusuario=request.session.get("idusuario")).first()
    qs = queryset_clientes_por_rol(usuario)

    cliente = get_object_or_404(qs, idcliente=pk)

    cliente.eliminar_logico()
    messages.success(request, "Cliente eliminado correctamente.")
    return redirect("cliente:listar")
