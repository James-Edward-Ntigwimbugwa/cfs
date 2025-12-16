import logging
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
import requests
from django.template.loader import render_to_string
from jinja2 import Environment, FileSystemLoader
from django.utils import timezone
from dotenv import dotenv_values

from myapp_notifications.constants import NOTIFICATION_MAP
config = dotenv_values(".env")
logger = logging.getLogger(__name__)


class NotificationServices:
    @classmethod
    def send_email_notification(cls, email_body, html_template, attachment_url=None):

        EMAIL_HOST = config['EMAIL_HOST']
        EMAIL_PASSWORD = config['EMAIL_HOST_PASSWORD']
        EMAIL_USER = config['EMAIL_HOST_USER']
        EMAIL_PORT = config['EMAIL_PORT']
        DEFAULT_FROM_EMAIL = config['DEFAULT_FROM_EMAIL']

        email_is_sent = True

        html_content = render_to_string(html_template, {'data': email_body})

        # Create a Jinja2 environment with the HTML template
        env = Environment(loader=FileSystemLoader(html_template))
        template = env.from_string(html_content)

        # Render the template with the provided emailBody
        rendered_template = template.render({'data': email_body})

        # Create a multipart message and set the headers
        msg = MIMEMultipart()
        msg['From'] = DEFAULT_FROM_EMAIL
        msg['To'] = email_body['receiver_details']
        msg['Subject'] = email_body['subject']

        # Attach the rendered HTML content as the email body
        msg.attach(MIMEText(rendered_template, 'html'))
        if attachment_url is not None:
            url = config['FILE_URL'] + "/" + attachment_url
            response = requests.get(url)
            if response.status_code == 200:
                attachment_content = response.content

                # Create attachment from content
                attachment_part = MIMEBase('application', 'pdf')
                attachment_part.set_payload(attachment_content)
                encoders.encode_base64(attachment_part)

                # Add header as key/value pair to attachment part
                attachment_part.add_header(
                    'Content-Disposition', f"attachment; filename = Email_Attachment")

                # Attach the file to the email message
                msg.attach(attachment_part)

        # Create a secure SSL/TLS connection to the SMTP server
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()

        try:
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(DEFAULT_FROM_EMAIL,
                            email_body['receiver_details'], msg.as_string())
            email_is_sent = True

        except smtplib.SMTPAuthenticationError as auth_error:
            logger.error(
                f"[SMTPAuthenticationError]: Failed to authenticate :: {auth_error}")
            email_is_sent = False
        except smtplib.SMTPRecipientsRefused as e:
            logger.error(f"Exception sending email :: {e}")
            email_is_sent = False

        server.quit()

        return email_is_sent


    @classmethod
    def send(cls, notification_code: str, context: dict, html_template = None):
        """
        Sends dynamic emails using NOTIFICATION_MAP definitions.
        Reuses send_email_notification() to handle actual SMTP logic.
        """
        try:
            template_data = NOTIFICATION_MAP.get(notification_code)
            if not template_data:
                raise ValueError(f"Notification code '{notification_code}' not found in NOTIFICATION_MAP")

            # Safe formatting for placeholders
            def safe_format(text, ctx):
                try:
                    return text.format(**ctx)
                except KeyError as e:
                    missing = str(e).strip("'")
                    logger.warning(f"Missing context key '{missing}' in {notification_code}")
                    return text

            subject = safe_format(template_data["subject"], context)
            message_body = safe_format(template_data["message_body"], context)

            template = "notifications/shared_notification.html" if not html_template else html_template
            cc_list = context.get("cc_list", [])
            if isinstance(cc_list, str):
                cc_list = [cc_list]

            # Build the same payload structure your SMTP sender expects
            email_body = {
                "IMAGE_URL": os.path.join(settings.BASE_DIR, "myapp_assets"),
                "receiver_details": context["receiver_email"],
                "subject": subject,
                "message": message_body,
                "cc_list": cc_list,
                "front_end_url": context.get("front_end_url", ""),
                "signature": context.get("signature", "SPPS Secretariat"),
                "action_label": template_data.get("action_label", ""),
                **context
            }

            # Reuse the existing SMTP sender
            return cls.send_email_notification(email_body, template)
        except Exception as e:
            logger.error(f"Error sending dynamic email '{notification_code}': {e}")
            return False

    @classmethod
    def shared_send_sms_notification(cls, reciver, message_body):
        try:
            data_body = {
                "recive_phone": reciver,
                "message_sent": message_body,
                "date_sent": timezone.now().today(),
                "sender_id": config['SENDER_ID'],
                "vote_code": config['VOTE_CODE']
            }
            response_data = requests.post(url=config['SHARED_SMS_API_URL'], data=data_body)
            # Validate successful response
            if response_data.status_code != 200:
                print(f"SMS Notification Failed with status code {response_data.status_code} :: {response_data.text}")
                return False
            return True
        except Exception as e:
            logger.error(f"Sending Notification via SMS Failed :: {e}")
            return False

