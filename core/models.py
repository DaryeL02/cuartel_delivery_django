from django.db import models

class Rol(models.Model):
    id_roles = models.AutoField(primary_key=True, db_column="ID_roles")
    nombre = models.CharField(max_length=50, db_column="Nombre")
    descripcion = models.CharField(max_length=200, db_column="Descripcion")
    estado = models.BooleanField(db_column="Estado")

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        ordering = ['id_roles']
        db_table = "roles"


class Usuario(models.Model):
    id_usuarios = models.AutoField(primary_key=True, db_column="ID_usuarios")
    usuario = models.CharField(max_length=30, db_column="Usuario")
    password = models.CharField(max_length=30, db_column="Password")
    fecha_modificacion = models.DateTimeField(db_column="Fecha_modificacion")
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column="Fecha_creacion")

    def __str__(self):
        return f"{self.usuario}"

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['id_usuarios']
        db_table = "usuarios"


class UsuarioRol(models.Model):
    id_usuarios_roles = models.AutoField(primary_key=True, db_column="ID_usuarios_roles")
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        db_column="ID_usuarios",
        related_name="usuarios_roles",
    )
    rol = models.ForeignKey(
        Rol,
        on_delete=models.CASCADE,
        db_column="ID_roles",
        related_name="usuarios_roles",
    )

    def __str__(self):
        return f"{self.usuario} - {self.rol}"

    class Meta:
        verbose_name = "Usuario-Rol"
        verbose_name_plural = "Usuarios-Roles"
        ordering = ['id_usuarios_roles']
        db_table = "usuarios_x_roles"


class Empleado(models.Model):
    id_empleados = models.AutoField(primary_key=True, db_column="ID_empleados")
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.DO_NOTHING,
        db_column="ID_usuarios",
        related_name="empleado",
    )
    dni = models.IntegerField(db_column="DNI")
    nombre = models.CharField(max_length=50, db_column="Nombre")
    apellido = models.CharField(max_length=50, db_column="Apellido")
    telefono = models.CharField(max_length=20, db_column="Telefono")
    domicilio = models.CharField(max_length=200, db_column="Domicilio")
    estado = models.BooleanField(db_column="Estado")
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column="Fecha_creacion")

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ['id_empleados']
        db_table = "empleados"


class Local(models.Model):
    id_locales = models.AutoField(primary_key=True, db_column="ID_locales")
    nombre = models.CharField(max_length=50, db_column="Nombre")
    direccion = models.CharField(max_length=200, db_column="Direccion")
    telefono = models.CharField(max_length=20, db_column="Telefono")
    red_social = models.CharField(max_length=50, db_column="Red_social")
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column="Fecha_creacion")

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name = "Local"
        verbose_name_plural = "Locales"
        ordering = ['id_locales']
        db_table = "locales"


class Caja(models.Model):
    id_cajas = models.AutoField(primary_key=True, db_column="ID_cajas")
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        db_column="ID_usuarios",
        related_name="cajas",
    )
    local = models.ForeignKey(
        Local,
        on_delete=models.CASCADE,
        db_column="ID_locales",
        related_name="cajas",
    )
    fecha_apertura = models.DateTimeField(db_column="Fecha_apertura")
    fecha_cierre = models.DateTimeField(
        db_column="Fecha_cierre",
        null=True,
        blank=True,
    )
    monto_apertura = models.DecimalField(
        max_digits=9, decimal_places=2, db_column="Monto_apertura"
    )
    monto_cierre = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        db_column="Monto_cierre",
        null=True,
        blank=True,
    )
    estado = models.BooleanField(db_column="Estado")

    def __str__(self):
        return f"Caja #{self.id_cajas} - {self.local}"

    class Meta:
        verbose_name = "Caja"
        verbose_name_plural = "Cajas"
        ordering = ['id_cajas']
        db_table = "cajas"


