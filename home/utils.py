from django.core.mail import EmailMessage
from django.conf import settings
import re
import time

#-----------------Email Send------------------------------------------------
def send_mail(to_email, subject, context_dict):
    # Create body dynamically
    lines = ["New Form Submission Received\n"]

    for key, val in context_dict.items():
        lines.append(f"{key.capitalize()}: {val}")

    email_body = "\n".join(lines)

    email_msg = EmailMessage(
        subject=subject,
        body=email_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[to_email],
    )
    email_msg.send(fail_silently=False)



#-----------------Spam Protection- ------------------------------------------------

def is_spam(request, message):
    if not message:
        message = ""

    # Check for URLs
    if re.search(r'https?://|www\.', message.lower()):
        return True
        
    # Check for Russian / Cyrillic characters
    if re.search(r'[\u0400-\u04FF]', message):
        return True

    if request.POST.get("company"):
        return True
    form_time = request.session.get("form_time")
    if form_time and (time.time() - form_time < 3):
        return True

    return False