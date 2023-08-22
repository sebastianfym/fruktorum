from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Permission, Group
from django.db import models
from django.db import transaction


class UserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                if password:
                    user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(
        Group,
        verbose_name='Группы',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='user_groups'  # Добавить это поле
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='Разрешения пользователя',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='user_permissions'  # Добавить это поле
    )
    email = models.CharField(max_length=50, blank=True, null=True, verbose_name='Почта', unique=True)
    first_name = models.CharField(max_length=20, blank=True, null=True, verbose_name='Имя', unique=True)
    last_name = models.CharField(max_length=20, blank=True, null=True, verbose_name='Фамилия', unique=True)

    is_active = models.BooleanField(default=True, verbose_name="активный")
    is_staff = models.BooleanField(default=False, verbose_name="персонал")
    is_superuser = models.BooleanField(default=False, verbose_name="админ")
    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return f'{self.email}, {self.first_name}, {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
