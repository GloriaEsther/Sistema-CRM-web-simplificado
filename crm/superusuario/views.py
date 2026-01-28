from django.shortcuts import render,redirect,get_object_or_404
from crm.utils import solo_superusuario
from cliente.models import Cliente
from usuario.models import Usuario
from ventas.models import Venta
from oportunidades.models import Oportunidad
from django.db.models import Q
from django.contrib import messages

@solo_superusuario
def dashboard(request):

    usuarios_activos = Usuario.activos.count()
    usuarios_inactivos = Usuario.todos.filter(activo=False).count()

    duenos = Usuario.activos.filter(rol__nombre_rol="Dueño")

    duenos_sin_clientes = duenos.exclude(
        idusuario__in=Cliente.todos.values_list('owner_id', flat=True)
    ).count()

    duenos_sin_oportunidades = duenos.exclude(
        idusuario__in=Oportunidad.todos.values_list(
            'negocio_oportunidad_id', flat=True
        )
    ).count()

    usuarios_total = Usuario.todos.count()
    clientes_total = Cliente.todos.count()
    oportunidades_total = Oportunidad.activos.count()

    clientes = Cliente.todos.order_by('-idcliente')[:10]
    usuarios = Usuario.todos.order_by('-idusuario')[:5]

    negocios = []

    for dueno in duenos:
        total_clientes = Cliente.todos.filter(owner=dueno).count()
        total_oportunidades = Oportunidad.activos.filter(
            negocio_oportunidad=dueno
        ).count()

        if total_clientes == 0 and total_oportunidades == 0:
            estado = "Inactivo"
        elif total_clientes > 0 and total_oportunidades == 0:
            estado = "Bajo uso"
        else:
            estado = "Activo"

        negocios.append({
            "dueno": dueno,
            "clientes": total_clientes,
            "oportunidades": total_oportunidades,
            "estado": estado
        })

    return render(request, "superusuario/dashboard.html", {
        "usuarios_activos": usuarios_activos,
        "usuarios_inactivos": usuarios_inactivos,
        "duenos_sin_clientes": duenos_sin_clientes,
        "duenos_sin_oportunidades": duenos_sin_oportunidades,
        "total_clientes": clientes_total,
        "total_usuarios": usuarios_total,
        "total_oportunidades": oportunidades_total,
        "clientes": clientes,
        "usuarios": usuarios,
        "negocios": negocios,
    })

@solo_superusuario
def buscar_negocios(request):
    q = request.GET.get("q", "").strip()

    duenos = Usuario.activos.filter(rol__nombre_rol="Dueño")

    if q:
        duenos = duenos.filter(
            Q(nombre__icontains=q) |
            Q(apellidopaterno__icontains=q) |
            Q(apellidomaterno__icontains=q) |
            Q(nombre_negocio__icontains=q)
        )

    return render(request, "superusuario/lista_de_negocios.html", {
        "duenos": duenos
    })

@solo_superusuario# prueba....
def detalles_del_negocio(request, dueno_id):
    dueno = get_object_or_404(
        Usuario,
        idusuario=dueno_id,
        rol__nombre_rol="Dueño"
    )

    clientes = Cliente.todos.filter(owner=dueno).count()
    ventas = Venta.objects.filter(owner=dueno).count()
    oportunidades = Oportunidad.activos.filter(
        negocio_oportunidad=dueno
    ).count()

    return render(request, "superusuario/consultar_negocios.html", {
        "dueno": dueno,
        "clientes": clientes,
        "ventas": ventas,
        "oportunidades": oportunidades,
    })

@solo_superusuario
def ver_negocio(request, id_dueno):
    dueno = get_object_or_404(
        Usuario.activos,
        idusuario=id_dueno,
        rol__nombre_rol="Dueño"
    )

    request.session["modo_superusuario"] = True
    request.session["dueno_supervisado"] = dueno.idusuario
    messages.info(
        request,
        f"Estás viendo el negocio de {dueno.nombre}"
    )
    return redirect("cliente:listar")

@solo_superusuario
def salir_negocio(request):
    request.session.pop("modo_superusuario", None)
    request.session.pop("dueno_supervisado", None)
    messages.info(request, "Saliste del negocio supervisado")
    return redirect("superusuario:listar_negocios")
#si esas funciones si funcionan se les pasa arriba...

@solo_superusuario
def lista_negocios(request):#no lo he probado....
    busqueda = request.GET.get("q", "")

    duenos = Usuario.activos.filter(
        rol__nombre_rol="Dueño"
    )

    if busqueda:
        duenos = duenos.filter(
            Q(nombre__icontains=busqueda) |
            Q(nombre_negocio__icontains=busqueda)
        )

    negocios = []

    for dueno in duenos:
        clientes = Cliente.todos.filter(owner=dueno).count()
        oportunidades = Oportunidad.activos.filter(
            negocio_oportunidad=dueno
        ).count()

        negocios.append({
            "dueno": dueno,
            "clientes": clientes,
            "oportunidades": oportunidades
        })

    return render(request, "superusuario/negocios.html", {
        "negocios": negocios,
        "busqueda": busqueda
    })

@solo_superusuario
def usuarios_global(request):
    usuarios = Usuario.todos.select_related("rol")

    return render(request, "superusuario/usuarios.html", {
        "usuarios": usuarios
    })
