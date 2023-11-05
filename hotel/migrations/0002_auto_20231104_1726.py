# Generated by Django 3.2.22 on 2023-11-04 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkin',
            name='empleado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empleado_checkin', to='hotel.empleado'),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='estancia',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='estancia_checkin', to='hotel.estancia'),
        ),
        migrations.AlterField(
            model_name='checkout',
            name='empleado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empleado_checkout', to='hotel.empleado'),
        ),
        migrations.AlterField(
            model_name='checkout',
            name='estancia',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='estancia_checkout', to='hotel.estancia'),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente_comentario', to='hotel.cliente'),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='habitacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habitacion_comentario', to='hotel.habitacion'),
        ),
        migrations.AlterField(
            model_name='comodidad',
            name='habitacion',
            field=models.ManyToManyField(related_name='habitacion_comodidad', through='hotel.HabitacionComodidad', to='hotel.Habitacion'),
        ),
        migrations.AlterField(
            model_name='estancia',
            name='reserva',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reserva_estancia', to='hotel.reserva'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente_reserva', to='hotel.cliente'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='habitacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habitacion_reserva', to='hotel.habitacion'),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='reserva',
            field=models.ManyToManyField(related_name='reserva_servicio', through='hotel.ReservaServicio', to='hotel.Reserva'),
        ),
    ]