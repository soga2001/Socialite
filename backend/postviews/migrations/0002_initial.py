# Generated by Django 4.0 on 2023-08-27 23:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('postviews', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postviews',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_viewing', to='users.user'),
        ),
        migrations.AddConstraint(
            model_name='postviews',
            constraint=models.UniqueConstraint(fields=('post', 'user'), name='unique_views'),
        ),
    ]
