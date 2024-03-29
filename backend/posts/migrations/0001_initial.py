# Generated by Django 4.0 on 2023-09-01 21:32

from django.db import migrations, models
import posts.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('img_url', models.FileField(blank=True, null=True, upload_to=posts.models.rename_file)),
                ('caption', models.TextField(blank=True, max_length=255, null=True)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(blank=True, default=None, null=True)),
            ],
            options={
                'ordering': ['-date_posted'],
            },
        ),
    ]
