# Generated by Django 4.1.7 on 2023-03-15 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trashimages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='b64_img',
            field=models.CharField(max_length=9000000000, null=True),
        ),
    ]