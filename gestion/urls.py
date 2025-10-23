from rest_framework import routers

from .models import Suelos_Cultivos
from .views import (UsuarioViewSet, CategoriainsumosViewSet, DetalleinsumosViewSet,
                    InsumosViewSet, CultivosViewSet, RoleViewSet, SueloViewSet, SuelosCultivosViewSet,
                    UnidadesmedidaViewSet, MonitoreosueloViewSet, MantenimientocultivosViewSet)

router = routers.DefaultRouter()

router.register(r'usuarios', UsuarioViewSet)
router.register(r'categorias', CategoriainsumosViewSet)
router.register(r'detalleinsumos', DetalleinsumosViewSet)
router.register(r'insumos', InsumosViewSet)
router.register(r'cultivos', CultivosViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'suelos', SueloViewSet)
router.register(r'suelosCultivos', SuelosCultivosViewSet)
router.register(r'unidades', UnidadesmedidaViewSet)
router.register(r'monitoreosuelo', MonitoreosueloViewSet)
router.register(r'mantenimientos', MantenimientocultivosViewSet)



urlpatterns = router.urls