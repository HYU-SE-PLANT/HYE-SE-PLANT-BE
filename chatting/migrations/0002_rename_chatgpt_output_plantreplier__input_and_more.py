# Generated by Django 4.2.5 on 2023-10-20 18:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatting', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plantreplier',
            old_name='chatgpt_output',
            new_name='_input',
        ),
        migrations.RenameField(
            model_name='plantreplier',
            old_name='user_input',
            new_name='_output',
        ),
    ]
