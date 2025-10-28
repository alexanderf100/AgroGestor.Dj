from rest_framework import serializers
# Asegúrate de importar TODOS los modelos que vas a serializar
from .models import (
    Usuarios, Roles, Categoriainsumos, Unidadesmedida, Cultivos,
    Insumos, Mantenimientocultivos, Detalleinsumosusados, Suelos,
    Monitoreosuelos, Suelos_Cultivos,
    Cosechas, Ingresos, CostosCosecha # Nuevos modelos
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = Usuarios.USERNAME_FIELD

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['nombre'] = user.first_name
        token['rol'] = user.rolid.rol
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['usuario'] = {
            'id': self.user.id,
            'ussername': self.user.ussername,
            'nombre': self.user.first_name,
            'apellido': self.user.last_name,
            'email': self.user.email,
            'rol': self.user.rolid.rol,
        }
        return data



class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'

class UsuariosSerializer(serializers.ModelSerializer):
    # Para mostrar el nombre del rol en lugar del ID
    rol_nombre = serializers.CharField(source='rolid.rol', read_only=True)

    class Meta:
        model = Usuarios
        # Excluye campos sensibles o no necesarios en la API general
        fields = ['id', 'codigo', 'first_name', 'last_name', 'ussername', 'email', 'is_active', 'rolid', 'rol_nombre']
        read_only_fields = ['codigo', 'last_login', 'date_joined']


class CategoriainsumosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoriainsumos
        fields = '__all__'

class UnidadesmedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidadesmedida
        fields = '__all__'

class CultivosSerializer(serializers.ModelSerializer):
    # Para mostrar el ussername del usuario en lugar del ID
    usuario_ussername = serializers.CharField(source='usuarioid.ussername', read_only=True)

    class Meta:
        model = Cultivos
        fields = '__all__'
        read_only_fields = ['codigo'] # Código lo genera el modelo


class InsumosSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source='categoriainsumoid.categoriainsumo', read_only=True, allow_null=True)
    unidad_abreviatura = serializers.CharField(source='unidadesmedidaid.abreviatura', read_only=True, allow_null=True)

    class Meta:
        model = Insumos
        fields = '__all__'


class MantenimientocultivosSerializer(serializers.ModelSerializer):
    cultivo_nombre = serializers.CharField(source='cultivoid.nombrecultivo', read_only=True, allow_null=True)

    class Meta:
        model = Mantenimientocultivos
        fields = '__all__'

class DetalleinsumosusadosSerializer(serializers.ModelSerializer):
    insumo_nombre = serializers.CharField(source='insumosid.insumo', read_only=True, allow_null=True)
    mantenimiento_tipo = serializers.CharField(source='mantenimientocultivosid.nombretipomantenimiento', read_only=True, allow_null=True)

    class Meta:
        model = Detalleinsumosusados

        exclude = []
        fields = '__all__'


class SuelosSerializer(serializers.ModelSerializer):
    usuario_ussername = serializers.CharField(source='usuarioid.ussername', read_only=True, allow_null=True)
    class Meta:
        model = Suelos
        fields = '__all__'

class MonitoreosuelosSerializer(serializers.ModelSerializer):
    suelo_nombre = serializers.CharField(source='suelosid.nombre', read_only=True, allow_null=True)
    class Meta:
        model = Monitoreosuelos
        fields = '__all__'

class SuelosCultivosSerializer(serializers.ModelSerializer):
    suelo_nombre = serializers.CharField(source='suelosid.nombre', read_only=True, allow_null=True)
    cultivo_nombre = serializers.CharField(source='cultivosid.nombrecultivo', read_only=True, allow_null=True)
    class Meta:
        model = Suelos_Cultivos
        #
        exclude = []
        fields = '__all__'



class CosechasSerializer(serializers.ModelSerializer):
    cultivo_nombre = serializers.CharField(source='cultivoid.nombrecultivo', read_only=True, allow_null=True)
    unidad_abreviatura = serializers.CharField(source='unidadmedidaid.abreviatura', read_only=True, allow_null=True)

    class Meta:
        model = Cosechas
        fields = '__all__'
        read_only_fields = ['estado'] # El estado se maneja por borrado lógico


class IngresosSerializer(serializers.ModelSerializer):
    #Mostrar info de la cosecha
    cosecha_info = serializers.PrimaryKeyRelatedField(read_only=True) # O un Nested Serializer si quieres más detalle

    class Meta:
        model = Ingresos
        fields = '__all__'
        read_only_fields = ['estado']


class CostosCosechaSerializer(serializers.ModelSerializer):
    #Mostrar info de la cosecha
    cosecha_info = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CostosCosecha
        fields = '__all__'
        read_only_fields = ['estado']

