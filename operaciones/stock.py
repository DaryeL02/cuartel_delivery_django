from decimal import Decimal, ROUND_HALF_UP

from rest_framework import serializers

from core.models import Bebida, DetalleMenu, Insumo, Menu, Producto


def calcular_precio_menu(menu):
    total = Decimal('0.00')
    detalles = menu.detalles.select_related('producto', 'bebida')
    for detalle in detalles:
        articulo = detalle.producto or detalle.bebida
        if articulo is None:
            continue
        factor_descuento = Decimal(100 - detalle.descuento) / Decimal(100)
        total += articulo.precio_unitario * factor_descuento * detalle.cantidad
    return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def descontar_stock_menu(menu, cantidad_menus):
    menu = Menu.objects.select_for_update().get(pk=menu.pk)
    insumos_necesarios = {}
    bebidas_necesarias = {}
    detalles = DetalleMenu.objects.filter(menu=menu).select_related(
        'producto', 'bebida'
    ).prefetch_related('producto__productos_insumos')

    multiplicador = Decimal(cantidad_menus)
    for detalle in detalles:
        cantidad = multiplicador * detalle.cantidad
        if detalle.bebida_id:
            bebidas_necesarias[detalle.bebida_id] = (
                bebidas_necesarias.get(detalle.bebida_id, Decimal('0.00')) + cantidad
            )
        elif detalle.producto_id:
            receta = detalle.producto.productos_insumos.all()
            for ingrediente in receta:
                insumos_necesarios[ingrediente.insumo_id] = (
                    insumos_necesarios.get(ingrediente.insumo_id, Decimal('0.00'))
                    + ingrediente.cantidad * cantidad
                )

    bebidas = {
        bebida.pk: bebida
        for bebida in Bebida.objects.select_for_update().filter(
            pk__in=bebidas_necesarias
        ).order_by('pk')
    }
    insumos = {
        insumo.pk: insumo
        for insumo in Insumo.objects.select_for_update().filter(
            pk__in=insumos_necesarios
        ).order_by('pk')
    }

    faltantes = []
    for bebida_id, cantidad in bebidas_necesarias.items():
        bebida = bebidas[bebida_id]
        if bebida.stock_actual < cantidad:
            faltantes.append(
                (
                    f'Stock insuficiente para la bebida: {bebida.nombre} '
                    f'(Disponible: {bebida.stock_actual}, Requerido: {cantidad})'
                )
            )

    for insumo_id, cantidad in insumos_necesarios.items():
        insumo = insumos[insumo_id]
        if insumo.stock_actual < cantidad:
            faltantes.append(
                (
                    f'Stock insuficiente para el insumo: {insumo.nombre} '
                    f'(Disponible: {insumo.stock_actual}, Requerido: {cantidad})'
                )
            )

    if faltantes:
        raise serializers.ValidationError({'detalles': faltantes})

    for bebida_id, cantidad in bebidas_necesarias.items():
        bebida = bebidas[bebida_id]
        bebida.stock_actual -= cantidad
        bebida.save(update_fields=['stock_actual'])

    for insumo_id, cantidad in insumos_necesarios.items():
        insumo = insumos[insumo_id]
        insumo.stock_actual -= cantidad
        insumo.save(update_fields=['stock_actual'])


def descontar_stock_articulo(producto=None, bebida=None, cantidad=1):
    multiplicador = Decimal(cantidad)

    if bebida is not None:
        bebida = Bebida.objects.select_for_update().get(pk=bebida.pk)
        requerido = multiplicador
        if bebida.stock_actual < requerido:
            raise serializers.ValidationError({
                'detalles': [
                    (
                        f'Stock insuficiente para la bebida: {bebida.nombre} '
                        f'(Disponible: {bebida.stock_actual}, Requerido: {requerido})'
                    )
                ]
            })
        bebida.stock_actual -= requerido
        bebida.save(update_fields=['stock_actual'])
        return

    if producto is not None:
        producto = Producto.objects.select_for_update().prefetch_related(
            'productos_insumos__insumo'
        ).get(pk=producto.pk)
        insumos_necesarios = {}
        for ingrediente in producto.productos_insumos.all():
            requerido = ingrediente.cantidad * multiplicador
            insumos_necesarios[ingrediente.insumo_id] = (
                insumos_necesarios.get(ingrediente.insumo_id, Decimal('0.00')) + requerido
            )

        insumos = {
            insumo.pk: insumo
            for insumo in Insumo.objects.select_for_update().filter(
                pk__in=insumos_necesarios
            ).order_by('pk')
        }
        faltantes = []
        for insumo_id, requerido in insumos_necesarios.items():
            insumo = insumos[insumo_id]
            if insumo.stock_actual < requerido:
                faltantes.append(
                    (
                        f'Stock insuficiente para el insumo: {insumo.nombre} '
                        f'(Disponible: {insumo.stock_actual}, Requerido: {requerido})'
                    )
                )
        if faltantes:
            raise serializers.ValidationError({'detalles': faltantes})

        for insumo_id, requerido in insumos_necesarios.items():
            insumo = insumos[insumo_id]
            insumo.stock_actual -= requerido
            insumo.save(update_fields=['stock_actual'])
