# Generated by Django 4.2.5 on 2023-11-06 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('account_id', models.CharField(max_length=30, unique=True)),
                ('user_name', models.CharField(max_length=30)),
                ('tiiun_number', models.CharField(max_length=30)),
                ('garden_size', models.CharField(max_length=1)),
                ('address', models.CharField(max_length=30)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('is_active', models.BooleanField(default=True, verbose_name='active_status')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff_status')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser_status')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
