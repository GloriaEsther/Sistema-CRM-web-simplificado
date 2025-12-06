from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClienteForm
from .models import Cliente,EstadoClienteCat,FrecuenciaClienteCat
from django.contrib import messages
from crm.utils import require_roles
from usuario.models import Usuario
from django.db import models
from django.utils import timezone
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseBadRequest

@require_roles(['Dueño','Administrador','Vendedor'])
def crear_cliente(request):
    registrador_id = request.session.get('idusuario')
    usuario_registrador = Usuario.activos.get(idusuario=registrador_id)
   
    if usuario_registrador is None:
        messages.error(request, "No se encontró el usuario en sesión.")
        return redirect('usuario:inicio')

    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():

            try:
                nuevo_cliente = form.save(commit=False)
                # Asignar el Dueño logueado como el creador del registro
                nuevo_cliente.usuario_registro = usuario_registrador
                
                nuevo_cliente.save()

                messages.success(request, f"Cliente registrado correctamente.")
                # Redirigimos al mismo formulario para permitir que el Dueño siga registrando
                return redirect('cliente:crear_cliente')
                                
            except IntegrityError:
                # Si falla la unicidad (correo, RFC, CURP, etc.)
                messages.error(request, "Error: Ya existe un usuario con uno de los datos ingresados (correo, RFC o CURP).")
                # Pasamos 'duplicado': True para que el template muestre el modal
                return render(request, 'clientes/crear_cliente.html', {'form': form, 'duplicado': True})
            
            except Exception as e:
                messages.error(request, f"Ocurrió un error inesperado al registrar: {e}")           
    else:
        form = ClienteForm()
    return render(request, 'clientes/crear_cliente.html', {'form': form})

@require_roles(['Dueño','Administrador','Vendedor'])
def listar_clientes(request):
    q = request.GET.get('q','')
    estados = EstadoClienteCat.objects.all()
    frecuencias = FrecuenciaClienteCat.objects.all()

    if q:
        clientes = Cliente.objects.filter(activo=True).filter(
            models.Q(nombre__icontains=q) | models.Q(apellidopaterno__icontains=q) | models.Q(apellidomaterno__icontains=q)
        )
    else:
        clientes = Cliente.activos.all()#Cliente.objects.filter(activo=True)
    return render(request, 'clientes/listar.html', {
        'clientes': clientes,
        'estados': estados,
        'frecuencias': frecuencias,
    })



#----------------esto es prueba------------------#
@require_roles(['Dueño','Administrador','Vendedor'])#prueba......
def eliminar_cliente(request, pk):
    usuario_id = request.session.get("idusuario")
    usuario_logueado = get_object_or_404(Usuario, idusuario=usuario_id)
  
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == "POST":

        if usuario_logueado.rol.nombre_rol == "Vendedor":

            if cliente.usuario_registro != usuario_logueado:
                messages.error(request, "No puedes eliminar clientes que no registraste.")
                return redirect("clientes:listar_clientes")
            
        
        cliente.eliminar_logico()
        messages.success(request, "Cliente eliminado.")
        return redirect("clientes:listar_clientes")

  
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "clientes/_eliminar_confirmar.html", {
            "cliente": cliente
        })

   
    return redirect("clientes:listar_clientes")
    
@require_roles(['Dueño','Administrador','Vendedor'])    
def editar_cliente(request, pk):
   # oportunidad = get_object_or_404(Oportunidad.activos, pk=pk)
    cliente = get_object_or_404(Cliente, pk=pk)
    estados = EstadoClienteCat.objects.all()
    frecuencia=FrecuenciaClienteCat.objects.all()#no se si implementar lo de activos o no 
   
    if request.method == "POST":
        cliente.nombre = request.POST.get("nombre")
        cliente.apellidopaterno = request.POST.get("apellidopaterno")
        cliente.apellidomaterno = request.POST.get("apellidomaterno")
        cliente.numerotelcli = request.POST.get("numerotelcli")
        cliente.correo = request.POST.get("correo")
        cliente.direccion = request.POST.get("direccion")
        cliente.rfc =request.POST.get("rfc")
        cliente.fecha_nacimiento =request.POST.get("fecha_nacimiento")
        cliente.estado_cliente = request.POST.get("estado_cliente")
        cliente.frecuencia_compra = request.POST.get("frecuencia_compra")
        cliente.fecha_ultimocontacto = request.POST.get("fecha_ultimocontacto")
        cliente.comentarios =request.POST.get("comentarios")
        
        try:
            cliente.save()
            messages.success(request, "Cliente actualizado.")
            return redirect("clientes:listar_clientes")
        except Exception as e:
            messages.error(request, f"Error al guardar el cliente: {e}")
    
    if (
        request.headers.get("HX-Request") == "true" or
        request.headers.get("x-requested-with") == "XMLHttpRequest"
    ):
        return render(request, "clientes/listar.html", {
            "cliente": cliente,
            "estado": estados,
            "frecuencia": frecuencia,
        })

    
    return render(request, "clientes/listar.html", {
        "cliente": cliente,
        "estado": estado,
        "frecuencia": frecuencia,
    })


#vistas ajax(prueba)......
def ajax_consultar_cliente(request, pk):
    cliente = Cliente.activos.get(pk=pk)
    # Formato de fecha para display (dd/mm/yyyy) y para inputs HTML (yyyy-mm-dd)
    fecha_nacimiento_display = cliente.fecha_nacimiento.strftime('%d/%m/%Y') if cliente.fecha_nacimiento else ''
    fecha_nacimiento_iso = cliente.fecha_nacimiento.strftime('%Y-%m-%d') if cliente.fecha_nacimiento else ''
    
    fecha_ultimocontacto_display = cliente.fecha_ultimocontacto.strftime('%d/%m/%Y') if cliente.fecha_ultimocontacto else ''
    fecha_ultimocontacto_iso = cliente.fecha_ultimocontacto.strftime('%Y-%m-%d') if cliente.fecha_ultimocontacto else ''

    return JsonResponse({
        'idcliente': cliente.idcliente,
        'nombre': cliente.nombre,
        'apellidopaterno': cliente.apellidopaterno,
        'apellidomaterno': cliente.apellidomaterno or '',
        'numerotelcli': cliente.numerotelcli,
        'correo': cliente.correo,
        'direccion': cliente.direccion or '',
        'rfc': cliente.rfc or '',
        
        'fecha_nacimiento_display': fecha_nacimiento_display,
        'fecha_nacimiento_iso': fecha_nacimiento_iso,
        
        'estado_cliente': cliente.estado_cliente.nombre_estado,
        'estado_cliente_id': cliente.estado_cliente.idestadocli,
        
        'frecuencia_compra': cliente.frecuencia_compra.nombre_frecuencia,
        'frecuencia_compra_id': cliente.frecuencia_compra.idfrecuenciacli,
        
        'fecha_ultimocontacto_display': fecha_ultimocontacto_display,
        'fecha_ultimocontacto_iso': fecha_ultimocontacto_iso,

        'comentarios': cliente.comentarios or '',
    })

def ajax_buscar_cliente(request):
    q = request.GET.get('q', '').strip()
    qs = Cliente.activos.filter(nombre__icontains=q)[:15] if q else Cliente.activos.all()[:15]
    res = [{'id': c.idcliente, 'display': f"{c.nombre} {c.apellidopaterno}"} for c in qs]
    return JsonResponse(res, safe=False)

