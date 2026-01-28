from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClienteForm
from .models import Cliente
from django.contrib import messages
from crm.utils import queryset_clientes_por_rol,limpiar_valor,require_roles,obtener_owner
from usuario.models import Usuario
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from time import time
#Importar datos desde Excel
import pandas as pd
from .forms import ImportarClientesForm
from django.db import transaction
import traceback

def clientes_list(request):#empleados pueden ver clientes..
    usuario = Usuario.activos.filter(idusuario=request.session.get("idusuario")).first()
    owner = obtener_owner(request, usuario)

    if not owner:
        clientes = Cliente.activos.none()
    else:
        clientes = queryset_clientes_por_rol(usuario, owner)
        
    return render(request, "clientes/lista_clientes.html", {
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
                df = pd.read_excel(archivo, dtype=str)#prueba esto hace que el excel se lea como texto...

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
               
                #owner = usuario if usuario.rol.nombre_rol == "Dueño" else usuario.owner#prueba


                rfc_duplicado = 0
                registros_creados = 0
                num_duplicados = 0
                total_omitidos = 0
                correo_duplicados = 0

                clientes = Cliente.todos.filter(owner=owner).values_list('rfc', 'numerotelcli', 'correo')#prueba... 

                #buscar con sets(prueba)
                            
                rfc_existente = {str(r[0]).strip().upper() for r in clientes if r[0]}
                numtel_existente = {str(r[1]).strip() for r in clientes if r[1]}
                correo_existentes = {str(r[2]).strip().lower() for r in clientes if r[2]}
                
                with transaction.atomic():
                    for index, fila in df.iterrows():
                        
                        nombre = limpiar_valor(fila.get("nombre"))
                        telefono = limpiar_valor(fila.get("numerotelcli"))
                        correo_ =limpiar_valor(fila.get("correo"))
                        correo_para_comparar = correo_.lower().strip() if correo_ else None
                        rfc = limpiar_valor(fila.get("rfc"))
                        if rfc: rfc = rfc.upper() 

                        if not nombre or not telefono:# si hay celdas sin nombre o telefono ...
                            total_omitidos +=1
                            continue#los omite
                        #Logica de duplicado...
                        es_duplicado = False

                        if rfc and rfc in rfc_existente:
                                rfc_duplicado += 1
                                es_duplicado = True
                            
                        elif telefono and telefono in numtel_existente:
                                num_duplicados += 1
                                es_duplicado = True
                            
                        elif correo_ and correo_para_comparar in correo_existentes:
                                correo_duplicados += 1
                                es_duplicado = True

                        if es_duplicado:
                                total_omitidos += 1
                                continue

                        if telefono and len(telefono) > 10:
                            total_omitidos += 1
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
                        # Agregamos a los sets para que la siguiente fila detecte si este ya se agregó
                        if rfc: rfc_existente.add(rfc)
                        if telefono: numtel_existente.add(telefono)
                        if correo_: correo_existentes.add(correo_.lower())

                messages.success(
                    request,
                    f"Importación finalizada.  "
                    f"Clientes importados: {registros_creados}.  "
                    f"Clientes omitidos: {total_omitidos}.  "
                )
                return redirect("cliente:listar")

            except Exception as e:
                
                print(f"Error detallado en fila {index + 2}: {traceback.format_exc()}")
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
                