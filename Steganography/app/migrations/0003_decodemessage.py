# Generated by Django 5.1.4 on 2024-12-24 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_secretmessage_modifiedimage_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DecodeMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(upload_to='decode_images/')),
                ('Message', models.TextField()),
            ],
        ),
    ]