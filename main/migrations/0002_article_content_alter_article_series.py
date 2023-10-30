# Generated by Django 4.2.6 on 2023-10-27 04:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='content',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='series',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.SET_DEFAULT, to='main.articleseries', verbose_name='Series'),
        ),
    ]