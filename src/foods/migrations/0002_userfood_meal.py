# Generated by Django 4.1.7 on 2023-03-14 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfood',
            name='meal',
            field=models.TextField(choices=[('breakfast', 'breakfast'), ('lunch', 'lunch'), ('dinner', 'dinner')], default='breakfast'),
        ),
    ]
