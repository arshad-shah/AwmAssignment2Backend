# Generated by Django 4.1.3 on 2022-12-06 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MosqueFinder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
            ],
        ),
    ]