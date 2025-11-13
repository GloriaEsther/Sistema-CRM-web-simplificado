from django.shortcuts import render
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from ventas.models import Venta
from cliente.models import Cliente
from django.http import JsonResponse
from django.contrib import messages

def dashboard(request):
    return render(request, 'reportes/dashboard.html')

def ventas_mensuales_json(request):
    qs = (Venta.objects.filter(activo=True)
          .annotate(mes=TruncMonth('fecha_venta'))
          .values('mes')
          .annotate(total=Sum('preciototal'))
          .order_by('mes'))
    data = [{'mes': r['mes'].strftime('%Y-%m'), 'total': float(r['total'] or 0)} for r in qs]
    return JsonResponse(data, safe=False)

def clientes_frecuentes_json(request):
    qs = (Cliente.objects.filter(activo=True)
          .annotate(ventas=Count('oportunidad__venta_oportunidad'))
          .order_by('-ventas')[:10])
    data = [{'cliente': f"{c.nombre} {c.apellidopaterno}", 'ventas': c.ventas} for c in qs]
    return JsonResponse(data, safe=False)

