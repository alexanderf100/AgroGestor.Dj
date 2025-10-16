from rest_framework import  viewsets
from .models import Cultivos, Categoriainsumos, Usuarios, Unidadesmedida, Mantenimientocultivos, Insumos, Detalleinsumosusados, Monitoreosuelos, Roles  , Suelos, Suelos_Cultivos
from .serializers import CultivosSerializer, CategoriainsumosSerializer, UsuarioSerializer, UnidadesmedidaSerializer, \
    MantenimientocultivosSerializer, InsumosSerializer, DetalleinsumosSerializer, MonitoreosueloSerializer, \
    SuelosCultivosSerializer, SueloSerializer, RoleSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UsuarioSerializer

class CultivosViewSet(viewsets.ModelViewSet):
    queryset = Cultivos.objects.all()
    serializer_class = CultivosSerializer

class CategoriainsumosViewSet(viewsets.ModelViewSet):
    queryset = Categoriainsumos.objects.all()
    serializer_class = CategoriainsumosSerializer

class InsumosViewSet(viewsets.ModelViewSet):
    queryset = Insumos.objects.all()
    serializer_class = InsumosSerializer

class MantenimientocultivosViewSet(viewsets.ModelViewSet):
    queryset = Mantenimientocultivos.objects.all()
    serializer_class = MantenimientocultivosSerializer

class MonitoreosueloViewSet(viewsets.ModelViewSet):
    queryset = Monitoreosuelos.objects.all()
    serializer_class = MonitoreosueloSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    serializer_class = RoleSerializer

class SueloViewSet(viewsets.ModelViewSet):
    queryset = Suelos.objects.all()
    serializer_class = SueloSerializer

class SuelosCultivosViewSet(viewsets.ModelViewSet):
    queryset = Suelos_Cultivos.objects.all()
    serializer_class = SuelosCultivosSerializer

class UnidadesmedidaViewSet(viewsets.ModelViewSet):
    queryset = Unidadesmedida.objects.all()
    serializer_class = UnidadesmedidaSerializer

class DetalleinsumosViewSet(viewsets.ModelViewSet):
    queryset = Detalleinsumosusados.objects.all()
    serializer_class = DetalleinsumosSerializer