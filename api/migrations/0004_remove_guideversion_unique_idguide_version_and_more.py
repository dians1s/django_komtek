# Generated by Django 5.1 on 2024-09-01 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_guide_options_alter_guideelement_options_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='guideversion',
            name='unique_idGuide_version',
        ),
        migrations.RemoveConstraint(
            model_name='guideversion',
            name='unique_idGuide_dateStart',
        ),
        migrations.RemoveField(
            model_name='guideversion',
            name='idGuide',
        ),
        migrations.AddField(
            model_name='guideversion',
            name='codeGuide',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.guide', verbose_name='Код справочника'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='guide',
            name='code',
            field=models.CharField(max_length=100, unique=True, verbose_name='Код справочника'),
        ),
        migrations.AlterField(
            model_name='guide',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание справочника'),
        ),
        migrations.AlterField(
            model_name='guide',
            name='name',
            field=models.CharField(max_length=300, verbose_name='Наименование справочника'),
        ),
        migrations.AlterField(
            model_name='guideversion',
            name='dateStart',
            field=models.DateField(blank=True, verbose_name='Описание справочника'),
        ),
        migrations.AlterField(
            model_name='guideversion',
            name='version',
            field=models.CharField(max_length=50, verbose_name='Версия справочника'),
        ),
        migrations.AddConstraint(
            model_name='guideversion',
            constraint=models.UniqueConstraint(fields=('codeGuide', 'version'), name='unique_codeGuide_version'),
        ),
        migrations.AddConstraint(
            model_name='guideversion',
            constraint=models.UniqueConstraint(fields=('codeGuide', 'dateStart'), name='unique_codeGuide_dateStart'),
        ),
    ]
