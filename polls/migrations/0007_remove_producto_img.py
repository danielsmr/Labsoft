# Generated by Django 2.1.3 on 2018-12-03 22:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_producto_descripcion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='img',
        ),
    ]
