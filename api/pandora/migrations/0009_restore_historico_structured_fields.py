# Generated during history screen integration on 2026-05-18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pandora', '0008_analisellm_usuario_consulta'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicoos',
            name='campo_alterado',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='historicoos',
            name='valor_anterior',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='historicoos',
            name='valor_novo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterModelOptions(
            name='historicoos',
            options={
                'ordering': ['-data_modificacao'],
                'verbose_name': 'Historico de OS',
                'verbose_name_plural': 'Historicos de OS',
            },
        ),
    ]
