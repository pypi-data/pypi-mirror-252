import os, time
import simpleworkspace.loader as sw
from basetestcase import BaseTestCase
from simpleworkspace.logproviders import FileLogger
from datetime import datetime

class LogParser():
    date:datetime = None
    dateStr: str = None
    level:str = None
    module:str = None
    lineNo:int = None
    message:str = None

    @classmethod
    def ParseLine(cls, line:str):
        datepattern = 'dddd-dd-dd dd:dd:dd\.ddd\+dddd'.replace('d', '\\d')
        result = sw.utility.regex.MatchFirst(f"/({datepattern}) (\w+?) <(.+?),(.+?)>: (.*)/is", line)
        if(result):
            log = cls()
            log.dateStr = result[1]
            log.date = datetime.fromisoformat(result[1])
            log.level = result[2]
            log.module = result[3]
            log.lineNo = int(result[4])
            log.message = result[5]
            return log

        result = sw.utility.regex.MatchFirst(f"/({datepattern}) (\w+?): (.*)/is", line)
        if(result):
            log = cls()
            log.dateStr = result[1]
            log.date = datetime.fromisoformat(result[1])
            log.level = result[2]
            log.message = result[3]
            return log

        result = sw.utility.regex.MatchFirst(f"/(\w+?): (.*)/is", line)
        if(result):
            log = cls()
            log.level = result[1]
            log.message = result[2]
            return log


class LogProvidersTests(BaseTestCase):
    def test_logging_FileLogger_LocalTime(self):
        offset = time.strftime('%z') #'+HHMM'

        logpath = self.testPath + '/test.log'
        logger = FileLogger.GetLogger(logpath, useUTCTime=False)
        logger.debug("test log 1")
        for handler in logger.handlers:
            handler.flush()

        logLine = sw.io.file.Read(logpath).strip('\n')
        parsedLine = LogParser.ParseLine(logLine)
        assert parsedLine.dateStr.endswith(offset)

    def test_logging_FileLogger_UTC(self):
        offset = '+0000'

        logpath = self.testPath + '/test.log'
        logger = FileLogger.GetLogger(logpath, useUTCTime=True)
        logger.debug("test log 1")
        for handler in logger.handlers:
            handler.flush()

        logLine = sw.io.file.Read(logpath).strip('\n')
        parsedLine = LogParser.ParseLine(logLine)
        assert parsedLine.dateStr.endswith(offset)