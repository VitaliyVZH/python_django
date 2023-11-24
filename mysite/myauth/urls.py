from django.urls import path
from .views import (
    auth_base,
    MyLoginView,
    MyLogoutView,
    RegisterView,
    AboutMeView,
    get_cookie_view,
    set_cookie_view,
    get_session_view,
    set_session_view,
    UserListView,
    UserDetailsView,
)

app_name = 'myauth'
urlpatterns = [
    path('', auth_base, name='base'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('about-me/', AboutMeView.as_view(), name='about-me'),
    path('users/', UserListView.as_view(), name='users_list'),
    path('user-details/<int:pk>/<str:name>', UserDetailsView.as_view(), name='user_details'),
    path('cookie/get', get_cookie_view, name='cookie-get'),
    path('cookie/set', set_cookie_view, name='cookie-set'),
    path('session/get', get_session_view, name='session-get'),
    path('session/set', set_session_view, name='session-set'),
]
