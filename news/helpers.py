from django.core.mail import send_mail
from django.conf import settings 
from django.urls import reverse

def send_subscriber_mail(name, to_email): 
    subject = "Grettings from Healthcare system"
    message = "Thank you for subscribing to our 'Healthcare System'. You'll be notified about updates in the future about the website through this mail."  
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [to_email,],
        fail_silently=False,
    )
