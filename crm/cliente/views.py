from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClienteForm
from .models import Cliente
from django.contrib import messages
from crm.utils import queryset_clientes_por_rol,limpiar_valor,require_roles
from usuario.models import Usuario
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from time import time
#Importar datos desde Excel
import pandas as pd
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import ImportarClientesForm
from django.db import transaction

def clientes_list(request):#empleados pueden ver clientes...
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
            cliente.owner = usuario if usuario.rol.nombre_rol == "Dueño" else usuario.owner_id
            cliente.save()

            messages.success(request, "Cliente registrado correctamente.")
            return redirect("cliente:listar")

    else:
        form = ClienteForm()

    return render(request, "clientes/cliente_form.html", {
        "form": form,
        "timestamp": int(time())
    })


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

    return render(request, "clientes/cliente_editar.html", {
        "form": form,
        "timestamp": int(time())
    })

def cliente_eliminar(request, pk):
    usuario = Usuario.activos.filter(idusuario=request.session.get("idusuario")).first()
    cliente = get_object_or_404(Cliente.activos, idcliente=pk)
    rol=usuario.rol.nombre_rol
     # Dueño y Administrador: pueden eliminar cualquiera
    if rol in ["Dueño", "Administrador"]:
        cliente.eliminar_logico()
        messages.success(request, "Cliente eliminado correctamente.")
        return redirect("cliente:listar")

    # Vendedor: solo si él lo registró
    if rol == "Vendedor":
        if cliente.usuario_registro != usuario.idusuario:
            messages.error(
                request,
                "No tienes permiso para eliminar este cliente."
            )
            return redirect("cliente:listar")

        cliente.eliminar_logico()
        messages.success(request, "Cliente eliminado correctamente.")
        return redirect("cliente:listar")
    

def cliente_detalle(request, pk):
    cliente = Cliente.activos.filter(idcliente=pk).first()
    
    if not cliente:
        return HttpResponse("Cliente no encontrado", status=404)
    
    return render(request, "clientes/cliente_detalle.html", {
        "cliente": cliente
    })

def importar_clientes(request):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()

    if request.method == "POST":
        form = ImportarClientesForm(request.POST, request.FILES)

        if form.is_valid():
            archivo = request.FILES["archivo"]

            try:
                df = pd.read_excel(archivo)

                # Campos obligatorios
                campos_requeridos = [
                    "nombre",
                    "apellidopaterno",
                    "apellidomaterno",
                    "numerotelcli",
                    "correo",
                    "direccion",
                    "rfc",
                    "fecha_nacimiento",
                    "comentarios"
                ]

                for campo in campos_requeridos:
                    if campo not in df.columns:
                        messages.error(
                            request,
                            f"Falta la columna '{campo}' en el archivo Excel"
                        )
                        return redirect("cliente:importar")
                owner = (
                    usuario if usuario.rol.nombre_rol == "Dueño"
                    else usuario.owner_id
                )

                registros_omitidos = 0
                registros_creados = 0
         
                with transaction.atomic():
                    for index, fila in df.iterrows():
                        
                        nombre = limpiar_valor(fila.get("nombre"))
                        telefono = limpiar_valor(fila.get("numerotelcli"))
                        #rfc = limpiar_valor(fila.get("rfc"))

                        # Validaciones obligatorias
                        if not nombre:
                            messages.error(
                                request,
                                f"Fila {index + 2}: El campo 'nombre' es obligatorio."
                            )
                            return redirect("cliente:importar")

                        if not telefono:
                            messages.error(
                                request,
                                f"Fila {index + 2}: El teléfono es obligatorio."
                            )
                            return redirect("cliente:importar")
                        
                        # Validar RFC duplicado
                        rfc = fila.get("rfc")

                        # Normalizar RFC
                        if pd.isna(rfc) or str(rfc).strip() == "":
                            rfc = None
                        else:
                            rfc = str(rfc).strip().upper()

                        if rfc and Cliente.todos.filter(rfc=rfc, owner=owner).exists():
                            registros_omitidos += 1
                            continue  
                        
                        Cliente.todos.create(                           
                            nombre=nombre,
                            apellidopaterno=limpiar_valor(fila.get("apellidopaterno")),
                            apellidomaterno=limpiar_valor(fila.get("apellidomaterno")),
                            numerotelcli=telefono,
                            correo=limpiar_valor(fila.get("correo")),
                            direccion=limpiar_valor(fila.get("direccion")),
                            rfc=rfc,
                            fecha_nacimiento=(
                                None if pd.isna(fila.get("fecha_nacimiento"))
                                else fila.get("fecha_nacimiento")
                            ),
                            comentarios=limpiar_valor(fila.get("comentarios")),
                            
                            usuario_registro=usuario,
                            owner=owner,
                            activo=True
                        )
                        registros_creados += 1

                messages.success(
                    request,
                    f"Clientes importados: {registros_creados}. "
                    f"Omitidos por RFC duplicado: {registros_omitidos}."
                )

                return redirect("cliente:listar")

            except Exception as e:
                
                messages.error(
                    request,
                    "No se pudo importar el archivo. "
                    "Verifica que el Excel cumpla con el formato indicado."
                )
                
                return redirect("cliente:importar")

    else:
        form = ImportarClientesForm()

    return render(request, "clientes/importar_clientes.html", {
        "form": form
    })
                