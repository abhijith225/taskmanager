# Generated by Django 4.2.6 on 2024-12-24 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0002_users_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskhistory',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
