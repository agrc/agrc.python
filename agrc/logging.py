import sys
import datetime
import os


class Logger:
    log = ''
    logFolder = os.path.join(os.getcwd(), 'Logs')
    scriptName = ''
    addLogsToArcpyMessages = False

    def __init__(self, addLogsToArcpyMessages=False):
        self.addLogsToArcpyMessages = addLogsToArcpyMessages
        now = datetime.datetime.now()
        today = now.strftime('%Y-%m-%d')
        time = now.strftime('%I:%M %p')
        self.scriptName = os.path.split(sys.argv[0])[1]
        self.log = "%s || %s : %s || %s" % (self.scriptName, today, time, os.getenv('COMPUTERNAME'))

        if not os.path.exists(self.logFolder):
            os.mkdir(self.logFolder)

        self.logFile = os.path.join(self.logFolder, today + '.txt')
        print 'Logger Initialized: ' + self.log

    def logMsg(self, msg, printMsg=True):
        """
        logs a message and prints it to the screen
        """
        time = datetime.datetime.now().strftime('%I:%M %p')
        self.log = '{0}\n{1} | {2}'.format(self.log, time, msg)
        if printMsg:
            print msg

        if self.addLogsToArcpyMessages:
            from arcpy import AddMessage
            AddMessage(msg)

    def logGPMsg(self, printMsg=True):
        """
        logs the arcpy messages and prints them to the screen
        """
        from arcpy import GetMessages

        msgs = GetMessages()
        try:
            self.logMsg(msgs, printMsg)
        except:
            self.logMsg('error getting arcpy message', printMsg)

    def writeLogToFile(self):
        """
        writes the log to a
        """
        if not os.path.exists(self.logFolder):
            os.mkdir(self.logFolder)

        with open(self.logFile, mode='a') as f:
            f.write('\n\n' + self.log)

    def logError(self):
        """
        gets traceback info and logs it
        """
        # got from http://webhelp.esri.com/arcgisdesktop/9.3/index.cfm?TopicName=Error_handling_with_Python
        import traceback

        self.logMsg('ERROR!!!')
        errMsg = traceback.format_exc()
        self.logMsg(errMsg)
        return errMsg
