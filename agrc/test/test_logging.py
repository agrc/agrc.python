import agrc.logging
import unittest, sys, datetime, os, shutil
from mock import Mock

class LoggerTests(unittest.TestCase):
    logTxt = 'test log text'
    erTxt = 'test error text'
    def setUp(self):
        self.logger = agrc.logging.Logger()
        
    def tearDown(self):
        del self.logger
    
    def test_init(self):
        # should get the name of the script and date
        self.assertEqual(self.logger.log, os.path.split(sys.argv[0])[1] + ' || ' + \
                          datetime.datetime.now().strftime('%Y-%m-%d') + ' : ' + \
                          datetime.datetime.now().strftime('%I:%M %p'))
    
    def test_log(self):
        # should append the log message
        log = self.logger.log[:] # pass a copy
        self.logger.logMsg(self.logTxt)
        assert self.logger.log == log + '\n' + self.logTxt
    
    def test_logGPMsg(self): 
        # should call get messages on arcpy
        agrc.logging.GetMessages = Mock(name='GetMessages')
        self.logger.logMsg = Mock(name='logMsg')
        self.logger.logGPMsg()
        
        self.assertTrue(agrc.logging.GetMessages.called)
        assert self.logger.logMsg.called
        
    def test_writeToLogFile(self):
        if os.path.exists(self.logger.logFolder):
            shutil.rmtree(self.logger.logFolder)
        
        self.logger.writeLogToFile()
        # should create folder for script
        self.assertTrue(os.path.exists(self.logger.logFolder))
    
    def test_logError(self):
        self.logger.logMsg = Mock()
        
        self.logger.logError()
        
        assert self.logger.logMsg.called
        
if __name__ == '__main__':
    unittest.main()