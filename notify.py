import smtplib, users, config
from email.message import EmailMessage

def SendEmail(subject="No subject", body="No message"):
    admins = users.getAdmins()
    adminEmails = []

    for admin in admins:
        adminEmails.append(admin["email"])

    msg = EmailMessage()
    msg['Subject'] = f'KBot Notification - {subject}'
    msg['From'] = config.KBOT_EMAIL_USERNAME
    msg['To'] = adminEmails
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.ehlo()
        server.login(config.KBOT_EMAIL_USERNAME, config.KBOT_EMAIL_PASSWORD)
        server.send_message(msg)
