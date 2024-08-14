import os
import time
from nose.plugins import Plugin

class NoseTitlePrint(Plugin):
    name = "nose_title_print"

    def options(self, parser, env=os.environ):
        # action about store need a extra param.
        # store_true not need a extra param.
        parser.add_option('--nose-title-print', action='store_true',
                          dest='nose_title_print', default=None,
                          help='Add more information to test log.')

    def configure(self, options, conf):
        Plugin.configure(self, options, conf)
        # open the plugin when use --hci-test-info
        self.enabled = bool(options.nose_title_print)
    
    def write(self, output):
        self.stream.write(output)
    
    def setOutputStream(self, stream):
        self.stream = stream

    def beforeTest(self, test):
        # timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.write("======================================================================\n")
        self.write("\U0001F610\U0001F610\U0001F610 [Start Case:{}]\n".format(test))
    
    def afterTest(self, result):
        # self.write("result:{}".format(result.__dir__()))
        if None == result.passed:
            self.write("\n\U0001F600\U0001F600\U0001F600 [End Case:{}]\n".format(result))
        elif False == result.passed:
            self.write("\n\U0001F614\U0001F614\U0001F614 [End Case:{}]\n".format(result))
        # timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.write("======================================================================\n")

    def begin(self):
        pass