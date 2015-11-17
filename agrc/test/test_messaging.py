from agrc import messaging
import unittest
from mock import patch


@patch('agrc.messaging.SMTP')
class sendEmailFunction(unittest.TestCase):
    to = 'test@test.com'
    sub = 'test sub'
    body = 'test body'

    def test_sendmail_fired(self, SMTP_mock):
        # sendmail should fire only when testing is False
        smtp_instance = SMTP_mock.return_value
        emailer = messaging.Emailer(self.to, False)
        emailer.sendEmail(self.sub, self.body)
        self.assertTrue(smtp_instance.sendmail.called)

        smtp_instance.reset_mock()
        emailer.testing = True
        emailer.sendEmail(self.sub, self.body)
        self.assertFalse(smtp_instance.sendmail.called)

    def test_email_msg_format(self, SMTP_mock):
        # should format the message correctly
        emailer = messaging.Emailer(self.to, False)
        emailer.sendEmail(self.sub, self.body)
        args = SMTP_mock.return_value.sendmail.call_args[0]

        self.assertEqual(args[0], emailer.fromAddress)
        self.assertEqual(args[1], [self.to])
        self.assertEqual(args[2], ('Content-Type: text/plain; charset="us-ascii"\nMIME-Version: 1.0\nContent-Transfer-Encoding: '
                                   '7bit\nSubject: test sub\nFrom: noreply@utah.gov\nTo: test@test.com\n\ntest body'))

    def test_multiple_to_addresses(self, SMTP_mock):
        emailer = messaging.Emailer('test@test.com;test1@test.com')
        emailer.sendEmail(self.sub, self.body)
        args = SMTP_mock.return_value.sendmail.call_args[0]

        self.assertEqual(args[1], ['test@test.com', 'test1@test.com'])

    def test_quit(self, SMTP_mock):
        # should call quit on the server when it is finished
        emailer = messaging.Emailer(self.to, False)
        emailer.sendEmail(self.sub, self.body)
        self.assertTrue(SMTP_mock.return_value.quit.called)

if __name__ == '__main__':
    unittest.main()
