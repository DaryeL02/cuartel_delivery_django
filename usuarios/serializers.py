from rest_framework import serializers
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

    class Meta:
        model = Usuario
        fields = ['id_usuarios', 'usuario', 'password', 'email', 'roles_asignados']


class UsuarioSimplificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id_usuarios', 'usuario']


class EmpleadoSimplificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = [
            'id_empleados',
            'nombre',
            'apellido'
        ]


class EmpleadoSerializer(serializers.ModelSerializer):
    local_detalle = LocalSerializer(read_only=True, source='local')
    usuario_detalle = UsuarioSerializer(read_only=True, source='usuario')

    local = serializers.PrimaryKeyRelatedField(queryset=Local.objects.all(), required=False, allow_null=True)
    rol = serializers.PrimaryKeyRelatedField(queryset=Rol.objects.all(), source='usuario_rol', required=False, allow_null=True)
    usuario = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

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
            'local',
            'rol',
            'usuario',
            'email',
        ]

    @transaction.atomic
    def create(self, validated_data):
        username = validated_data.pop('usuario', None)
        email = validated_data.pop('email', None)
        rol_instancia = validated_data.pop('usuario_rol', None)

        if 'local' in validated_data and validated_data['local'] == "":
            validated_data['local'] = None

        nuevo_usuario = None
        if username:
            dni_str = str(validated_data.get('dni', '123456'))
            nuevo_usuario = Usuario.objects.create_user(
                usuario=username,
                email=email,
                password=dni_str
            )

            if rol_instancia:
                UsuarioRol.objects.create(usuario=nuevo_usuario, rol=rol_instancia)

        empleado = Empleado.objects.create(usuario=nuevo_usuario, **validated_data)
        return empleado

    @transaction.atomic
    def update(self, instance, validated_data):
        username = validated_data.pop('usuario', None)
        email = validated_data.pop('email', None)
        rol_instancia = validated_data.pop('usuario_rol', None)

        if 'local' in validated_data and validated_data['local'] == "":
            validated_data['local'] = None

        if instance.usuario:
            if username:
                instance.usuario.usuario = username

            if email:
                instance.usuario.email = email

            if username or email:
                instance.usuario.save()

            if rol_instancia:
                UsuarioRol.objects.filter(usuario=instance.usuario).delete()
                UsuarioRol.objects.create(usuario=instance.usuario, rol=rol_instancia)
        else:
            if username:
                dni_str = str(validated_data.get('dni', instance.dni))
                nuevo_usuario = Usuario.objects.create_user(
                    usuario=username,
                    email=email,
                    password=dni_str
                )
                instance.usuario = nuevo_usuario
                if rol_instancia:
                    UsuarioRol.objects.create(usuario=nuevo_usuario, rol=rol_instancia)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
