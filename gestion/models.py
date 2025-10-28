
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):

    def create_user(self, ussername, email, password=None, **extra_fields):
        if not ussername:
            raise ValueError('El campo Ussername es obligatorio')
        email = self.normalize_email(email)
        # Asegura que rolid tenga un valor antes de crear el user instance
        rol_id_instance = extra_fields.pop('rolid', None) # Extrae rolid si existe
        if not rol_id_instance:
             # Intenta buscar un rol por defecto o lanza error si no se proporciona
             try:
                 # Asigna un rol por defecto si existe (ej. ID 2 = 'Agricultor')
                 default_role = Roles.objects.get(id=2) # Ajusta este ID según tu BD
                 rol_id_instance = default_role
             except Roles.DoesNotExist:
                 raise ValueError("Se requiere un 'rolid' para crear un usuario.")

        # Asegúrate de pasar la instancia del Rol, no solo el ID, si el campo es ForeignKey
        user = self.model(ussername=ussername, email=email, rolid=rol_id_instance, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, ussername, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True) # Asegura que esté activo

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        try:
            # Busca el rol de Administrador en la tabla Roles (Ajusta 'Administrador' si tu rol se llama diferente)
            admin_role = Roles.objects.get(rol='Administrador')
            extra_fields['rolid'] = admin_role # Pasa la instancia del Rol
        except Roles.DoesNotExist:
            raise ValueError(
                "El rol 'Administrador' no existe en la base de datos. "
                "Por favor, créalo antes de crear un superusuario."
            )


        return self.create_user(ussername, email, password, **extra_fields)



