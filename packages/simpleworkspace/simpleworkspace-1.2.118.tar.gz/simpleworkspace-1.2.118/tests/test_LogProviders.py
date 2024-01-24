import os, time
import simpleworkspace.loader as sw
from basetestcase import BaseTestCase
from simpleworkspace.logproviders import FileLogger, StdoutLogger, RotatingFileLogger
from datetime import datetime
from contextlib import redirect_stdout
from simpleworkspace.types.byte import ByteEnum
import io
import gzip


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

    def test_logging_RotatingFileLogger_UTC(self):
        offset = '+0000'

        logpath = self.testPath + '/test.log'
        logger = RotatingFileLogger.GetLogger(logpath, useUTCTime=True)
        logger.debug("test log 1")
        for handler in logger.handlers:
            handler.flush()

        logLine = sw.io.file.Read(logpath).strip('\n')
        parsedLine = LogParser.ParseLine(logLine)
        assert parsedLine.dateStr.endswith(offset)

    def test_logging_RotatingFileLogger_RotateOnSizeLimit(self):
        logpath = self.testPath + '/test.log'
        logger = RotatingFileLogger.GetLogger(logpath, useUTCTime=True, maxBytes=100, maxRotations=2)
        logger.debug("start") #should not rotate
        assert "start" in sw.io.file.Read(logpath)
        assert not os.path.exists(logpath + ".1.gz")
        logger.debug("rotated:1" * 10) #should rotate previous
        assert os.path.exists(logpath + ".1.gz")
        logger.debug("rotated:2" * 10) #should rotate previous
        assert os.path.exists(logpath + ".2.gz")
        logger.debug("rotated:3" * 10) #should rotate previous, and remove oldest since maxrotations is 2
        assert not os.path.exists(logpath + ".3.gz")

        assert "rotated:3" in sw.io.file.Read(logpath)
        with gzip.open(logpath + ".1.gz", 'rb') as f:
            assert "rotated:2" in f.read().decode()
        with gzip.open(logpath + ".2.gz", 'rb') as f:
            assert "rotated:1" in f.read().decode()

    def test_logging_SysLogger_LocalTime(self):
        offset = time.strftime('%z') #'+HHMM'
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            logger = StdoutLogger.GetLogger(useUTCTime=False)
            logger.debug("test log 1")
            logger.handlers.clear() # remove handler to ensure next tests create a fresh one

        logLine = stdout.getvalue().strip('\n')
        parsedLine = LogParser.ParseLine(logLine)
        assert parsedLine.dateStr.endswith(offset)

    def test_logging_SysLogger_UTC(self):
        offset = '+0000'
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            logger = StdoutLogger.GetLogger(useUTCTime=True)
            logger.debug("test log 1")
            logger.handlers.clear() # remove handler to ensure next tests create a fresh one

        logLine = stdout.getvalue().strip('\n')
        parsedLine = LogParser.ParseLine(logLine)
        assert parsedLine.dateStr.endswith(offset)

    def test_logging_SysLogger_Detailed(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            logger = StdoutLogger.GetLogger(useUTCTime=True)
            logger.debug("test log 1")
            logger.handlers.clear() # remove handler to ensure next tests create a fresh one

        logLine = stdout.getvalue().strip('\n')
        parsedLine = LogParser.ParseLine(logLine)
        
        self.assertIsNotNone(parsedLine.date)
        self.assertIsNotNone(parsedLine.dateStr)
        self.assertIsNotNone(parsedLine.module)
        self.assertIsInstance(parsedLine.lineNo, int)
        self.assertEqual(parsedLine.level, 'DEBUG')
        self.assertEqual(parsedLine.message, "test log 1")

    def test_logging_SysLogger_Normal(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            logger = StdoutLogger.GetNormalLogger(useUTCTime=True)
            logger.debug("test log 1")
            logger.handlers.clear() # remove handler to ensure next tests create a fresh one

        logLine = stdout.getvalue().strip('\n')
        parsedLine = LogParser.ParseLine(logLine)
        
        self.assertIsNotNone(parsedLine.date)
        self.assertIsNotNone(parsedLine.dateStr)
        self.assertIsNone(parsedLine.module)
        self.assertIsNone(parsedLine.lineNo)
        self.assertEqual(parsedLine.level, 'DEBUG')
        self.assertEqual(parsedLine.message, "test log 1")


    def test_logging_SysLogger_Basic(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            logger = StdoutLogger.GetBasicLogger()
            logger.debug("test log 1")
            logger.handlers.clear() # remove handler to ensure next tests create a fresh one

        logLine = stdout.getvalue().strip('\n')
        parsedLine = LogParser.ParseLine(logLine)
        
        self.assertIsNone(parsedLine.date)
        self.assertIsNone(parsedLine.dateStr)
        self.assertIsNone(parsedLine.module)
        self.assertIsNone(parsedLine.lineNo)
        self.assertEqual(parsedLine.level, 'DEBUG')
        self.assertEqual(parsedLine.message, "test log 1")
        