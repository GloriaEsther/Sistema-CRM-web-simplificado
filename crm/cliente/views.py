from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClienteForm
from .models import Cliente
from django.contrib import messages
from crm.utils import require_roles
from usuario.models import Usuario
from django.db import models
from django.utils import timezone

@require_roles(['Dueño','Administrador','Vendedor'])
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            # asignar usuario_registro si está en session
            usuario_id = request.session.get('idusuario')
            if usuario_id:
                cliente.usuario_registro = Usuario.todos.get(pk=usuario_id)
            cliente.save()
            messages.success(request, "Cliente creado.")
            return redirect('clientes:listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'clientes/crear.html', {'form': form})

@require_roles(['Dueño','Administrador','Vendedor'])
def listar_clientes(request):
    q = request.GET.get('q','')
    if q:
        clientes = Cliente.objects.filter(activo=True).filter(
            models.Q(nombre__icontains=q) | models.Q(apellidopaterno__icontains=q) | models.Q(apellidomaterno__icontains=q)
        )
    else:
        clientes = Cliente.objects.filter(activo=True)
    return render(request, 'clientes/listar.html', {'clientes': clientes})

@require_roles(['Dueño','Administrador'])
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.activo = False
    cliente.fecha_eliminacion = timezone.now()
    cliente.save()
    messages.success(request, "Cliente dado de baja (lógico).")#Cliente dado de baja (lógico)
    return redirect('clientes:listar_clientes')
