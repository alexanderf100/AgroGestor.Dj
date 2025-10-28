from rest_framework import routers
from django.urls import path, include

# Importa TODOS tus ViewSets
from .views import (
    UsuarioViewSet, CategoriainsumosViewSet, DetalleinsumosViewSet,
    InsumosViewSet, CultivosViewSet, RoleViewSet, SueloViewSet,
    SuelosCultivosViewSet, UnidadesmedidaViewSet, MonitoreosueloViewSet,
    MantenimientocultivosViewSet,
    CosechasViewSet, IngresosViewSet, CostosCosechaViewSet # Nuevos
)

router = routers.DefaultRouter()

router.register(r'usuarios', UsuarioViewSet, basename='usuarios')
router.register(r'roles', RoleViewSet, basename='roles')
router.register(r'categorias', CategoriainsumosViewSet, basename='categorias')
router.register(r'unidades', UnidadesmedidaViewSet, basename='unidades')
router.register(r'cultivos', CultivosViewSet, basename='cultivos')
router.register(r'insumos', InsumosViewSet, basename='insumos')
router.register(r'mantenimientos', MantenimientocultivosViewSet, basename='mantenimientos')
router.register(r'detalleinsumos', DetalleinsumosViewSet, basename='detalleinsumos')
router.register(r'suelos', SueloViewSet, basename='suelos')
router.register(r'monitoreosuelo', MonitoreosueloViewSet, basename='monitoreosuelo')
router.register(r'suelos-cultivos', SuelosCultivosViewSet, basename='suelos-cultivos')
router.register(r'cosechas', CosechasViewSet, basename='cosechas')
router.register(r'ingresos', IngresosViewSet, basename='ingresos')
router.register(r'costos-cosecha', CostosCosechaViewSet, basename='costos-cosecha')


# Las URLs base son generadas por el router
urlpatterns = router.urls

