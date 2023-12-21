
from PyQt6.QtCore import QThread
from PyQt6.QtCore import pyqtSignal
from reporter import *

import pandas as pd
import os
import logging.config
import logging
logging.config.fileConfig('./config/logging.ini')
logger = logging.getLogger('worker')

# 以进程的方式生成报告
class WorkerThread(QThread):
    signal = pyqtSignal(str)
    info_signal = pyqtSignal(str)
    # signal = pyqtSignal()
    def __init__(self,info_file,reports_result):
        super(WorkerThread,self).__init__()
        self.info_file = info_file
        self.reports_result = reports_result
        basename = os.path.basename(self.info_file)

    def run(self):
        logger.info('\n running ---1')
        self.adf = pd.read_excel(self.info_file, dtype=str)

        content = '\n已完成报告\n'
        logger.info(self.info_file)
        results = run_report(self.info_file ,self.reports_result)
        self.signal.emit(content)


