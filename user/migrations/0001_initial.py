# Generated by Django 4.2.4 on 2023-08-20 19:13

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
                ('email', models.CharField(blank=True, max_length=12, null=True, unique=True, verbose_name='Почта')),
                ('first_name', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Имя')),
                ('last_name', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Фамилия')),
                ('is_active', models.BooleanField(default=True, verbose_name='активный')),
                ('is_staff', models.BooleanField(default=False, verbose_name='персонал')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='админ')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='user_groups', to='auth.group', verbose_name='Группы')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_permissions', to='auth.permission', verbose_name='Разрешения пользователя')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]