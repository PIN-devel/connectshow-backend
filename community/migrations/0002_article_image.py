# Generated by Django 2.1.15 on 2020-07-08 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]