class MetodoPago(models.Model):
    id_metodos = models.AutoField(primary_key=True, db_column="ID_metodos")
    nombre = models.CharField(max_length=50, db_column="Nombre")
    descripcion = models.CharField(max_length=200, db_column="Descripcion")
    estado = models.BooleanField(db_column="Estado")

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name = "Método de pago"
        verbose_name_plural = "Métodos de pago"
        ordering = ['id_metodos']
        db_table = "metodos_pago"


class Venta(models.Model):
    id_ventas = models.AutoField(primary_key=True, db_column="ID_ventas")
    metodo = models.ForeignKey(
        MetodoPago,
        on_delete=models.PROTECT,
        db_column="ID_metodo",
        related_name="ventas",
    )
    precio_total = models.DecimalField(
        max_digits=9, decimal_places=2, db_column="Precio_total"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column="Fecha_creacion")

    def __str__(self):
        return f"Venta #{self.id_ventas} - ${self.precio_total}"

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['id_ventas']
        db_table = "ventas"


class Compra(models.Model):
    id_compras = models.AutoField(primary_key=True, db_column="ID_compras")
    metodo = models.ForeignKey(
        MetodoPago,
        on_delete=models.PROTECT,
        db_column="ID_metodos",
        related_name="compras",
    )
    proveedor = models.ForeignKey(
        "Proveedor",
        on_delete=models.SET_NULL,
        db_column="ID_proveedores",
        related_name="compras",
        null=True,
        blank=True,
    )
    precio_total = models.DecimalField(
        max_digits=9, decimal_places=2, db_column="Precio_total"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column="Fecha_creacion")

    def __str__(self):
        return f"Compra #{self.id_compras} - ${self.precio_total}"

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        ordering = ['id_compras']
        db_table = "compras"


class Categoria(models.Model):
    id_categorias = models.AutoField(primary_key=True, db_column="ID_categorias")
    nombre = models.CharField(max_length=30, db_column="Nombre")
    descripcion = models.CharField(max_length=200, db_column="Descripcion")

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['id_categorias']
        db_table = "categorias"


class Proveedor(models.Model):
    id_proveedores = models.AutoField(primary_key=True, db_column="ID_proveedores")
    nombre = models.CharField(max_length=100, db_column="Nombre")
    direccion = models.CharField(max_length=200, db_column="Direccion")
    telefono = models.CharField(max_length=20, db_column="Telefono")
    email = models.CharField(max_length=30, db_column="Email")
    cuit = models.CharField(max_length=30, db_column="CUIT")
    descripcion = models.CharField(max_length=200, db_column="Descripcion")

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['id_proveedores']
        db_table = "proveedores"


class Insumo(models.Model):
    id_insumos = models.AutoField(primary_key=True, db_column="ID_insumos")
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        db_column="ID_categorias",
        related_name="insumos",
    )
    nombre = models.CharField(max_length=50, db_column="Nombre")
    descripcion = models.CharField(max_length=200, db_column="Descripcion")
    unidad = models.CharField(max_length=10, db_column="Unidad")
    stock_actual = models.IntegerField(db_column="Stock_actual")
    stock_minimo = models.IntegerField(db_column="Stock_minimo")

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"
        ordering = ['id_insumos']
        db_table = "insumos"


class ProveedorInsumo(models.Model):
    id_proveedores_insumos = models.AutoField(
        primary_key=True,
        db_column="ID_proveedores_insumos",
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.CASCADE,
        db_column="ID_proveedores",
        related_name="proveedores_insumos",
    )
    insumo = models.ForeignKey(
        Insumo,
        on_delete=models.CASCADE,
        db_column="ID_insumos",
        related_name="proveedores_insumos",
    )

    def __str__(self):
        return f"{self.proveedor} - {self.insumo}"

    class Meta:
        verbose_name = "Proveedor-Insumo"
        verbose_name_plural = "Proveedores-Insumos"
        ordering = ['id_proveedores_insumos']
        db_table = "proveedores_x_insumos"


