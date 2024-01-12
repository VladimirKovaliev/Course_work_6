from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.views import MailingListView, MailingCreateView, MailingDeleteView, MailingUpdateView, LogListView, \
    MessageCreateView

urlpatterns = [
    path('', MailingListView.as_view(template_name='mailing/mailing_list.html'), name='mailing_list'),
    path('mailing_create/', MailingCreateView.as_view(template_name="mailing/mailing_create.html")),
    path('message_create', MessageCreateView.as_view(template_name="mailing/message_create.html"),
         name='message_create'),
    path('mailing_update/<int:pk>/',
         cache_page(60)(MailingUpdateView.as_view(template_name='mailing/mailing_create.html'))),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view()),
    path('log_list/', LogListView.as_view(template_name='mailing/log_list.html')),
]
