# Generated by Django 4.0.6 on 2022-12-22 05:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFollowing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followed_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('followed_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('following_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-followed_date'],
            },
        ),
        migrations.AddConstraint(
            model_name='userfollowing',
            constraint=models.UniqueConstraint(fields=('followed_user', 'following_user'), name='unique_followers'),
        ),
    ]