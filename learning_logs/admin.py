from django.contrib import admin
from learning_logs.models import Topic, Entry

admin.site.register(Topic)  # Регистрируем модель Topic на админке
admin.site.register(Entry)