class Roles(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS')
    rol = models.CharField(db_column='Rol', max_length=20, db_collation='Modern_Spanish_CI_AS')
    descripcionrol = models.CharField(db_column='DescripcionRol', max_length=150, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    estado = models.BooleanField(db_column='Estado')

    class Meta:
        managed = False
        db_table = 'Roles'

    def __str__(self):
        return self.rol


class Usuarios(AbstractUser):
    # Desactivamos username y adaptamos AbstractUser a nuestra tabla
    username = None
    id = models.AutoField(db_column='Id', primary_key=True)
    codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS', blank=True, null=True) # Permitir null temporalmente si lo crea Django
    first_name = models.CharField(db_column='Nombre', max_length=40, db_collation='Modern_Spanish_CI_AS')
    last_name = models.CharField(db_column='Apellido', max_length=50, db_collation='Modern_Spanish_CI_AS')
    ussername = models.CharField(db_column='UsserName', unique=True, max_length=20, db_collation='Modern_Spanish_CI_AS') # Este es nuestro USERNAME_FIELD
    email = models.EmailField(db_column='Correo', max_length=254) # Usar EmailField para validación
    # contraseña = models.CharField(db_column='Contraseña', max_length=50, db_collation='Modern_Spanish_CI_AS') # Ya no se usa para auth
    is_active = models.BooleanField(db_column='Estado', default=True) # Mapeado a 'Estado'
    rolid = models.ForeignKey(Roles, models.DO_NOTHING, db_column='RolId') # Relación con Roles


    # Configuración para el sistema de autenticación
    USERNAME_FIELD = 'ussername'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email'] # Campos pedidos por createsuperuser

    objects = CustomUserManager() # Usamos nuestro manager

    class Meta:
        managed = False # Seguimos sin gestionar la tabla directamente
        db_table = 'Usuarios'

    def __str__(self):
        return self.ussername


class Categoriainsumos(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS')
    estado = models.BooleanField(db_column='Estado')
    categoriainsumo = models.CharField(db_column='CategoriaInsumo', max_length=50, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'CategoriaInsumos'

class Unidadesmedida(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS')
    nombre = models.CharField(db_column='Nombre', max_length=20, db_collation='Modern_Spanish_CI_AS')
    estado = models.BooleanField(db_column='Estado')
    abreviatura = models.CharField(db_column='Abreviatura', max_length=4, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'UnidadesMedida'

class Cultivos(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS', blank=True) # Blank=True temporal si save() lo genera
    nombrecultivo = models.CharField(db_column='NombreCultivo', max_length=50, db_collation='Modern_Spanish_CI_AS')
    fechasiembra = models.DateTimeField(db_column='FechaSiembra')
    fechacosecha = models.DateTimeField(db_column='FechaCosecha', blank=True, null=True)
    area_m2 = models.DecimalField(db_column='Area_m2', max_digits=10, decimal_places=2)
    estado = models.BooleanField(db_column='Estado', default=True) # Default True
    usuarioid = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='UsuarioId')

    def save(self, *args, **kwargs):
        if not self.codigo:
            # Genera un código único de 8 caracteres si no existe
            self.codigo = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs) # Llama al método save original

    class Meta:
        managed = False
        db_table = 'Cultivos'

class Insumos(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS')
    insumo = models.CharField(db_column='Insumo', max_length=50, db_collation='Modern_Spanish_CI_AS')
    cantidad = models.DecimalField(db_column='Cantidad', max_digits=10, decimal_places=2)
    fechacaducidad = models.DateTimeField(db_column='FechaCaducidad', blank=True, null=True) # Permitir null si no aplica
    estado = models.BooleanField(db_column='Estado')
    categoriainsumoid = models.ForeignKey(Categoriainsumos, models.DO_NOTHING, db_column='CategoriaInsumoId')
    # --- CORREGIDO NOMBRE DE CAMPO Y COLUMNA ---
    unidadesmedidaid = models.ForeignKey(Unidadesmedida, models.DO_NOTHING, db_column='UnidadesMedidaId')
    # ----------------------------------------
    # NUEVO CAMPO:
    preciounitario = models.DecimalField(db_column='PrecioUnitario', max_digits=10, decimal_places=2, default=0)

    class Meta:
        managed = False
        db_table = 'Insumos'

class Mantenimientocultivos(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS')
    nombretipomantenimiento = models.CharField(db_column='NombreTipoMantenimiento', max_length=50, db_collation='Modern_Spanish_CI_AS')
    fechamantenimiento = models.DateTimeField(db_column='FechaMantenimiento')
    descripcionmantenimiento = models.CharField(db_column='DescripcionMantenimiento', max_length=400, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    estado = models.BooleanField(db_column='Estado')
    cultivoid = models.ForeignKey(Cultivos, models.CASCADE, db_column='CultivoId') # Cambiado a CASCADE
    # NUEVO CAMPO:
    costomanoobra = models.DecimalField(db_column='CostoManoObra', max_digits=10, decimal_places=2, default=0)

    class Meta:
        managed = False
        db_table = 'MantenimientoCultivos'

class Detalleinsumosusados(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    # Codigo parece ser redundante si ID es PK, y unique=True causó problemas
    # codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS')
    cantidadusada = models.DecimalField(db_column='CantidadUsada', max_digits=10, decimal_places=2)
    estado = models.BooleanField(db_column='Estado')
    insumosid = models.ForeignKey('Insumos', models.DO_NOTHING, db_column='InsumosId') # Considerar si debe ser CASCADE o SET_NULL
    mantenimientocultivosid = models.ForeignKey('Mantenimientocultivos', models.CASCADE, db_column='MantenimientoCultivosId') # CASCADE tiene sentido aquí

    class Meta:
        managed = False
        db_table = 'DetalleInsumosUsados'


class Suelos(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS')
    nombre = models.CharField(db_column='Nombre', max_length=30, db_collation='Modern_Spanish_CI_AS')
    area_m2 = models.DecimalField(db_column='Area_m2', max_digits=10, decimal_places=2)
    estado = models.BooleanField(db_column='Estado')
    usuarioid = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='UsuarioId')

    class Meta:
        managed = False
        db_table = 'Suelos'

class Monitoreosuelos(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS')
    humedad = models.DecimalField(db_column='Humedad', max_digits=5, decimal_places=2)
    ph = models.DecimalField(db_column='pH', max_digits=4, decimal_places=2)
    nitrogeno = models.DecimalField(db_column='Nitrogeno', max_digits=4, decimal_places=2, blank=True, null=True)
    fechamonitoreo = models.DateTimeField(db_column='FechaMonitoreo')
    estado = models.BooleanField(db_column='Estado')
    suelosid = models.ForeignKey('Suelos', models.DO_NOTHING, db_column='SuelosId', blank=True, null=True) # O CASCADE?

    class Meta:
        managed = False
        db_table = 'MonitoreoSuelos'


class Suelos_Cultivos(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    # Codigo parece ser redundante si ID es PK, y unique=True causó problemas
    # codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS')
    suelosid = models.ForeignKey(Suelos, models.CASCADE, db_column='SuelosId', blank=True, null=True) # CASCADE si al borrar suelo se borra relación
    estado = models.BooleanField(db_column='Estado')
    cultivosid = models.ForeignKey(Cultivos, models.CASCADE, db_column='CultivosId', blank=True, null=True) # CASCADE si al borrar cultivo se borra relación

    class Meta:
        managed = False
        db_table = 'Suelos_Cultivos'




class Cosechas(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    cultivoid = models.ForeignKey(Cultivos, models.CASCADE, db_column='CultivoId') # Si se borra cultivo, se borra cosecha
    fechacosecha = models.DateTimeField(db_column='FechaCosecha')
    cantidadrecogida = models.DecimalField(db_column='CantidadRecogida', max_digits=10, decimal_places=2)
    unidadmedidaid = models.ForeignKey(Unidadesmedida, models.DO_NOTHING, db_column='UnidadMedidaId') # No borrar unidad si se borra cosecha
    calidad = models.CharField(db_column='Calidad', max_length=50, blank=True, null=True)
    observaciones = models.TextField(db_column='Observaciones', blank=True, null=True)
    estado = models.BooleanField(db_column='Estado', default=True) # Para borrado lógico

    class Meta:
        managed = False
        db_table = 'Cosechas'

class Ingresos(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    cosechaid = models.ForeignKey(Cosechas, models.CASCADE, db_column='CosechaId') # Si se borra cosecha, se borra ingreso
    fechaingreso = models.DateField(db_column='FechaIngreso') # Cambiado a DateField
    montoingreso = models.DecimalField(db_column='MontoIngreso', max_digits=12, decimal_places=2)
    descripcion = models.CharField(db_column='Descripcion', max_length=255, blank=True, null=True)
    estado = models.BooleanField(db_column='Estado', default=True) # Para borrado lógico

    class Meta:
        managed = False
        db_table = 'Ingresos'

class CostosCosecha(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)
    cosechaid = models.ForeignKey(Cosechas, models.CASCADE, db_column='CosechaId') # Si se borra cosecha, se borra costo
    fechacosto = models.DateField(db_column='FechaCosto') # Cambiado a DateField
    montocosto = models.DecimalField(db_column='MontoCosto', max_digits=12, decimal_places=2)
    tipocosto = models.CharField(db_column='TipoCosto', max_length=100)
    descripcion = models.CharField(db_column='Descripcion', max_length=255, blank=True, null=True)
    estado = models.BooleanField(db_column='Estado', default=True) # Para borrado lógico

    class Meta:
        managed = False
        db_table = 'CostosCosecha'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, db_collation='Modern_Spanish_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, db_collation='Modern_Spanish_CI_AS')
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, db_collation='Modern_Spanish_CI_AS')
    first_name = models.CharField(max_length=150, db_collation='Modern_Spanish_CI_AS')
    last_name = models.CharField(max_length=150, db_collation='Modern_Spanish_CI_AS')
    email = models.CharField(max_length=254, db_collation='Modern_Spanish_CI_AS')
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    object_repr = models.CharField(max_length=200, db_collation='Modern_Spanish_CI_AS')
    action_flag = models.SmallIntegerField()
    change_message = models.TextField(db_collation='Modern_Spanish_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS')
    model = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, db_collation='Modern_Spanish_CI_AS')
    name = models.CharField(max_length=255, db_collation='Modern_Spanish_CI_AS')
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40, db_collation='Modern_Spanish_CI_AS')
    session_data = models.TextField(db_collation='Modern_Spanish_CI_AS')
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128, db_collation='Modern_Spanish_CI_AS')
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)
