# Generated by Django 3.1.3 on 2020-11-11 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_auto_20201111_2036'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='picture',
            options={'ordering': ['pub_date']},
        ),
        migrations.AlterField(
            model_name='picture',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
