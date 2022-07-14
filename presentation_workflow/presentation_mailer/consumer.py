import json
import pika
import django
import os
import sys
from django.core.mail import send_mail


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()


def process_approval(ch, method, properties, body):
    data = json.loads(body)
    presenter_email = data[0]["presenter_email"]
    subject = "Your presentation has been accepted"
    data_name = data[0]["presenter_name"]
    data_title = data[0]["title"]
    subj_body = f"{data_name}, we're happy to tell you that your presentation {data_title} has been accepted"
    send_mail(
        subject=subject,
        message=subj_body,
        from_email="admin@conference.go",
        recipient_list=[presenter_email],
        fail_silently=False,
    )


def process_rejection(ch, method, properties, body):
    data = json.loads(body)
    presenter_email = data[0]["presenter_email"]
    subject = "Your presentation has been rejected"
    data_name = data[0]["presenter_name"]
    data_title = data[0]["title"]
    subj_body = f"{data_name}, we're sorry to tell you that your presentation {data_title} has been rejected"
    send_mail(
        subject=subject,
        message=subj_body,
        from_email="admin@conference.go",
        recipient_list=[presenter_email],
        fail_silently=False,
    )


parameters = pika.ConnectionParameters(host="rabbitmq")
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue="presentation_approvals")
channel.basic_consume(
    queue="presentation_approvals",
    on_message_callback=process_approval,
    auto_ack=True,
)

channel.queue_declare(queue="presentation_rejections")
channel.basic_consume(
    queue="presentation_rejections",
    on_message_callback=process_rejection,
    auto_ack=True,
)

channel.start_consuming()
