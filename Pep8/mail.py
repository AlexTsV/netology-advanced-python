import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Mail:
    def __init__(self, subject, recipients, message, login='samby_05@mail.ru', password='Qazwsx88',
                 MAIL_SMTP="smtp.mail.ru", MAIL_IMAP="imap.mail.ru"):
        self.MAIL_SMTP = MAIL_SMTP
        self.MAIL_IMAP = MAIL_IMAP
        self.login = login
        self.password = password
        self.subject = subject
        self.recipients = recipients
        self.message = message

    def send_message(self):
        msg = MIMEMultipart()
        msg['From'] = self.login
        msg['To'] = ', '.join(self.recipients)
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.message))

        ms = smtplib.SMTP(self.MAIL_SMTP, 587)
        # identify ourselves to smtp gmail client
        ms.ehlo()
        # secure our email with tls encryption
        ms.starttls()
        # re-identify ourselves as an encrypted connection
        ms.ehlo()

        ms.login(self.login, self.password)
        ms.sendmail(self.login, self.recipients, msg.as_string())
        ms.quit()

    # send end

    def recieve(self, header=None):
        self.header = header
        mail = imaplib.IMAP4_SSL(self.MAIL_IMAP)
        mail.login(self.login, self.password)
        mail.list()
        mail.select("inbox")
        if self.header:
            criterion = f'(HEADER Subject {self.header})'
        else:
            criterion = "ALL"
        result, data = mail.uid('search', None, criterion)
        assert data[0], 'There are no letters with current header'
        latest_email_uid = data[0].split()[-1]
        result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        raw_email = str(data[0][1])
        email_message = email.message_from_string(raw_email)
        print(email_message)
        mail.logout()
    # end recieve


if __name__ == '__main__':
    letter = Mail('Test', ['samby_05@mail.ru'], 'Hello world!')
    # letter.send_message()
    letter.recieve()
