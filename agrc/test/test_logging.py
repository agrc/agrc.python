from agrc import logging
import unittest
import sys
import datetime
import os
import shutil
from mock import Mock, patch


class LoggerTests(unittest.TestCase):
    logTxt = 'test log text'
    erTxt = 'test error text'

    def setUp(self):
        self.logger = logging.Logger()

    def tearDown(self):
        del self.logger

    def test_init(self):
        # should get the name of the script and date
        self.assertEqual(self.logger.log, os.path.split(sys.argv[0])[1] + ' || ' +
                         datetime.datetime.now().strftime('%Y-%m-%d') + ' : ' +
                         datetime.datetime.now().strftime('%I:%M %p') + ' || None')

    def test_log(self):
        # should append the log message
        original_length = len(self.logger.log)
        self.logger.logMsg(self.logTxt)
        self.assertGreater(self.logger.log.find(self.logTxt), original_length)

    @patch('agrc.logging.Logger.logMsg')
    @patch('arcpy.GetMessages')
    def test_logGPMsg(self, GetMessages_mock, logMsg_mock):
        # should call get messages on arcpy
        self.logger.logGPMsg()

        self.assertTrue(GetMessages_mock.called)
        self.assertTrue(logMsg_mock.called)

    def test_writeToLogFile(self):
        if os.path.exists(self.logger.logFolder):
            shutil.rmtree(self.logger.logFolder)

        self.logger.writeLogToFile()
        # should create folder for script
        self.assertTrue(os.path.exists(self.logger.logFolder))

    def test_logError(self):
        self.logger.logMsg = Mock()

        self.logger.logError()

        self.assertTrue(self.logger.logMsg.called)

if __name__ == '__main__':
    unittest.main()
