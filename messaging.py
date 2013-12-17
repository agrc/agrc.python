import smtplib
from email.mime.text import MIMEText


class Emailer:
    # set this to True to prevent emails from actually being sent
    fromAddress = 'noreply@utah'
    toAddress = ''
    server = 'send.state.ut.us'
    port = 25
    
    def __init__(self, toAddress, testing=False):
        self.testing = testing
        
        if len(toAddress) > 0:
            self.toAddress = toAddress
        else:
            raise Exception('You must provide a toAddress')
        
        if testing:
            print('Emailer: Testing only. No emails will be sent!*************')
    
    def sendEmail(self, subject, body, toAddress=False):
        """
        sends an email using the agrcpythonemailer@gmail.com account
        """
        
        if not toAddress:
            toAddress = self.toAddress

        message = MIMEText(body)
        message['Subject'] = subject
        message['From'] = self.fromAddress
        message['To'] = toAddress

        if not self.testing:
            s = smtplib.SMTP(self.server, self.port)
            
            s.sendmail(self.fromAddress, toAddress, message.as_string())
            s.quit()
            
            print('email sent')
        else:
            print('***Test Email Message:***')
            print(message)
            print('***End Test Email Message***')