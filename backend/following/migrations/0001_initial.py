# Generated by Django 4.0.6 on 2023-03-20 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserFollowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed_date', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'ordering': ['-followed_date'],
            },
        ),
    ]
