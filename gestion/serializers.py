from rest_framework import serializers
from .models import Cultivos, Categoriainsumos, Usuarios, Unidadesmedida, Mantenimientocultivos, Insumos, Detalleinsumosusados, Monitoreosuelos, Roles  , Suelos, Suelos_Cultivos
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        exclude = ('contraseña')

class CultivosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cultivos
        fields = '__all__'
        read_only_fields = ['codigo']

class MantenimientocultivosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mantenimientocultivos
        fields = '__all__'

class InsumosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumos
        fields = '__all__'

class DetalleinsumosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detalleinsumosusados
        fields = '__all__'

class MonitoreosueloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitoreosuelos
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'

class CategoriainsumosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoriainsumos
        fields = '__all__'

class UnidadesmedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidadesmedida
        fields = '__all__'

class SueloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suelos
        fields = '__all__'

class SuelosCultivosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suelos_Cultivos
        fields = '__all__'



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)



        return token


    def validate(self, attrs):

        attrs['username'] = attrs.get('ussername')


        data = super().validate(attrs)
        return data