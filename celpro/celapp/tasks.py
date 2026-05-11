from celery import shared_task
import time


@shared_task
def delay_task(text):
    time.sleep(10)
    print(text)

    return "Done"


@shared_task
def email_task(email):
    print(f"Email successfully sent to {email}")

    return "Email simulation done"
