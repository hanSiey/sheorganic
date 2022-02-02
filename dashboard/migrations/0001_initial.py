# Generated by Django 3.2.4 on 2022-02-01 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Distributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=20, null=True)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('area_of_operation', models.CharField(max_length=200)),
                ('status', models.CharField(blank=True, choices=[('Active', 'Active'), ('Not Available', 'Not Available')], default='Active', max_length=20, null=True)),
            ],
        ),
    ]
