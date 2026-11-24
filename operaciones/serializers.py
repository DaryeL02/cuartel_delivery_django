from rest_framework import serializers
from django.db import transaction
from core.models import (
    Pedido,
    DetallePedido,
    DetalleMenu,
    Venta,
    DetalleVenta,
    MetodoPago,
    Producto,
    Bebida,
    Menu,
    Empleado,
    Caja,
    MovimientoCaja,
)
from usuarios.serializers import EmpleadoSimplificadoSerializer
from catalogo.serializers import ProductoSerializer
from inventario.serializers import BebidaSerializer
from .stock import (
    calcular_precio_menu,
    descontar_stock_articulo,
    descontar_stock_menu,
)


class MenuComponenteSerializer(serializers.ModelSerializer):
    producto = serializers.SerializerMethodField()
    bebida = serializers.SerializerMethodField()

    class Meta:
        model = DetalleMenu
        fields = ['id_detalles_menus', 'cantidad', 'descuento', 'producto', 'bebida']

    def get_producto(self, obj):
        return {'nombre': obj.producto.nombre} if obj.producto_id else None

    def get_bebida(self, obj):
        return {'nombre': obj.bebida.nombre} if obj.bebida_id else None


class MenuContenidoSerializer(serializers.ModelSerializer):
    detalles = MenuComponenteSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = ['id_menus', 'nombre', 'detalles']


# --------------------------------- #
#              PEDIDOS              #
# --------------------------------- #

class DetallePedidoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)
    bebida = BebidaSerializer(read_only=True)
    menu = MenuContenidoSerializer(read_only=True)

    class Meta:
        model = DetallePedido
        fields = [
            'id_detalles_pedidos',
            'cantidad',
            'subtotal',
            'producto',
            'bebida',
            'menu',
        ]


class PedidoEscrituraDetalleSerializer(serializers.Serializer):
    id_productos = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(), required=False, allow_null=True
    )
    id_bebidas = serializers.PrimaryKeyRelatedField(
        queryset=Bebida.objects.all(), required=False, allow_null=True
    )
    id_menus = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.all(), required=False, allow_null=True
    )
    cantidad = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        articulos = [attrs.get(campo) for campo in ('id_productos', 'id_bebidas', 'id_menus')]
        if sum(articulo is not None for articulo in articulos) != 1:
            raise serializers.ValidationError(
                'Cada detalle debe indicar exactamente un producto, una bebida o un menú.'
            )
        menu = attrs.get('id_menus')
        if menu and not menu.estado:
            raise serializers.ValidationError({'id_menus': 'Solo se pueden agregar menús activos.'})
        return attrs


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
            'detalles',
        ]

    @transaction.atomic
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles', [])

        pedido = Pedido.objects.create(precio_total=0, **validated_data)

        total_acumulado = 0

        for detalle in detalles_data:
            producto = detalle.get('id_productos')
            bebida = detalle.get('id_bebidas')
            menu = detalle.get('id_menus')
            cantidad = detalle['cantidad']
            articulo = producto or bebida
            subtotal = (
                calcular_precio_menu(menu) * cantidad
                if menu
                else articulo.precio_unitario * cantidad
            )

            total_acumulado += subtotal

            DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                bebida=bebida,
                menu=menu,
                cantidad=cantidad,
                subtotal=subtotal,
            )
            if menu and pedido.estado == Pedido.Estado.FINALIZADO:
                descontar_stock_menu(menu, cantidad)
            elif pedido.estado == Pedido.Estado.FINALIZADO:
                descontar_stock_articulo(
                    producto=producto,
                    bebida=bebida,
                    cantidad=cantidad,
                )

        pedido.precio_total = total_acumulado
        pedido.save()

        return pedido

    @transaction.atomic
    def update(self, instance, validated_data):
        detalles_data = validated_data.pop('detalles', None)
        finalizar = (
            instance.estado != Pedido.Estado.FINALIZADO
            and validated_data.get('estado') == Pedido.Estado.FINALIZADO
        )
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if detalles_data is not None:
            instance.detalles.all().delete()
            total_acumulado = 0
            for detalle in detalles_data:
                producto = detalle.get('id_productos')
                bebida = detalle.get('id_bebidas')
                menu = detalle.get('id_menus')
                cantidad = detalle['cantidad']
                articulo = producto or bebida
                subtotal = (
                    calcular_precio_menu(menu) * cantidad
                    if menu
                    else articulo.precio_unitario * cantidad
                )
                total_acumulado += subtotal
                DetallePedido.objects.create(
                    pedido=instance,
                    producto=producto,
                    bebida=bebida,
                    menu=menu,
                    cantidad=cantidad,
                    subtotal=subtotal,
                )
            instance.precio_total = total_acumulado

        instance.save()
        if finalizar:
            detalles = instance.detalles.select_related(
                'menu', 'producto', 'bebida'
            ).prefetch_related('producto__productos_insumos')
            for detalle in detalles:
                if detalle.menu_id:
                    descontar_stock_menu(detalle.menu, detalle.cantidad)
                else:
                    descontar_stock_articulo(
                        producto=detalle.producto,
                        bebida=detalle.bebida,
                        cantidad=detalle.cantidad,
                    )
        return instance


