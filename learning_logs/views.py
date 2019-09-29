from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
    """Домашняя страница приложения Learning_Log"""
    return render(request, 'learning_logs/index.html')


def topics(request):
    """Выводит список тем"""
    topics = Topic.objects.order_by('date_added')  # Получаем данные из БД. Сортируем по дате добавления
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """Выводит одну тему и все ее записи"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def new_topic(request):
    """Определяет новую тему."""
    if request.method != 'POST':
        # Данные не отправились. Создаем пустую форму
        form = TopicForm()
    else:
        # Отправлены данные POST. Обрабатываем
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


def new_entry(request, topic_id):
    """Добавляет новую запись по конкретной теме."""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # Данные не отправлялись, создаем пустую форму
        form = EntryForm
    else:
        # Отправлены данные POST. Обрабатываем
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)  # Пока не сохраняем в БД
            new_entry.topic = topic  # Задаем атрибут topic перед сохранением в БД
            new_entry.save()  # Сохраняем в БД
            return HttpResponseRedirect(reverse('topic',
                                                args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


def edit_entry(request, entry_id):
    """Редактирует существующую запись."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        # Исходный запрос, форма заполняется данными текущей записи
        form = EntryForm(instance=entry)  # Приказываем создать форму, заполненную информацией из существующего
        # объекта записи
    else:
        # Отправка данных в POST
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
