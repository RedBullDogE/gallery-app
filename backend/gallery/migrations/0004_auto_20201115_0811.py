# Generated by Django 3.1.3 on 2020-11-15 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_auto_20201111_2039'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='picture',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AddField(
            model_name='picture',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='pictures/thumbs'),
        ),
    ]
