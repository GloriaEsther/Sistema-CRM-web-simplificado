from django.shortcuts import render,redirect
from usuario.models import Usuario
from cliente.models import Cliente
from servicios.models import Servicio
from cotizacion.models import Cotizacion, CotizacionDetalle
from django.http import HttpResponse
from time import time
from django.contrib import messages
from crm.utils import queryset_cotizaciones_por_rol,obtener_owner,queryset_clientes_por_rol,queryset_servicios_por_rol,require_roles

def cotizacion_crear(request):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()

    if not usuario:
        return redirect("usuario:login")
    
    owner = obtener_owner(request, usuario)

    if not owner:
        messages.error(request, "No hay negocio seleccionado.")
        return redirect("superusuario:listar_negocios")
    
    clientes = queryset_clientes_por_rol(usuario,owner)
    servicios = queryset_servicios_por_rol(usuario,owner)

    if usuario.rol.nombre_rol == "Consultor":
        messages.error(
            request,
            "No tienes permisos para registrar cotizaciones."
        )
        return redirect("cotizacion:listar")
    
    if request.method == "POST":
        cliente_id = request.POST.get("cliente")
        servicio_id = request.POST.get("servicio")
        cantidad = int(request.POST.get("cantidad", 1))

        cliente = Cliente.activos.get(idcliente=cliente_id)
        servicio = Servicio.activos.get(idservicio=servicio_id)

        cotizacion = Cotizacion.activos.create(
            cliente=cliente,
            total=servicio.precio * cantidad,
            activo=True,
            owner=owner,
            usuario_registro=usuario
        )

        CotizacionDetalle.activos.create(
            cotizacion=cotizacion,
            servicio=servicio,
            cantidad=cantidad,
            precio_unitario=servicio.precio,
            subtotal=servicio.precio * cantidad,
            activo=True
        )

        messages.success(request, "Cotización creada correctamente.")
        return redirect("cotizacion:listar")
    
    return render(request, "cotizacion/crear_cotizacion.html", {
        "clientes": clientes,
        "servicios": servicios,
        "timestamp": int(time())
    })
    
    
def cotizacion_detalle(request, pk):
    cotizacion = Cotizacion.activos.filter(idcotizacion=pk).first()

    if not cotizacion:
        return HttpResponse("Cotización no encontrada", status=404)

    detalles = cotizacion.detalles.filter(activo=True)

    return render(request, "cotizacion/consultar_cotizacion.html", {
        "cotizacion": cotizacion,
        "detalles": detalles
    })


@require_roles(['Dueño', 'Administrador','Superusuario','Consultor'])
def cotizaciones_list(request):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()
    owner = obtener_owner(request, usuario)

    if not owner:
       cotizaciones = Cotizacion.activos.none()
    else:
        cotizaciones = queryset_cotizaciones_por_rol(usuario,owner)

    return render(request, "cotizacion/lista_cotizaciones.html", {
        "cotizaciones": cotizaciones
    })
