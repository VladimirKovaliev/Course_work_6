from django.contrib.auth.views import LogoutView, LoginView
from django.conf.urls.static import static
from django.urls import path

from config import settings
from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, SendPasswordView, EnterCode

app_name = UsersConfig.name

urlpatterns = [
    path('', RegisterView.as_view(template_name='users/register.html'), name='user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('profile/', ProfileView.as_view(template_name='users/profile.html'), name='profile'),
    path('send_password/', SendPasswordView.as_view(template_name='users/send_password.html'), name='send_password'),
    path('code/', EnterCode.as_view(), name='code'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
