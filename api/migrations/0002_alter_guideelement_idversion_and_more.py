# Generated by Django 5.1 on 2024-08-27 16:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guideelement',
            name='idVersion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.guideversion'),
        ),
        migrations.AlterField(
            model_name='guideversion',
            name='idGuide',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.guide'),
        ),
    ]