from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.core.management import BaseCommand

from mailing.models import Settings, Message, MailLog, Client


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Начал рассылку")
        for mailing in Settings.objects.filter(status=Settings.StatusType.ACTIVE):
            if self.check_active(mailing):
                self.process_mailing(mailing)

    @classmethod
    def check_active(cls, mailing):

        current_date = datetime.now(tz=timezone.utc)
        if mailing.period == Settings.PeriodityType.ADAY:
            period_lag = current_date - timedelta(days=1)
        if mailing.period == Settings.PeriodityType.AWEEK:
            period_lag = current_date - timedelta(days=7)
        if mailing.period == Settings.PeriodityType.AMONTH:
            period_lag = current_date - timedelta(days=30)

        last_mailing = MailLog.objects.filter(settings = mailing, status=MailLog.SendStatus.SENT, data_time__gte=period_lag)

        print(f"нашел рассылку {mailing}, period_lag = {period_lag}, last_mailing {last_mailing}")
        for mailing in last_mailing:
            print(f"уже отправил {mailing}")
            return False

        print(f"отправляю {mailing}")
        cls.process_mailing(mailing, current_date)
        return True

    @classmethod
    def process_mailing(cls, mailing, current_date=datetime.now(tz=timezone.utc)):

        message_to_send = Message.objects.get(title=mailing.message)

        for client in cls.get_clients(mailing):

            email_to_send = client.email
            sending_error = ""

            try:

                send_mail(
                    {message_to_send.title},
                    f'{message_to_send.body}',
                    'RME1C@mail.ru',
                    [email_to_send],
                    fail_silently=False,
                )

            except Exception as sending_error:
                status = MailLog.SendStatus.ERROR
                print(sending_error)
            else:
                status = MailLog.SendStatus.SENT

            MailLog.objects.create(data_time=current_date, status=status,
                                   server_answer=sending_error, client=client, settings=mailing)

    @classmethod
    def get_clients(cls, obj):
        return [client for client in obj.client.all()]