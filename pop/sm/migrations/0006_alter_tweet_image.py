# Generated by Django 3.2 on 2021-04-21 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sm', '0005_alter_tweet_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='images/'),
        ),
    ]
