from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import (
    Usuarios, Categoriainsumos, Detalleinsumosusados, Insumos, Cultivos,
    Roles, Suelos, Suelos_Cultivos, Unidadesmedida, Monitoreosuelos, Mantenimientocultivos
)
from .serializers import (
    UsuarioSerializer, CategoriainsumosSerializer, DetalleinsumosSerializer,
    InsumosSerializer, CultivosSerializer, RoleSerializer, SueloSerializer,
    SuelosCultivosSerializer, UnidadesmedidaSerializer, MonitoreosueloSerializer,
    MantenimientocultivosSerializer
)
# Importaciones para el login
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer

# --- PLANTILLA DE COMPORTAMIENTO PARA BORRADO LÓGICO ---
class SoftDeleteViewSetMixin:
    """
    Anula el método `destroy` para realizar un borrado lógico (estado=False)
    y filtra el queryset para mostrar solo los registros activos.
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.estado = False  # Cambia el estado en lugar de borrar
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        """
        Sobrescribe el queryset para devolver solo los objetos
        donde el campo 'estado' es True.
        """
        # Usamos `self.queryset.model` para obtener el modelo asociado a la vista
        return self.queryset.model.objects.filter(estado=True)

# --- VISTAS ACTUALIZADAS CON EL BORRADO LÓGICO ---

# Nota: El orden de herencia es importante. El Mixin va primero.
class CultivosViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Cultivos.objects.all()
    serializer_class = CultivosSerializer

class MantenimientocultivosViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Mantenimientocultivos.objects.all()
    serializer_class = MantenimientocultivosSerializer

class InsumosViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Insumos.objects.all()
    serializer_class = InsumosSerializer

# --- APLICA EL MIXIN A TODAS LAS DEMÁS VISTAS QUE QUIERAS PROTEGER ---

class UsuarioViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuarioSerializer

class CategoriainsumosViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Categoriainsumos.objects.all()
    serializer_class = CategoriainsumosSerializer

class DetalleinsumosViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Detalleinsumosusados.objects.all()
    serializer_class = DetalleinsumosSerializer

class RoleViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RoleSerializer

class SueloViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Suelos.objects.all()
    serializer_class = SueloSerializer

class SuelosCultivosViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Suelos_Cultivos.objects.all()
    serializer_class = SuelosCultivosSerializer

class UnidadesmedidaViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Unidadesmedida.objects.all()
    serializer_class = UnidadesmedidaSerializer

class MonitoreosueloViewSet(SoftDeleteViewSetMixin, viewsets.ModelViewSet):
    queryset = Monitoreosuelos.objects.all()
    serializer_class = MonitoreosueloSerializer

# --- VISTA DE LOGIN (Esta no cambia) ---
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
