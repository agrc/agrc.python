import agrc.messaging
import unittest
from mock import Mock, patch


class sendEmailFunction(unittest.TestCase):
    # TODO: These tests are broken trying to mock smtplib :(
    to = 'test@test.com'
    sub = 'test sub'
    body = 'test body'

    def setUp(self):
        self.emailer = agrc.messaging.Emailer(self.to)
        with patch('smtplib.SMTP') as self.serverMock:
            instance = self.serverMock.return_value
            instance.sendmail = Mock()
            instance.sendmail.return_value = ''
        self.emailer.sendEmail(self.sub, self.body)
    
    def tearDown(self):
        self.serverMock.sendmail.reset_mock()
        self.serverMock.quit.reset_mock()
        self.emailer = None
    
    def test_sendmail_fired(self):
        # sendmail should fire only when testing is False
        assert self.serverMock.sendmail.called
        
        emailerTesting = agrc.messaging.Emailer(self.to, True)
        emailerTesting.server.sendmail = Mock(name='sendmail-testing')
        emailerTesting.sendEmail(self.sub, self.body)
        assert not emailerTesting.server.sendmail.called
    
    def test_email_msg_format(self):
        # should format the message correctly
        args = self.serverMock.sendmail.call_args[0]
        
        assert args[0] == self.emailer.fromAddress
        assert args[1] == self.to
        assert args[2] == 'From: agrcpythonemailer@gmail.com\nTo: test@test.com\nSubject: test sub\n\ntest body'
        
    def test_quit(self):
        # should call quit on the server when it is finished
        assert self.serverMock.quit.called
        
if __name__ == '__main__':
    unittest.main()