# Generated by Django 5.1.3 on 2024-11-21 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Anilizor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_type', models.CharField(unique=True)),
                ('price', models.FloatField()),
            ],
        ),
    ]
