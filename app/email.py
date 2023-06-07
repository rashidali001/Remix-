from flask_mail import Message
from app import mail, app
from flask import render_template
import smtplib

smtp_server = 'smtp.gmail.com'
smtp_port = 587

smtp_obj = smtplib.SMTP(smtp_server, smtp_port)
smtp_obj.starttls()
smtp_obj.login('rashidestonian@gmail.com', 'ntlrynsdctibfxmo')

def send_email(subject, sender, recipients, text_body, html_body):
    sender = sender
    recipients = recipients
    message = text_body
    smtp_obj.sendmail(sender, recipients, message)
    smtp_obj.quit()
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
    """

def send_password_reset_email(user):
    token = user.get_reset_password_token()

    send_email("[REMIX] PASSWORD RESET",
                sender=app.config["ADMINS"][0],
                recipients=[user.email],
                text_body= render_template("/email/text_body.txt", token=token, user=user),
                html_body = render_template("/email/text_body.txt", token=token, user=user)
                )

