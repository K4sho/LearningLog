from django.db import models


class Topic(models.Model):
    """Тема, изучаемая пользователем"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Возвращает строковое представление модели"""
        return self.text


class Entry(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "entries"

    def __str__(self):
        """Возвращает строковое представление модели"""
        return self.text[:50] + "..."


# @classmethod. Можно вызвать из класса, а не из экземпляра. return cls(параметры). Методу передается cls
# @staticmethod. Не учавствуют в классе как методы. Не могут обращаться к классовым методам и переменным