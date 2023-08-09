# import smtplib
# from email.mime.text import MIMEText
# # def send_email(sender_email, sender_name, receiver_email, subject, body):
# #     # Replace 'your_email@gmail.com' and 'your_password' with your Gmail credentials
   

# #     # Create the email message
# #     message = MIMEMultipart()
# #     message['From'] = formataddr((sender_name, sender_email))
# #     message['To'] = receiver_email
# #     message['Subject'] = subject

# #     # Attach the email body
# #     message.attach(MIMEText(body, 'plain'))

# #     # Connect to Gmail's SMTP server
# #     server = smtplib.SMTP('smtp.gmail.com', 465)
# #     server.starttls()

# #     # Login to your Gmail account
# #     server.login(gmail_user, gmail_password)

# #     # Send the email
# #     server.sendmail(gmail_user, receiver_email, message.as_string())

# #     # Close the connection
# #     server.quit()

# def send_email(recipients, subject, body):
#     msg = MIMEText(body)
#     gmail_user = 'ecommercesecured@gmail.com'
#     gmail_password = 'Flinders_1228'
#     msg['Subject'] = subject
#     msg['From'] = gmail_user
#     msg['To'] = ', '.join(recipients)
#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
#        smtp_server.login(gmail_user, gmail_password)
#        smtp_server.sendmail(gmail_user, recipients, msg.as_string())
#     print("Message sent!")

# # Example usage
# # sender_email = 'achint1820@gmail.com'
# # sender_name = 'Your Name'
# receiver_email = 'achint1820@gmail.com'
# subject = 'Test Email from Python'
# body = 'This is a test email sent from Python using smtplib.'

# send_email(receiver_email, subject, body)

from __future__ import print_function

import base64
from email.message import EmailMessage

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def gmail_create_draft():
    """Create and insert a draft email.
       Print the returned draft's message and id.
       Returns: Draft object, including draft id and message meta data.

      Load pre-authorized user credentials from the environment.
      TODO(developer) - See https://developers.google.com/identity
      for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)

        message = EmailMessage()

        message.set_content('This is automated draft mail')

        message['To'] = 'achint1820@gmail.com'
        message['From'] = 'ecommercesecured@gmail.com'
        message['Subject'] = 'Automated draft'

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
            'message': {
                'raw': encoded_message
            }
        }
        # pylint: disable=E1101
        draft = service.users().drafts().create(userId="ecommercesecured@gmail.com",
                                                body=create_message).execute()

        print(F'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        draft = None

    return draft


if __name__ == '__main__':
    gmail_create_draft()