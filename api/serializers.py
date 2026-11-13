from rest_framework import serializers
from core.models import *
from django.db import transaction
from django.utils import timezone

# --------------------------------- #
#        USUARIOS/EMPLEADOS         #
# --------------------------------- #

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

class UsuarioSimplificadoSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Usuario
        fields = ['id_usuarios', 'usuario']

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
     
# --------------------------------- #
#              INSUMOS              #
# --------------------------------- #   
            
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

# --------------------------------- #
#             PRODUCTOS             #
# --------------------------------- #

class InsumoSimplificadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Insumo
        fields = [
            'id_insumos', 
            'nombre'
        ]

class ProductoInsumoSerializer(serializers.ModelSerializer):

    insumo = InsumoSimplificadoSerializer()
    
    class Meta:
        model = ProductoInsumo
        fields = ['id_productos_insumos', 'insumo']

class ProductoEscrituraDetalleSerializer(serializers.Serializer):
    id_insumos = serializers.PrimaryKeyRelatedField(queryset=Insumo.objects.all())
    
class ProductoSerializer(serializers.ModelSerializer):

    insumos_asociados = ProductoInsumoSerializer(many=True, read_only=True, source='productos_insumos')
      
    
    insumos = ProductoEscrituraDetalleSerializer(many=True, write_only=True)
    
    precio_unitario = serializers.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        model = Producto
        fields = [
            'id_productos', 
            'nombre', 
            'descripcion', 
            'precio_unitario', 
            'estado',
            'insumos_asociados',
            'insumos',
            ]
        
    @transaction.atomic
    def create(self, validated_data):
        # 1. Extraemos los insumos de la petición
        insumos_data = validated_data.pop('insumos', [])

        # 2. Creamos el producto principal con los datos restantes (nombre, precio, estado, etc.)
        nuevo_producto = Producto.objects.create(**validated_data)
        
        # 3. Iteramos de forma limpia por cada insumo enviado
        for item in insumos_data:
            # Obtenemos la instancia real del modelo Insumo provista por el PrimaryKeyRelatedField
            insumo_instancia = item['id_insumos']
            
            # 4. Creamos el registro en la tabla intermedia asociando las dos instancias reales
            ProductoInsumo.objects.create(
                producto=nuevo_producto,
                insumo=insumo_instancia
            )

        # Retornamos el objeto Producto que espera recibir Django REST Framework
        return nuevo_producto
    
    @transaction.atomic
    def update(self, instance, validated_data):
        # 1. Extraer los nuevos insumos de los datos validados (si se enviaron)
        # Si no se envían insumos en el PUT/PATCH, dejamos None para no borrar los existentes por error
        insumos_data = validated_data.pop('insumos', None)

        # 2. Actualizar los campos propios del Producto (nombre, precio_unitario, estado, descripcion)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 3. Si se envió la lista de insumos, sincronizamos la tabla intermedia
        if insumos_data is not None:
            # Borramos las relaciones viejas de este producto en productos_x_insumos
            ProductoInsumo.objects.filter(producto=instance).delete()
            
            # Creamos las nuevas relaciones
            for item in insumos_data:
                insumo_instancia = item['id_insumos']
                ProductoInsumo.objects.create(
                    producto=instance,
                    insumo=insumo_instancia
                )

        return instance
        
    

# --------------------------------- #
#               MENÚS               #
# --------------------------------- #

class DetalleMenuSerializer(serializers.ModelSerializer):
    
    producto = ProductoSerializer()
    
    class Meta:
        model = DetalleMenu
        fields = [
            'id_detalles_menus',
            'cantidad', 
            'descuento', 
            'producto'
            ]

class MenuSerializer(serializers.ModelSerializer):
    
    detalle_menu = DetalleMenuSerializer(many=True, read_only=True, source='detalles')
    
    class Meta:
        model = Menu
        fields = [
            'id_menus', 
            'nombre', 
            'estado',
            'detalle_menu'
            ]

# --------------------------------- #
#               CAJAS               #
# --------------------------------- #

class EmpleadoSimplificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = [
            'id_empleados', 
            'nombre',
            'apellido'
            ]
        
class MovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoCaja
        fields = [
            'id_movimientos',
            'tipo_movimiento',
            'concepto',
            'monto'
            ]

class CajaSerializer(serializers.ModelSerializer):
    
    movimientos_asociados = MovimientoSerializer(many=True, read_only=True, source='movimientos')
    
    empleado_detalle = EmpleadoSimplificadoSerializer(read_only=True, source='usuario.empleado')
    
    caja = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Caja
        fields = [
            'id_cajas',
            'fecha_hora_apertura',
            'fecha_hora_cierre',
            'monto_apertura',
            'monto_cierre',
            'estado',
            'movimientos_asociados',
            'empleado_detalle',
            'usuario',
            'local',
            'caja'
            ]
        extra_kwargs = {
            'usuario': {'required': False},
            'local': {'required': False},
            'monto_apertura': {'required': False},
            
        }
        
    @transaction.atomic
    def create(self, validated_data):

        nueva_caja = Caja.objects.create(**validated_data)
    
        return nueva_caja
    
    @transaction.atomic
    def update(self, instance, validated_data):
        
        validated_data.pop('caja', None)

        # 2. Actualizar los campos propios del Producto (nombre, precio_unitario, estado, descripcion)
        instance.fecha_hora_cierre = timezone.now()
        instance.estado = False
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()

        return instance

# --------------------------------- #
#              PEDIDOS              #
# --------------------------------- #


