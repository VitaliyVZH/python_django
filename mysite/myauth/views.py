import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from myauth.models import Profile

log = logging.getLogger(__name__)


def auth_base(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request=request, template_name='myauth/base.html', context=context)


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'

    def get_success_url(self):
        return reverse('myauth:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password2')
        user = authenticate(self.request, username=username, password=password)
        login(request=self.request, user=user)
        return response


class AboutMeView(UserPassesTestMixin, UpdateView):
    template_name = 'myauth/about-me.html'
    model = Profile
    fields = 'avatar',
    success_url = reverse_lazy('myauth:about-me')

    def test_func(self):
        return self.request.user.has_perm('myauth.change_profile')

    def get_object(self, queryset=None):
        return self.request.user.profile


class UserListView(UserPassesTestMixin, ListView):
    template_name = 'myauth/users-list.html'
    model = Profile
    # queryset = (Profile.objects.select_related('user').all())

    def test_func(self):
        log.info('User list')
        return self.request.user.is_staff


class UserDetailsView(UserPassesTestMixin, UpdateView):
    template_name = 'myauth/user-details.html'
    model = Profile
    # queryset = (Profile.objects.select_related('user').all())
    fields = 'avatar',

    def test_func(self):
        log.info('User details view')
        if self.request.user.is_staff:
            return True
        self.object = self.get_object()
        if self.request.user.pk == self.object.user.pk:
            return True
        return False

    def get_success_url(self):
        return reverse('myauth:user_details', kwargs={
            'pk': self.object.pk,
            'name': self.object.user.username
        })


class MyLoginView(LoginView):
    template_name = 'myauth/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('myauth:about-me')


class MyLogoutView(LogoutView):
    redirect_field_name = 'myauth/login.html'
    extra_context = {'title': 'Goodbye'}


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('fizz', 'buzz', max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default value')
    return HttpResponse(f'Cookie value: {value!r}')


def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['foobar'] = 'spameggs'
    return HttpResponse('Session set!')


def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default')
    return HttpResponse(f'Session value: {value!r}')
