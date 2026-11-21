from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_caja_diferencia_total_caja_digital_esperado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimientocaja',
            name='metodo',
            field=models.ForeignKey(
                blank=True,
                db_column='ID_metodos',
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='movimientos_caja',
                to='core.metodopago',
            ),
        ),
    ]