class DetallePedidoSerializer(serializers.ModelSerializer):
    
    producto = ProductoSerializer()
    
    class Meta:
        model = DetallePedido
        fields = [
            'id_detalles_pedidos',
            'cantidad', 
            'subtotal', 
            'producto'
            ]
    
class PedidoEscrituraDetalleSerializer(serializers.Serializer):
    id_productos = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
    cantidad = serializers.IntegerField()
    
class PedidoSerializer(serializers.ModelSerializer):

    # Campos de lectura (GET)
    empleado_detalle = EmpleadoSimplificadoSerializer(read_only=True, source='empleado')    
    pedido_detalle = DetallePedidoSerializer(many=True, read_only=True, source='detalles')

    # Campos de escritura (POST)
    empleado = serializers.PrimaryKeyRelatedField(queryset=Empleado.objects.all(), write_only=True)
    detalles = PedidoEscrituraDetalleSerializer(many=True, write_only=True)
    
    # Se calcula automáticamente
    precio_total = serializers.DecimalField(max_digits=9, decimal_places=2, read_only=True)
    estado = serializers.ChoiceField(choices=Pedido.Estado.choices, default=Pedido.Estado.EN_PROCESO)

    class Meta:
        model = Pedido
        fields = [
            'id_pedidos', 
            'cliente',
            'direccion', 
            'precio_total',
            'estado',
            'pagado', 
            'fecha_hora_creacion',
            'empleado_detalle',
            'pedido_detalle',
            'empleado',
            'detalles'
        ]
        
    @transaction.atomic
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles', [])
        
        # Creamos el pedido con total en 0 inicialmente
        pedido = Pedido.objects.create(precio_total=0, **validated_data)
        
        total_acumulado = 0
        
        for detalle in detalles_data:
            producto = detalle['id_productos']
            cantidad = detalle['cantidad']
            subtotal = producto.precio_unitario * cantidad
            
            total_acumulado += subtotal
            
            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                subtotal=subtotal
            )
            
        pedido.precio_total = total_acumulado
        pedido.save()
        
        return pedido

# --------------------------------- #
#               VENTAS              #
# --------------------------------- #

class ProductoSimplificadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = [
            'id_productos', 
            'nombre',
            'precio_unitario'
        ]

class DetalleVentaSerializer(serializers.ModelSerializer):
    
    producto = ProductoSerializer()
    
    class Meta:
        model = DetalleVenta
        fields = ['id_detalles_ventas', 'cantidad', 'subtotal', 'producto']

class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = ['id_metodos','nombre']

class VentaEscrituraDetalleSerializer(serializers.Serializer):
    id_productos = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
    cantidad = serializers.IntegerField()

class VentaSerializer(serializers.ModelSerializer):

    metodo_detalle = MetodoPagoSerializer(read_only=True, source='metodo')
    detalle_venta = DetalleVentaSerializer(many=True, read_only=True, source='detalles')
    
    
    caja = serializers.PrimaryKeyRelatedField(queryset=Caja.objects.all(), write_only=True)
    metodo = serializers.PrimaryKeyRelatedField(queryset=MetodoPago.objects.all())
    detalles = VentaEscrituraDetalleSerializer(many=True, write_only=True)
    
    precio_total = serializers.DecimalField(max_digits=9, decimal_places=2, read_only=True)

    class Meta:
        model = Venta
        fields = [
            'id_ventas', 
            'precio_total',
            'metodo_detalle', 
            'detalle_venta',
            'caja',    
            'metodo',
            'detalles',
        ]
        
    @transaction.atomic
    def create(self, validated_data):
        caja_instancia = validated_data.pop('caja')
        detalles_data = validated_data.pop('detalles', [])
        
        venta = Venta.objects.create(precio_total=0, **validated_data)
        
        total_acumulado = 0 # Para calcular el precio total
        
        for detalle in detalles_data:
            producto = detalle['id_productos']
            cantidad = detalle['cantidad']
            subtotal = producto.precio_unitario * cantidad

            total_acumulado += subtotal
            
            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                subtotal=subtotal
            )

        venta.precio_total = total_acumulado
        venta.save()
        
        MovimientoCaja.objects.create(
            venta=venta,
            caja=caja_instancia,
            tipo_movimiento=MovimientoCaja.TipoMovimiento.INGRESO,
            concepto=f"Venta #{venta.id_ventas}",
            monto=total_acumulado
        )


        return venta

# --------------------------------- #
#              COMPRAS              #
# --------------------------------- #

class InsumoSimplificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insumo
        fields = [
            'id_insumos', 
            'nombre'
            ]

class DetalleCompraSerializer(serializers.ModelSerializer):
    
    insumo = InsumoSimplificadoSerializer()
    
    class Meta:
        model = DetalleCompra
        fields = [
            'id_detalles_compras', 
            'cantidad', 
            'subtotal', 
            'insumo'
            ]

class CompraSerializer(serializers.ModelSerializer):

    detalle_compra = DetalleCompraSerializer(many=True, read_only=True, source='detalles')

    class Meta:
        model = Compra
        fields = [
            'id_compras', 
            'precio_total',
            'detalle_compra',
        ]





# fields = [
#             'id_cajas', 'fecha_hora_apertura', 'fecha_hora_cierre',
#             'monto_apertura', 'monto_cierre', 'estado',
#             'movimientos_asociados', 'usuario', 'local', 'caja'
#         ]
#         # Esto hace que los campos no sean obligatorios en la validación de entrada
#         extra_kwargs = {
#             'monto_apertura': {'required': False},
#             'usuario': {'required': False},
#             'local': {'required': False},
#         }