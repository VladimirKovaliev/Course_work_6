import string
import random

from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, TemplateView

from users.forms import RegisterForm, UserProfileForm, SendPasswordForm, EnterCodeForm
from users.models import User


class RegisterView(CreateView):
    """Контроллер для регистрации пользователя"""
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:code')

    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_active = False
            new_user.save()
            email_to_send = self.request.POST.get('email')

            characters = string.digits
            code = ''.join(random.choice(characters) for _ in range(4))
            self.request.session['email_code'] = code
            self.request.session['email'] = email_to_send

            send_mail(
                'Регистрация почти завершена.',
                f'Ваш код для подтверждения {code}',
                'mailings.app@yandex.ru',
                [email_to_send],
                fail_silently=False,
            )
            print(f"письмо отправлено на {email_to_send} c кодом {code}")
            return super().form_valid(form)


class UserListView(ListView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class ProfileView(UpdateView):
    model = User
    form_Class = UserProfileForm
    success_url = reverse_lazy('users:login')

    def get_object(self, queryset=None):
        return self.request.user


class SendPasswordView(TemplateView):
    template_name = 'users/send_password.html'
    form_class = SendPasswordForm
    success_url = reverse_lazy('users:login')

    def post(self, request):
        email_to_send = request.POST.get('email')
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(8))

        send_mail(
            'Ваш пароль на сервисе рассылок был изменен',
            f'Ваш новый пароль: {password}',
            'mailings.app@yandex.ru',
            [email_to_send],
            fail_silently=False
        )

        print(f'Письмо отправлено на {email_to_send} с кодом {password}')

        user_details = User.objects.get(email=email_to_send)
        user_details.set_password(password)
        user_details.save()

        return render(request, self.template_name)


class EnterCode(TemplateView):
    template_name = 'users/enter_code.html'
    form_class = EnterCodeForm
    success_url = reverse_lazy('users:login')

    def post(self, request):
        if request.POST.get('code') == request.session['email_code']:
            user_details = User.objects.get(email=request.session['email'])
            user_details.is_active = True
            user_details.save()
            return render(request, 'users/login.html')
        else:
            return render(request, self.template_name)
