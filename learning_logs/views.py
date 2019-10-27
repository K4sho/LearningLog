from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required


def index(request):
    """Домашняя страница приложения Learning_Log"""
    return render(request, 'learning_logs/index.html')


@login_required()
def topics(request):
    """Выводит список тем"""
    # filter - показываем пользователю только его темы. атрибут owner в БД соответствует текущему пользователю
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')  # Получаем данные из БД. Сортируем по
    # дате добавления
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


@login_required()
def topic(request, topic_id):
    """Выводит одну тему и все ее записи"""
    topic = Topic.objects.get(id=topic_id)
    #  Проверяем принадлежит ли тема текущему пользователю
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required()
def new_topic(request):
    """Определяет новую тему."""
    if request.method != 'POST':
        # Данные не отправились. Создаем пустую форму
        form = TopicForm()
    else:
        # Отправлены данные POST. Обрабатываем
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)  # Новая тема должна быть изменена перед сохранением в БД
            new_topic.owner = request.user  # Присваеваем текущего пользователя
            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required()
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


@login_required()
def edit_entry(request, entry_id):
    """Редактирует существующую запись."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    #  Проверяем совпадает ли владелец темы с текущим пользователем
    if topic.owner != request.user:
        raise Http404

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
