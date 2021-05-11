from django.db import models


class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name="ID пользователя в соц сети",
        unique=True
    )
    name = models.TextField(
        verbose_name="Имя пользователя"
    )

    button_value = models.CharField(max_length=55)

    def __str__(self):
        return f'# {self.external_id} {self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Message(models.Model):
    profile = models.ForeignKey(
        to='ugc.Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    created_at = models.DateTimeField(
        verbose_name='Время получения',
        auto_now_add=True
    )

    def __str__(self):
        return f'Сообщение {self.pk} {self.profile}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Deposit(models.Model):
    profile = models.ForeignKey(
        to='ugc.Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT,
    )
    sum = models.CharField(max_length=50)
    deadline = models.CharField(max_length=50)
    emonth = models.CharField(max_length=50)

    def __str__(self):
        return f'Сообщение {self.profile} {self.sum}'