# Generated by Django 3.1.3 on 2020-11-16 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0004_auto_20201115_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='description',
            field=models.TextField(blank=True, default='', max_length=1000, null=True),
        ),
    ]