# --------------------------------- #
#               VENTAS              #
# --------------------------------- #

class DetalleVentaSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)
    bebida = BebidaSerializer(read_only=True)
    menu = MenuContenidoSerializer(read_only=True)

    class Meta:
        model = DetalleVenta
        fields = ['id_detalles_ventas', 'cantidad', 'subtotal', 'producto', 'bebida', 'menu']


class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = ['id_metodos', 'nombre']


class VentaEscrituraDetalleSerializer(serializers.Serializer):
    id_productos = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(), required=False, allow_null=True
    )
    id_bebidas = serializers.PrimaryKeyRelatedField(
        queryset=Bebida.objects.all(), required=False, allow_null=True
    )
    id_menus = serializers.PrimaryKeyRelatedField(
        queryset=Menu.objects.all(), required=False, allow_null=True
    )
    cantidad = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        articulos = [attrs.get(campo) for campo in ('id_productos', 'id_bebidas', 'id_menus')]
        if sum(articulo is not None for articulo in articulos) != 1:
            raise serializers.ValidationError(
                'Cada detalle debe indicar exactamente un producto, una bebida o un menú.'
            )
        menu = attrs.get('id_menus')
        if menu and not menu.estado:
            raise serializers.ValidationError({'id_menus': 'Solo se pueden vender menús activos.'})
        return attrs


class VentaSerializer(serializers.ModelSerializer):
    metodo_detalle = MetodoPagoSerializer(read_only=True, source='metodo')
    detalle_venta = DetalleVentaSerializer(many=True, read_only=True, source='detalles')
    caja_detalle = serializers.SerializerMethodField()

    caja = serializers.PrimaryKeyRelatedField(queryset=Caja.objects.all(), write_only=True)
    metodo = serializers.PrimaryKeyRelatedField(queryset=MetodoPago.objects.all())
    detalles = VentaEscrituraDetalleSerializer(many=True, write_only=True)

    precio_total = serializers.DecimalField(max_digits=9, decimal_places=2, read_only=True)

    class Meta:
        model = Venta
        fields = [
            'id_ventas',
            'precio_total',
            'fecha_hora_creacion',
            'metodo_detalle',
            'detalle_venta',
            'caja_detalle',
            'caja',
            'metodo',
            'detalles',
        ]

    def get_caja_detalle(self, obj):
        movimiento = next(iter(obj.movimientos_caja.all()), None)
        if movimiento is None:
            return None

        caja = movimiento.caja
        empleado = getattr(caja.usuario, 'empleado', None)
        return {
            'id_cajas': caja.id_cajas,
            'fecha_hora_apertura': caja.fecha_hora_apertura,
            'fecha_hora_cierre': caja.fecha_hora_cierre,
            'local': caja.local_id,
            'usuario': caja.usuario.usuario,
            'empleado_nombre': (
                f'{empleado.nombre} {empleado.apellido}' if empleado else None
            ),
        }

    @transaction.atomic
    def create(self, validated_data):
        caja_instancia = validated_data.pop('caja')
        detalles_data = validated_data.pop('detalles', [])

        venta = Venta.objects.create(precio_total=0, **validated_data)

        total_acumulado = 0

        for detalle in detalles_data:
            producto = detalle.get('id_productos')
            bebida = detalle.get('id_bebidas')
            menu = detalle.get('id_menus')
            cantidad = detalle['cantidad']
            articulo = producto or bebida
            subtotal = (
                calcular_precio_menu(menu) * cantidad
                if menu
                else articulo.precio_unitario * cantidad
            )

            total_acumulado += subtotal

            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                bebida=bebida,
                menu=menu,
                cantidad=cantidad,
                subtotal=subtotal,
            )
            if menu:
                descontar_stock_menu(menu, cantidad)
            else:
                descontar_stock_articulo(
                    producto=producto,
                    bebida=bebida,
                    cantidad=cantidad,
                )

        venta.precio_total = total_acumulado
        venta.save()

        MovimientoCaja.objects.create(
            venta=venta,
            caja=caja_instancia,
            tipo_movimiento=MovimientoCaja.TipoMovimiento.INGRESO,
            concepto=f"Venta #{venta.id_ventas}",
            monto=total_acumulado,
        )

        return venta
