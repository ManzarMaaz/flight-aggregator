# notification_manager.py
from twilio.rest import Client
import smtplib
from email.message import EmailMessage
from app.config import settings

class NotificationManager:
    """
    Manages sending SMS and Email notifications.
    """
    def __init__(self):
        """
        Initializes the Twilio client and email credentials.
        """
        # Twilio setup 
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.twilio_number = settings.TWILIO_VIRTUAL_NUMBER
        self.receiver_number = settings.TWILIO_VERIFIED_NUMBER

        # Email setup
        self.my_mail = settings.MY_MAIL 
        self.my_pass = settings.MY_PASS
        self.smtp_server = settings.SMTP_SERVER

    def send_sms(self, message_body: str):
        """
        Sends a text message with the specified body to the verified number.
        """
        try:
            message = self.client.messages.create(
                body=message_body,
                from_=self.twilio_number,
                to=self.receiver_number
            )
            print(f"\n✅ SMS Status: {message.status}")
            print(f"✅ SMS Successfully Send SID: {message.sid}\n")
        except Exception as e:
            print(f"❌ Failed to send SMS: {e}")
            
    def send_email(self, subject: str, body: str, to_email: str):
        """
        Sends a single email with the flight deal details.
        """
        try:
            msg = EmailMessage()
            msg.set_content(body)
            msg['Subject'] = subject
            msg['From'] = self.my_mail
            msg['To'] = to_email

            with smtplib.SMTP_SSL(self.smtp_server, 465) as connection:
                connection.login(self.my_mail, self.my_pass)
                connection.send_message(msg)
            
            print(f"✅ Email sent successfully to {to_email}")
        except Exception as e:
            print(f"❌ Failed to send email to {to_email}: {e}")