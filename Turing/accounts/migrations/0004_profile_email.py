# Generated by Django 5.1.3 on 2024-12-10 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_profile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='2024-12-10 16:32:45', max_length=254, unique=True),
            preserve_default=False,
        ),
    ]