class Producto(models.Model):
    id_productos = models.AutoField(primary_key=True, db_column="ID_productos")
    nombre = models.CharField(max_length=100, db_column="Nombre")
    descripcion = models.CharField(max_length=200, db_column="Descripcion")
    precio_unitario = models.DecimalField(
        max_digits=9, decimal_places=2, db_column="Precio_unitario"
    )
    estado = models.BooleanField(db_column="Estado")

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['id_productos']
        db_table = "productos"


class ProductoInsumo(models.Model):
    id_productos_insumos = models.AutoField(
        primary_key=True,
        db_column="ID_productos_insumos",
    )
    insumo = models.ForeignKey(
        Insumo,
        on_delete=models.CASCADE,
        db_column="ID_insumos",
        related_name="productos_insumos",
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        db_column="ID_productos",
        related_name="productos_insumos",
    )

    def __str__(self):
        return f"{self.producto} - {self.insumo}"

    class Meta:
        verbose_name = "Producto-Insumo"
        verbose_name_plural = "Productos-Insumos"
        ordering = ['id_productos_insumos']
        db_table = "productos_x_insumos"


class DetalleVenta(models.Model):
    id_detalles_ventas = models.AutoField(
        primary_key=True,
        db_column="ID_detalles_ventas",
    )
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        db_column="ID_Ventas",
        related_name="detalles",
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        db_column="ID_Producto",
        related_name="detalles_ventas",
    )
    cantidad = models.IntegerField(db_column="Cantidad")
    subtotal = models.DecimalField(
        max_digits=9, decimal_places=2, db_column="Subtotal"
    )

    def __str__(self):
        return f"Venta #{self.venta} - {self.producto} x{self.cantidad}"

    class Meta:
        verbose_name = "Detalle de venta"
        verbose_name_plural = "Detalles de venta"
        ordering = ['id_detalles_ventas']
        db_table = "detalles_ventas"


class DetalleCompra(models.Model):
    id_detalles_compras = models.AutoField(
        primary_key=True,
        db_column="ID_detalles_compras",
    )
    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        db_column="ID_compras",
        related_name="detalles",
    )
    insumo = models.ForeignKey(
        Insumo,
        on_delete=models.PROTECT,
        db_column="ID_insumos",
        related_name="detalles_compras",
    )
    cantidad = models.IntegerField(db_column="Cantidad")
    subtotal = models.DecimalField(
        max_digits=9, decimal_places=2, db_column="Subtotal"
    )

    def __str__(self):
        return f"Compra #{self.compra} - {self.insumo} x{self.cantidad}"

    class Meta:
        verbose_name = "Detalle de compra"
        verbose_name_plural = "Detalles de compra"
        ordering = ['id_detalles_compras']
        db_table = "detalles_compras"


class Pedido(models.Model):
    class Estado(models.TextChoices):
        CANCELADO = "Cancelado", "Cancelado"
        EN_PROCESO = "En proceso", "En proceso"
        FINALIZADO = "Finalizado", "Finalizado"

    id_pedidos = models.AutoField(primary_key=True, db_column="ID_pedidos")
    empleado = models.ForeignKey(
        Empleado,
        on_delete=models.PROTECT,
        db_column="ID_empleados",
        related_name="pedidos",
    )
    cliente = models.CharField(max_length=50, db_column="Cliente")
    direccion = models.CharField(max_length=200, db_column="Direccion")
    precio_total = models.DecimalField(
        max_digits=9, decimal_places=2, db_column="Precio_total"
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        db_column="Estado",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column="Fecha_creacion")

    def __str__(self):
        return f"Pedido #{self.id_pedidos} - {self.cliente}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['id_pedidos']
        db_table = "pedidos"


