from rest_framework import serializers
from core.models import Empleado, Insumo, Producto, Usuario, Categoria, Proveedor, ProveedorInsumo, Rol, Local, UsuarioRol
from django.db import transaction

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id_roles', 'nombre']
        
class UsuarioRolSerializer(serializers.ModelSerializer):
    # Traemos el detalle completo del rol asignado en la tabla intermedia
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
        fields = ['id_usuarios', 'usuario', 'password', 'email', 'roles_asignados',]

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
    
    # @transaction.atomic es un mecanismo de seguridad de base de datos (un "seguro de vida" para tus datos). 
    # Le dice a Django: "Ejecuta todo este bloque de código junto; si algo llega a fallar a la mitad, 
    # cancela todo y vuelve atrás como si nada hubiera pasado".
    
    @transaction.atomic
    def create(self, validated_data):
        # 1. Extraer los datos que no pertenecen directamente a la tabla Empleado
        username = validated_data.pop('usuario', None)
        email = validated_data.pop('email', None)
        rol_instancia = validated_data.pop('usuario_rol', None)
        
        # Manejo del campo 'local' si llega vacío ("") desde el frontend
        if 'local' in validated_data and validated_data['local'] == "":
            validated_data['local'] = None

        # 2. Crear el Usuario de Django si se envió un 'usuario'
        nuevo_usuario = None
        if username:
            # Creamos el usuario con una contraseña por defecto (ej: DNI o genérica)
            # El frontend o el admin debería poder cambiarla después
            dni_str = str(validated_data.get('dni', '123456'))
            nuevo_usuario = Usuario.objects.create_user(
                usuario=username,
                email=email,
                password=dni_str
            )

            # 3. Asignar el Rol en la tabla intermedia (usuarios_x_roles)
            if rol_instancia:
                UsuarioRol.objects.create(usuario=nuevo_usuario, rol=rol_instancia)

        # 4. Crear el Empleado asociándole el usuario creado
        empleado = Empleado.objects.create(usuario=nuevo_usuario, **validated_data)
        return empleado

    @transaction.atomic
    def update(self, instance, validated_data):
        # 1. Extraer datos anidados
        username = validated_data.pop('usuario', None)
        email = validated_data.pop('email', None)
        rol_instancia = validated_data.pop('usuario_rol', None)

        if 'local' in validated_data and validated_data['local'] == "":
            validated_data['local'] = None

        # 2. Actualizar o crear la sección de Usuario
        if instance.usuario:
            # Si el empleado ya tiene un usuario, actualizamos su username si cambió
            if username:
                instance.usuario.usuario = username
                instance.usuario.save()
                
            if email:
                instance.usuario.email = email
                
            if username or email:
                instance.usuario.save()
            
            # Actualizar el Rol (borramos los anteriores y asignamos el nuevo)
            if rol_instancia:
                UsuarioRol.objects.filter(usuario=instance.usuario).delete()
                UsuarioRol.objects.create(usuario=instance.usuario, rol=rol_instancia)
        else:
            # Si el empleado no tenía usuario asignado y ahora se envía uno
            if username:
                dni_str = str(validated_data.get('dni', instance.dni))
                nuevo_usuario = Usuario.objects.create_user(usuario=username,  email=email, password=dni_str)
                instance.usuario = nuevo_usuario
                if rol_instancia:
                    UsuarioRol.objects.create(usuario=nuevo_usuario, rol=rol_instancia)

        # 3. Actualizar los campos propios del Empleado
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
            
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id_categorias', 'nombre']
        
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ['id_proveedores', 'nombre']
        
class ProveedorInsumoSerializer(serializers.ModelSerializer):
    proveedor = ProveedorSerializer()
    
    class Meta:
        model = ProveedorInsumo
        fields = ['id_proveedores_insumos', 'proveedor']

class InsumoSerializer(serializers.ModelSerializer):
    # Campos de Lectura (Para el GET del Frontend)
    categoria_detalle = CategoriaSerializer(read_only=True, source='categoria')
    proveedores_asociados = ProveedorInsumoSerializer(many=True, read_only=True, source='proveedores_insumos')

    # Campos de Escritura (Para el POST/PUT del Frontend)
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())
    proveedor = serializers.PrimaryKeyRelatedField(queryset=Proveedor.objects.all(), write_only=True, required=False)

    class Meta:
        model = Insumo
        fields = [
            'id_insumos', 
            'nombre', 
            'descripcion', 
            'unidad', 
            'stock_actual', 
            'stock_minimo', 
            'categoria',            # Escribir ID
            'proveedor',            # Escribir ID
            'categoria_detalle',    # Leer Objeto
            'proveedores_asociados' # Leer Lista
        ]

    def create(self, validated_data):
        proveedor_instancia = validated_data.pop('proveedor', None)
        insumo = Insumo.objects.create(**validated_data)
        if proveedor_instancia:
            ProveedorInsumo.objects.create(insumo=insumo, proveedor=proveedor_instancia)
        return insumo

    def update(self, instance, validated_data):
        proveedor_instancia = validated_data.pop('proveedor', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if proveedor_instancia is not None:
            ProveedorInsumo.objects.filter(insumo=instance).delete()
            ProveedorInsumo.objects.create(insumo=instance, proveedor=proveedor_instancia)
        return instance

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'





