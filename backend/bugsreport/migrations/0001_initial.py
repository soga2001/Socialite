# Generated by Django 4.0 on 2023-08-23 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_user_is_admin_alter_user_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='BugsReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bug', models.CharField(max_length=30)),
                ('replication', models.TextField(max_length=255)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(blank=True, default=None, null=True)),
                ('resolved', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'ordering': ['-date_posted'],
            },
        ),
    ]