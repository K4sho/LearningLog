from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def logout_view(request):
    """Завершает сеанс работы с приложением"""
    logout(request)  # Вызываем библиотечную функцию logout
    # и возвращаемся на домашнюю страницу
    return HttpResponseRedirect(reverse("learning_logs:index"))


def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()  # Сохраняем созданный объекта юзера
            # Выполнение входа и перенаправление на домашнюю страницу
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])  #
            # Возвращается проверенный объект пользователя
            login(request, authenticated_user)  # Создается сессия с
            # текущим пользователем
            return HttpResponseRedirect(reverse("learning_logs:index"))
    context = {'form': form}
    return render(request, 'users/register.html', context)
