# Generated by Django 4.0.5 on 2022-06-26 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0003_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]