class DetallePedido(models.Model):
    id_detalles_pedidos = models.AutoField(
        primary_key=True,
        db_column="ID_detalles_pedidos",
    )
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        db_column="ID_pedidos",
        related_name="detalles",
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        db_column="ID_productos",
        related_name="detalles_pedidos",
    )
    cantidad = models.IntegerField(db_column="Cantidad")
    subtotal = models.DecimalField(
        max_digits=9, decimal_places=2, db_column="Subtotal"
    )
    fecha = models.DateTimeField(db_column="Fecha")

    def __str__(self):
        return f"Pedido #{self.pedido} - {self.producto} x{self.cantidad}"

    class Meta:
        verbose_name = "Detalle de pedido"
        verbose_name_plural = "Detalles de pedido"
        ordering = ['id_detalles_pedidos']
        db_table = "detalles_pedidos"


class Menu(models.Model):
    id_menus = models.AutoField(primary_key=True, db_column="ID_menus")
    nombre = models.CharField(max_length=100, db_column="Nombre")
    estado = models.BooleanField(db_column="Estado")
    fecha_inicio = models.DateTimeField(db_column="Fecha_inicio")
    fecha_fin = models.DateTimeField(
        db_column="Fecha_fin",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name = "Menú"
        verbose_name_plural = "Menús"
        ordering = ['id_menus']
        db_table = "menus"


class DetalleMenu(models.Model):
    id_detalles_menus = models.AutoField(
        primary_key=True,
        db_column="ID_detalles_menus",
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        db_column="ID_menus",
        related_name="detalles",
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        db_column="ID_productos",
        related_name="detalles_menus",
    )
    cantidad = models.IntegerField(db_column="Cantidad")
    descuento = models.IntegerField(db_column="Descuento")

    def __str__(self):
        return f"{self.menu} - {self.producto}"

    class Meta:
        verbose_name = "Detalle de menú"
        verbose_name_plural = "Detalles de menú"
        ordering = ['id_detalles_menus']
        db_table = "detalles_menus"


class MovimientoCaja(models.Model):
    class TipoMovimiento(models.TextChoices):
        INGRESO = "ingreso", "Ingreso"
        EGRESO = "egreso", "Egreso"

    id_movimientos = models.AutoField(
        primary_key=True,
        db_column="ID_movimientos",
    )
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        db_column="ID_ventas",
        related_name="movimientos_caja",
        null=True,
        blank=True,
    )
    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        db_column="ID_compras",
        related_name="movimientos_caja",
        null=True,
        blank=True,
    )
    caja = models.ForeignKey(
        Caja,
        on_delete=models.PROTECT,
        db_column="ID_cajas",
        related_name="movimientos",
    )
    # tipo_movimiento = models.CharField(
    #     max_length=7,
    #     choices=TipoMovimiento.choices,
    #     db_column="Tipo_movimiento",
    # )
    class tipo_movimiento(models.TextChoices):
        INGRESO = "Ingreso", "Ingreso"
        EGRESO = "Egreso", "Egreso"
    
    concepto = models.CharField(max_length=50, db_column="Concepto")
    monto = models.DecimalField(
        max_digits=9, decimal_places=2, db_column="Monto"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column="Fecha_creacion")

    def __str__(self):
        return f"{self.tipo_movimiento.capitalize()} - ${self.monto}"

    class Meta:
        verbose_name = "Movimiento de caja"
        verbose_name_plural = "Movimientos de caja"
        ordering = ['id_movimientos']
        db_table = "movimientos_caja"

# class Empleado(models.Model):
#     id_empleados = models.AutoField(primary_key=True, db_column="ID_empleados")
#     usuario = models.OneToOneField(
#         Usuario,
#         on_delete=models.SET_NULL,  # 1. Cambias el comportamiento a SET_NULL
#         null=True,                  # 2. Permite que la Base de Datos guarde valores NULL
#         blank=True,                 # 3. Permite que los formularios de Django lo acepten vacío
#         db_column="ID_usuarios",
#         related_name="empleado",
#     )
