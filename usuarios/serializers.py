from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.db import transaction
from core.models import Rol, UsuarioRol, Local, Usuario, Empleado


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id_roles', 'nombre']


class UsuarioRolSerializer(serializers.ModelSerializer):
    rol_detalle = RolSerializer(read_only=True, source='rol')

    class Meta:
        model = UsuarioRol
        fields = ['id_usuarios_roles', 'rol_detalle']


class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = ['id_locales', 'nombre']


class UsuarioSerializer(serializers.ModelSerializer):
    roles_asignados = UsuarioRolSerializer(many=True, read_only=True, source='usuarios_roles')
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = ['id_usuarios', 'usuario', 'password', 'email', 'roles_asignados']


class UsuarioSimplificadoSerializer(serializers.ModelSerializer):
    rol_nombre = serializers.SerializerMethodField()
    roles_nombres = serializers.SerializerMethodField()
    is_superuser = serializers.BooleanField(read_only=True)

    class Meta:
        model = Usuario
        fields = ['id_usuarios', 'usuario', 'rol_nombre', 'roles_nombres', 'is_superuser']

    def get_rol_nombre(self, obj):
        usuario_rol = obj.usuarios_roles.select_related('rol').filter(rol__estado=True).first()
        return usuario_rol.rol.nombre if usuario_rol else None

    def get_roles_nombres(self, obj):
        return list(
            obj.usuarios_roles.filter(rol__estado=True).values_list('rol__nombre', flat=True)
        )


class PerfilUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=False,
        trim_whitespace=False,
    )

    class Meta:
        model = Usuario
        fields = ['email', 'password']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class EmpleadoSimplificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = [
            'id_empleados',
            'nombre',
            'apellido'
        ]


class EmpleadoSerializer(serializers.ModelSerializer):
    dni = serializers.CharField(
        max_length=8,
        validators=[
            *Empleado._meta.get_field('dni').validators,
            UniqueValidator(
                queryset=Empleado.objects.all(),
                message='Ya existe un empleado registrado con este DNI.',
            ),
        ],
    )
    local_detalle = LocalSerializer(read_only=True, source='local')
    usuario_detalle = UsuarioSerializer(read_only=True, source='usuario')
    rol_nombre = serializers.SerializerMethodField()

    local = serializers.PrimaryKeyRelatedField(queryset=Local.objects.all(), required=False, allow_null=True)
    rol = serializers.PrimaryKeyRelatedField(queryset=Rol.objects.all(), source='usuario_rol', required=False, allow_null=True)
    usuario = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        allow_blank=False,
        trim_whitespace=False,
    )

    class Meta:
        model = Empleado
        fields = [
            'id_empleados',
            'dni',
            'nombre',
            'apellido',
            'telefono',
            'domicilio',
            'estado',
            'local_detalle',
            'usuario_detalle',
            'rol_nombre',
            'local',
            'rol',
            'usuario',
            'email',
            'password',
        ]

    def get_rol_nombre(self, obj):
        if not obj.usuario_id:
            return None
        usuario_rol = obj.usuario.usuarios_roles.select_related('rol').first()
        return usuario_rol.rol.nombre if usuario_rol else None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields['dni'].read_only = True
            self.fields['password'].required = False
            self.fields['password'].allow_blank = True

    def validate(self, attrs):
        password = attrs.get('password')
        if (
            self.instance is not None
            and not self.instance.usuario_id
            and attrs.get('usuario')
            and not password
        ):
            raise serializers.ValidationError({
                'password': 'La contraseña es obligatoria para crear las credenciales del usuario.'
            })
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        username = validated_data.pop('usuario', None)
        email = validated_data.pop('email', None)
        password = validated_data.pop('password')
        rol_instancia = validated_data.pop('usuario_rol', None)

        if 'local' in validated_data and validated_data['local'] == "":
            validated_data['local'] = None

        nuevo_usuario = Usuario.objects.create_user(
            usuario=username,
            email=email,
            password=password,
        )

        if rol_instancia:
            UsuarioRol.objects.create(usuario=nuevo_usuario, rol=rol_instancia)

        empleado = Empleado.objects.create(usuario=nuevo_usuario, **validated_data)
        return empleado

    @transaction.atomic
    def update(self, instance, validated_data):
        username = validated_data.pop('usuario', None)
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)
        rol_instancia = validated_data.pop('usuario_rol', None)

        if 'local' in validated_data and validated_data['local'] == "":
            validated_data['local'] = None

        if instance.usuario:
            if username:
                instance.usuario.usuario = username

            if email:
                instance.usuario.email = email

            if password:
                instance.usuario.set_password(password)

            if username or email or password:
                instance.usuario.save()

            if rol_instancia:
                UsuarioRol.objects.filter(usuario=instance.usuario).delete()
                UsuarioRol.objects.create(usuario=instance.usuario, rol=rol_instancia)
        else:
            if username:
                nuevo_usuario = Usuario.objects.create_user(
                    usuario=username,
                    email=email,
                    password=password,
                )
                instance.usuario = nuevo_usuario
                if rol_instancia:
                    UsuarioRol.objects.create(usuario=nuevo_usuario, rol=rol_instancia)
            elif password:
                raise serializers.ValidationError({
                    'usuario': 'Debes ingresar un usuario para establecer una contraseña.'
                })

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
