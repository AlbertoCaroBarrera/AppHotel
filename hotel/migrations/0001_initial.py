# Generated by Django 3.2.22 on 2023-11-20 20:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('correo_electronico', models.EmailField(max_length=254)),
                ('telefono', models.IntegerField()),
                ('direccion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Comodidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('cargo', models.CharField(choices=[('Bo', 'Botones'), ('Re', 'Recepcionista'), ('Se', 'Servicio de habitaciones'), ('At', 'Atencion al cliente'), ('Gp', 'Gestion y protocolo')], default='Bo', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('hora_inicio', models.DateTimeField(default=django.utils.timezone.now)),
                ('hora_final', models.DateTimeField(default=django.utils.timezone.now)),
                ('ubicacion', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Habitacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_hab', models.IntegerField()),
                ('tipo', models.CharField(max_length=200)),
                ('precio_noche', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_entrada', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_salida', models.DateTimeField(default=django.utils.timezone.now)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente_reserva', to='hotel.cliente')),
                ('habitacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habitacion_reserva', to='hotel.habitacion')),
            ],
        ),
        migrations.CreateModel(
            name='ReservaServicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(null=True)),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.reserva')),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('precio', models.FloatField()),
                ('reserva', models.ManyToManyField(related_name='reserva_servicio', through='hotel.ReservaServicio', to='hotel.Reserva')),
            ],
        ),
        migrations.AddField(
            model_name='reservaservicio',
            name='servicio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.servicio'),
        ),
        migrations.CreateModel(
            name='ReservaEvento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.evento')),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.reserva')),
            ],
        ),
        migrations.CreateModel(
            name='Puntuacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuacion', models.IntegerField()),
                ('comentario', models.TextField()),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente_puntuacion', to='hotel.cliente')),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evento_puntuacion', to='hotel.evento')),
            ],
        ),
        migrations.CreateModel(
            name='HabitacionComodidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comodidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.comodidad')),
                ('habitacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.habitacion')),
            ],
        ),
        migrations.AddField(
            model_name='evento',
            name='reserva',
            field=models.ManyToManyField(related_name='reserva_evento', through='hotel.ReservaEvento', to='hotel.Reserva'),
        ),
        migrations.CreateModel(
            name='Estancia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_llegada', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_salida', models.DateTimeField(default=django.utils.timezone.now)),
                ('reserva', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reserva_estancia', to='hotel.reserva')),
            ],
        ),
        migrations.CreateModel(
            name='CuentaBancaria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('Ca', 'Caixa'), ('BB', 'BBVA'), ('Un', 'UNICAJA'), ('In', 'ING')], default='Ca', max_length=2)),
                ('numero_cuenta', models.IntegerField()),
                ('cliente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hotel.cliente')),
            ],
        ),
        migrations.AddField(
            model_name='comodidad',
            name='habitacion',
            field=models.ManyToManyField(related_name='habitacion_comodidad', through='hotel.HabitacionComodidad', to='hotel.Habitacion'),
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puntuacion', models.IntegerField()),
                ('comentario', models.TextField()),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente_comentario', to='hotel.cliente')),
                ('habitacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habitacion_comentario', to='hotel.habitacion')),
            ],
        ),
        migrations.CreateModel(
            name='CheckOut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora_check_out', models.DateTimeField(default=django.utils.timezone.now)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empleado_checkout', to='hotel.empleado')),
                ('estancia', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='estancia_checkout', to='hotel.estancia')),
            ],
        ),
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora_check_in', models.DateTimeField(default=django.utils.timezone.now)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empleado_checkin', to='hotel.empleado')),
                ('estancia', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='estancia_checkin', to='hotel.estancia')),
            ],
        ),
    ]
