# Generated by Django 5.0 on 2023-12-24 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_rename_history_gift_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gifts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField()),
                ('description', models.CharField()),
            ],
        ),
    ]
