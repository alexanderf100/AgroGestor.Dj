from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F, DecimalField, Value
from django.db.models.functions import Coalesce # Para manejar nulos en sumas
from django.shortcuts import get_object_or_404 # Para obtener objetos fácil

# Importa TODOS los modelos y serializers
from .models import (
    Usuarios, Roles, Categoriainsumos, Unidadesmedida, Cultivos,
    Insumos, Mantenimientocultivos, Detalleinsumosusados, Suelos,
    Monitoreosuelos, Suelos_Cultivos,
    Cosechas, Ingresos, CostosCosecha # Nuevos
)
from .serializers import (
    UsuariosSerializer, RolesSerializer, CategoriainsumosSerializer,
    UnidadesmedidaSerializer, CultivosSerializer, InsumosSerializer,
    MantenimientocultivosSerializer, DetalleinsumosusadosSerializer,
    SuelosSerializer, MonitoreosuelosSerializer, SuelosCultivosSerializer,
    CosechasSerializer, IngresosSerializer, CostosCosechaSerializer, # Nuevos
    MyTokenObtainPairSerializer # Para la vista de login
)
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class SoftDeleteViewSetMixin:
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filtra para mostrar solo los activos por defecto
        model = getattr(self, 'model', self.queryset.model)

        # ¡CAMBIO AQUÍ!
        # Debe ser 'estado=True' para ser consistente con 'perform_destroy'
        return model.objects.filter(estado=True)

    def perform_destroy(self, instance):
        # Esto ya estaba correcto
        instance.estado = False
        instance.save()



class UsuarioViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Usuarios.objects.all().order_by('id')
    serializer_class = UsuariosSerializer
    model = Usuarios
    def get_queryset(self):
        # Esta vista usará 'is_active' en lugar de 'estado'
        return self.model.objects.filter(is_active=True)
    def perform_destroy(self, instance):
        # El soft-delete de Usuario es con 'is_active'
        instance.is_active = False
        instance.save()

class RoleViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Roles.objects.all().order_by('id')
    serializer_class = RolesSerializer
    model = Roles

class CategoriainsumosViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Categoriainsumos.objects.all().order_by('id')
    serializer_class = CategoriainsumosSerializer
    model = Categoriainsumos

class UnidadesmedidaViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Unidadesmedida.objects.all().order_by('id')
    serializer_class = UnidadesmedidaSerializer
    model = Unidadesmedida

class CultivosViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Cultivos.objects.all().order_by('-fechasiembra') # Orden más útil
    serializer_class = CultivosSerializer
    model = Cultivos

class InsumosViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Insumos.objects.all().order_by('insumo')
    serializer_class = InsumosSerializer
    model = Insumos

class MantenimientocultivosViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Mantenimientocultivos.objects.all().order_by('-fechamantenimiento')
    serializer_class = MantenimientocultivosSerializer
    model = Mantenimientocultivos

class DetalleinsumosViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Detalleinsumosusados.objects.all().order_by('id')
    serializer_class = DetalleinsumosusadosSerializer
    model = Detalleinsumosusados

class SueloViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Suelos.objects.all().order_by('nombre')
    serializer_class = SuelosSerializer
    model = Suelos

class MonitoreosueloViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Monitoreosuelos.objects.all().order_by('-fechamonitoreo')
    serializer_class = MonitoreosuelosSerializer
    model = Monitoreosuelos

class SuelosCultivosViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Suelos_Cultivos.objects.all().order_by('id')
    serializer_class = SuelosCultivosSerializer
    model = Suelos_Cultivos



class CosechasViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Cosechas.objects.all().order_by('-fechacosecha')
    serializer_class = CosechasSerializer
    model = Cosechas


    @action(detail=True, methods=['get'], url_path='reporte')
    def reporte_rentabilidad(self, request, pk=None):
        cosecha = get_object_or_404(Cosechas, pk=pk, estado=True) # Asegura que esté activa
        cultivo = cosecha.cultivoid

        # 1. Calcular Ingresos Totales (Usando Coalesce para manejar NULL)
        ingresos_data = Ingresos.objects.filter(cosechaid=cosecha, estado=True).aggregate(
            total=Coalesce(Sum('montoingreso'), Value(0), output_field=DecimalField())
        )
        ingresos_totales = ingresos_data['total']

        # 2. Calcular Costos Directos de Cosecha (Usando Coalesce)
        costos_directos_data = CostosCosecha.objects.filter(cosechaid=cosecha, estado=True).aggregate(
            total=Coalesce(Sum('montocosto'), Value(0), output_field=DecimalField())
        )
        costos_directos_cosecha = costos_directos_data['total']

        # 3. Calcular Costos de Mantenimiento (del cultivo asociado, usando Coalesce)
        costos_mantenimiento_data = Mantenimientocultivos.objects.filter(cultivoid=cultivo, estado=True).aggregate(
            total=Coalesce(Sum('costomanoobra'), Value(0), output_field=DecimalField())
        )
        costos_mantenimiento = costos_mantenimiento_data['total']

        # 4. Calcular Costos de Insumos (del cultivo asociado, usando Coalesce)
        costos_insumos_data = Detalleinsumosusados.objects.filter(
            mantenimientocultivosid__cultivoid=cultivo, # Filtra por el cultivo a través del mantenimiento
            estado=True,
            insumosid__estado=True # Asegura que el insumo base esté activo
        ).aggregate(
            total=Coalesce(
                Sum(F('cantidadusada') * F('insumosid__preciounitario')),
                Value(0),
                output_field=DecimalField()
            )
        )
        costos_insumos = costos_insumos_data['total']

        # 5. Calcular Totales y Rentabilidad
        costos_totales = costos_directos_cosecha + costos_mantenimiento + costos_insumos
        rentabilidad_neta = ingresos_totales - costos_totales

        # Prepara la respuesta
        reporte = {
            'cosecha_id': cosecha.id,
            'cultivo_nombre': cultivo.nombrecultivo,
            'fecha_cosecha': cosecha.fechacosecha.strftime('%Y-%m-%d %H:%M') if cosecha.fechacosecha else None, # Formatear fecha
            'ingresos_totales': float(ingresos_totales), # Convertir Decimal a float para JSON
            'costos_totales': float(costos_totales),
            'costos_desglose': { # Mejor desglose
                'directos_cosecha': float(costos_directos_cosecha),
                'mantenimiento_mano_obra': float(costos_mantenimiento),
                'insumos_utilizados': float(costos_insumos),
            },
            'rentabilidad_neta': float(rentabilidad_neta)
        }

        return Response(reporte, status=status.HTTP_200_OK)


class IngresosViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Ingresos.objects.all().order_by('-fechaingreso')
    serializer_class = IngresosSerializer
    model = Ingresos
    # permission_classes = [permissions.IsAuthenticated] # Heredado del Mixin


class CostosCosechaViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = CostosCosecha.objects.all().order_by('-fechacosto')
    serializer_class = CostosCosechaSerializer
    model = CostosCosecha


