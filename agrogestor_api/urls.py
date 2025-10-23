from django.contrib import admin
from rest_framework_simplejwt.views import TokenRefreshView
from gestion.views import MyTokenObtainPairView
from django.urls import path, include
#from rest_framework_simplejwt.views import (
#    TokenObtainPairView,
#    TokenRefreshView,
#)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('gestion.urls')), # <-- Esta línea conecta todo
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'), # <-- USA TU VISTA
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
