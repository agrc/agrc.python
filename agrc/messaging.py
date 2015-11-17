from smtplib import SMTP
from email.mime.text import MIMEText


class Emailer:
    # set this to True to prevent emails from actually being sent
    fromAddress = 'noreply@utah.gov'
    server = 'send.state.ut.us'
    port = 25

    def __init__(self, toAddress, testing=False):
        """
        split multiple emails addresses with a ';' (e.g. toAddress='hello@test.com;hello2@test.com')
        """
        self.testing = testing

        if toAddress is not None:
            self.toAddress = toAddress
        else:
            raise Exception('You must provide a toAddress')

        if testing:
            print('Emailer: Testing only. No emails will be sent!')

    def sendEmail(self, subject, body, toAddress=False):
        """
        sends an email using the agrcpythonemailer@gmail.com account
        """

        if not toAddress:
            toAddress = self.toAddress
        toAddress = toAddress.split(';')

        message = MIMEText(body)
        message['Subject'] = subject
        message['From'] = self.fromAddress
        message['To'] = ','.join(toAddress)

        if not self.testing:
            s = SMTP(self.server, self.port)

            s.sendmail(self.fromAddress, toAddress, message.as_string())
            s.quit()

            print('email sent')
        else:
            print('***Begin Test Email Message***')
            print(message)
            print('***End Test Email Message***')
