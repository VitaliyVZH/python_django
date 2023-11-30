from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy


def log_out_user(request: HttpRequest):
    logout(request)
    return redirect(reverse('myauth:login'))


class MyLogoutView(LogoutView):
    """
    Класс реализует выход пользователя из учётной записи
    """
    # страница, куда будет перенаправлен пользователь после разлогирования
    next_page = reverse_lazy("myauth:login")
