# -*- coding: utf-8 -*-
from imio.helpers.emailer import create_html_email
from imio.helpers.emailer import send_email
from imio.scan_logger import log
from plone import api


def send_notification(title, lines):
    """Send email if required."""
    emails = api.portal.get_registry_record("imio.scan_logger.interfaces.ISettings.notification_emails")
    if not emails:
        return
    emails = [email.strip() for email in emails.split(",")]
    msg = create_html_email("\n".join(["<p>{}</p>".format(line) for line in lines]))
    mfrom = api.portal.get_registry_record("plone.email_from_address")
    ret, error = send_email(msg, title, mfrom, emails)
    # try:
    # api.portal.send_email(mfrom, emails[0], title, "\n".join(lines))
    # except ValueError as error:
    if not ret:
        log.error(f"Cannot send email: {error}")
