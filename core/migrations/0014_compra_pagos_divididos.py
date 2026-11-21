from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_usuario_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra',
            name='metodo',
            field=models.ForeignKey(
                blank=True,
                db_column='ID_metodos',
                null=True,
                on_delete=models.PROTECT,
                related_name='compras',
                to='core.metodopago',
            ),
        ),
        migrations.AddField(
            model_name='compra',
            name='monto_efectivo',
            field=models.DecimalField(
                db_column='Monto_efectivo',
                decimal_places=2,
                default=0,
                max_digits=9,
            ),
        ),
        migrations.AddField(
            model_name='compra',
            name='monto_transferencia',
            field=models.DecimalField(
                db_column='Monto_transferencia',
                decimal_places=2,
                default=0,
                max_digits=9,
            ),
        ),
    ]
