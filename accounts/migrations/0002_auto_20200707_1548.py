# Generated by Django 2.1.15 on 2020-07-07 06:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_club', to=settings.AUTH_USER_MODEL),
        ),
    ]
