from django.contrib import admin

from django.contrib import admin
from .models import (
    Rol, Usuario, UsuarioRol, Empleado, Local, Caja, 
    MetodoPago, Venta, Compra, Categoria, Proveedor, 
    Insumo, ProveedorInsumo, Producto, ProductoInsumo, 
    DetalleVenta, DetalleCompra, Pedido, DetallePedido, 
    Menu, DetalleMenu, MovimientoCaja
)

# --- CONFIGURACIONES PERSONALIZADAS PARA SECCIONES PRINCIPALES ---

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuarios', 'usuario', 'fecha_creacion', 'fecha_modificacion')
    search_fields = ('usuario',)
    list_filter = ('fecha_creacion',)

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id_empleados', 'apellido', 'nombre', 'dni', 'telefono', 'estado')
    search_fields = ('apellido', 'nombre', 'dni')
    list_filter = ('estado', 'fecha_creacion')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_productos', 'nombre', 'precio_unitario', 'estado')
    search_fields = ('nombre',)
    list_filter = ('estado',)

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('id_insumos', 'nombre', 'categoria', 'stock_actual', 'stock_minimo', 'unidad')
    search_fields = ('nombre',)
    list_filter = ('categoria', 'unidad')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id_pedidos', 'cliente', 'empleado', 'precio_total', 'estado', 'fecha_creacion')
    search_fields = ('cliente', 'empleado__apellido')
    list_filter = ('estado', 'fecha_creacion')

@admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    list_display = ('id_cajas', 'local', 'usuario', 'monto_apertura', 'monto_cierre', 'estado')
    list_filter = ('estado', 'local')

# --- REGISTROS SIMPLES PARA TABLAS SECUNDARIAS O DE RELACIÓN ---

admin.site.register(Rol)
admin.site.register(UsuarioRol)
admin.site.register(Local)
admin.site.register(MetodoPago)
admin.site.register(Venta)
admin.site.register(Compra)
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(ProveedorInsumo)
admin.site.register(ProductoInsumo)
admin.site.register(DetalleVenta)
admin.site.register(DetalleCompra)
admin.site.register(DetallePedido)
admin.site.register(Menu)
admin.site.register(DetalleMenu)
admin.site.register(MovimientoCaja)
