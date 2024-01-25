import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class SendgridNotificationSystem:
    # Default constructor
    def __init__(self):
        pass


    # Private method to create email message
    def __create_email__(self, from_email, to_email, subject, body):
        message = Mail(
            from_email=from_email,
            to_emails=to_email,
            subject=subject,
            html_content=f'<strong>{body}</strong>'
        )
        return message


    # Public method to send email message
    def send_email_message(self, from_email, to_email, subject, body):
        try:
            api_key = os.environ.get('SENDGRID_API')
            sg = SendGridAPIClient(api_key)
            response = sg.send(self.__create_email__(from_email, to_email, subject, body))
            print(response.status_code)
            print(response.body + '\n' + response.headers)
        except Exception as e:
            print('Error sending email')
            print(e)
