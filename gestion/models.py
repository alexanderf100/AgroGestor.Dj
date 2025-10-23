# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
import uuid



class Categoriainsumos(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    estado = models.BooleanField(db_column='Estado')  # Field name made lowercase.
    categoriainsumo = models.CharField(db_column='CategoriaInsumo', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CategoriaInsumos'


class Cultivos(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nombrecultivo = models.CharField(db_column='NombreCultivo', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    fechasiembra = models.DateTimeField(db_column='FechaSiembra')  # Field name made lowercase.
    fechacosecha = models.DateTimeField(db_column='FechaCosecha', blank=True, null=True)  # Field name made lowercase.
    area_m2 = models.DecimalField(db_column='Area_m2', max_digits=10, decimal_places=2)  # Field name made lowercase.
    estado = models.BooleanField(db_column='Estado')  # Field name made lowercase.
    usuarioid = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='UsuarioId')  # Field name made lowercase.

    def save(self, *args, **kwargs):
        # Si el objeto no tiene un código
        if not self.codigo:
            # Genera un código único de 8 caracteres en mayúsculas
            self.codigo = uuid.uuid4().hex[:8].upper()
        # Llama al método de guardado
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'Cultivos'


class Detalleinsumosusados(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', max_length=8, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    cantidadusada = models.DecimalField(db_column='CantidadUsada', max_digits=10, decimal_places=2)  # Field name made lowercase.
    estado = models.BooleanField(db_column='Estado')  # Field name made lowercase.
    insumosid = models.ForeignKey('Insumos', models.DO_NOTHING, db_column='InsumosId')  # Field name made lowercase.
    mantenimientocultivosid = models.ForeignKey('Mantenimientocultivos', models.DO_NOTHING, db_column='MantenimientoCultivosId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DetalleInsumosUsados'


class Insumos(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    insumo = models.CharField(db_column='Insumo', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    cantidad = models.DecimalField(db_column='Cantidad', max_digits=10, decimal_places=2)  # Field name made lowercase.
    fechacaducidad = models.DateTimeField(db_column='FechaCaducidad')  # Field name made lowercase.
    estado = models.BooleanField(db_column='Estado')  # Field name made lowercase.
    categoriainsumoid = models.ForeignKey(Categoriainsumos, models.DO_NOTHING, db_column='CategoriaInsumoId')  # Field name made lowercase.
    inidadesmedidaid = models.ForeignKey('Unidadesmedida', models.DO_NOTHING, db_column='InidadesMedidaId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Insumos'


class Mantenimientocultivos(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nombretipomantenimiento = models.CharField(db_column='NombreTipoMantenimiento', max_length=50, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    fechamantenimiento = models.DateTimeField(db_column='FechaMantenimiento')  # Field name made lowercase.
    descripcionmantenimiento = models.CharField(db_column='DescripcionMantenimiento', max_length=400, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    estado = models.BooleanField(db_column='Estado')  # Field name made lowercase.
    cultivoid = models.ForeignKey(Cultivos, models.DO_NOTHING, db_column='CultivoId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MantenimientoCultivos'


class Monitoreosuelos(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    humedad = models.DecimalField(db_column='Humedad', max_digits=5, decimal_places=2)  # Field name made lowercase.
    ph = models.DecimalField(db_column='pH', max_digits=4, decimal_places=2)  # Field name made lowercase.
    nitrogeno = models.DecimalField(db_column='Nitrogeno', max_digits=4, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    fechamonitoreo = models.DateTimeField(db_column='FechaMonitoreo')  # Field name made lowercase.
    estado = models.BooleanField(db_column='Estado')  # Field name made lowercase.
    suelosid = models.ForeignKey('Suelos', models.DO_NOTHING, db_column='SuelosId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MonitoreoSuelos'


class Roles(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    rol = models.CharField(db_column='Rol', max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    descripcionrol = models.CharField(db_column='DescripcionRol', max_length=150, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)  # Field name made lowercase.
    estado = models.BooleanField(db_column='Estado')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Roles'


class Suelos(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=30, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    area_m2 = models.DecimalField(db_column='Area_m2', max_digits=10, decimal_places=2)  # Field name made lowercase.
    estado = models.BooleanField(db_column='Estado')  # Field name made lowercase.
    usuarioid = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='UsuarioId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Suelos'


class Suelos_Cultivos(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    suelosid = models.ForeignKey(Suelos, models.DO_NOTHING, db_column='SuelosId', blank=True, null=True)  # Field name made lowercase.
    estado = models.BooleanField(db_column='Estado')  # Field name made lowercase.
    cultivosid = models.ForeignKey(Cultivos, models.DO_NOTHING, db_column='CultivosId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Suelos_Cultivos'


class Unidadesmedida(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=20, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.
    estado = models.BooleanField(db_column='Estado')  # Field name made lowercase.
    abreviatura = models.CharField(db_column='Abreviatura', max_length=4, db_collation='Modern_Spanish_CI_AS')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UnidadesMedida'

# EN gestion/models.py

# EN gestion/models.py

class CustomUserManager(BaseUserManager):
    """
    Manager personalizado para nuestro modelo de usuario con ussername como identificador.
    """
    def create_user(self, ussername, email, password=None, **extra_fields):
        if not ussername:
            raise ValueError('El campo Ussername es obligatorio')
        email = self.normalize_email(email)
        user = self.model(ussername=ussername, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, ussername, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # --- LÓGICA AÑADIDA PARA ASIGNAR EL ROL ---
        try:
            # Busca el rol de Administrador en la tabla Roles
            admin_role = Roles.objects.get(rol='Administrador')
            # Lo añade a los campos que se van a guardar
            extra_fields['rolid'] = admin_role
        except Roles.DoesNotExist:
            raise ValueError(
                "El rol 'Administrador' no existe en la base de datos. "
                "Por favor, créalo antes de crear un superusuario."
            )
        # -------------------------------------------

        return self.create_user(ussername, email, password, **extra_fields)


class Usuarios(AbstractUser):
    # 1. Desactivamos el 'username' por defecto de AbstractUser
    username = None

    # 2. Definimos tus campos, asegurándonos de que coincidan con la base de datos
    #    y le decimos a AbstractUser cuáles usar.
    id = models.AutoField(db_column='Id', primary_key=True)
    codigo = models.CharField(db_column='Codigo', unique=True, max_length=8, db_collation='Modern_Spanish_CI_AS')

    # Mapeamos los campos de AbstractUser a tus columnas de la BD
    first_name = models.CharField(db_column='Nombre', max_length=40, db_collation='Modern_Spanish_CI_AS')
    last_name = models.CharField(db_column='Apellido', max_length=50, db_collation='Modern_Spanish_CI_AS')
    ussername = models.CharField(db_column='UsserName', unique=True, max_length=20, db_collation='Modern_Spanish_CI_AS')
    email = models.CharField(db_column='Correo', max_length=30, db_collation='Modern_Spanish_CI_AS')

    # El campo 'contraseña' de tu BD ya no será usado por el sistema de auth seguro de Django.
    # Django usará su propio campo 'password' internamente. Lo dejamos aquí para que el modelo no dé error,
    # pero no lo usaremos para el login.
    contraseña = models.CharField(db_column='Contraseña', max_length=50, db_collation='Modern_Spanish_CI_AS')

    # Mapeamos 'estado' a 'is_active' de AbstractUser
    is_active = models.BooleanField(db_column='Estado', default=True)

    # Tu campo de relación
    rolid = models.ForeignKey(Roles, models.DO_NOTHING, db_column='RolId')

    # 3. Le decimos al sistema de autenticación cuál es el campo de login
    USERNAME_FIELD = 'ussername'

    # 4. Campos requeridos al usar 'createsuperuser'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = CustomUserManager()


    class Meta:
        managed = False
        db_table = 'Usuarios'

    def __str__(self):
        return self.ussername

    class Meta:
        managed = False
        db_table = 'Usuarios'


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
