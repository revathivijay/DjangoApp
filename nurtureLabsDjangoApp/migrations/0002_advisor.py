# Generated by Django 3.2.2 on 2021-05-08 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nurtureLabsDjangoApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('photo_url', models.URLField()),
            ],
        ),
    ]
