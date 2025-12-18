from django.shortcuts import render
from crm.utils import solo_superusuario
from cliente.models import Cliente
from usuario.models import Usuario
from oportunidades.models import Oportunidad


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
