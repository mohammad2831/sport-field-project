# Generated by Django 5.2.1 on 2025-06-13 09:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_usercategoryscore_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercategoryscore',
            name='session_key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.anonymoususerprofile', to_field='session_key', verbose_name='سشن کاربر ناشناس'),
        ),
    ]
