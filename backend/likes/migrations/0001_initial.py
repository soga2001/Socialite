# Generated by Django 4.0 on 2023-09-01 21:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PostLikes',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('date_liked', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_liked'],
            },
        ),
    ]
