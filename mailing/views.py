from django.shortcuts import render
from django.urls import path, reverse_lazy
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from datetime import datetime, timezone

from mailing.forms import MailingForm
from mailing.management.commands.send_mails import Command
from mailing.models import Settings, Message, MailLog


class MailingListView(ListView):
    model = Settings

    def get_clients(self, obj):
        return [client.full_name for client in obj.client.all()]


class MailingCreateView(CreateView):
    model = Settings
    form_class = MailingForm

    success_url = reverse_lazy('mailing_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mailing = form.save()
            new_mailing.save()
            if form.instance.start_date < datetime.now(tz=timezone.utc):
                if Command.check_active(form.instance):
                    Command.process_mailing(form.instance)
            return super().form_valid(form)


class MessageCreateView(CreateView):
    model = Message
    fields = ('title', 'body')
    success_url = reverse_lazy('mailing_list')


class MailingUpdateView(UpdateView):
    model = Settings
    fields = ('start_date', 'period', 'status', 'client', 'message')
    success_url = reverse_lazy('mailing_list')


class MailingDeleteView(DeleteView):
    model = Settings
    success_url = reverse_lazy('mailing_list')


class LogListView(ListView):
    model = MailLog
