# Generated by Django 5.1.3 on 2024-11-24 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Anilizor', '0005_alter_docs_file_path_alter_users_to_docs_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docs',
            name='size',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
