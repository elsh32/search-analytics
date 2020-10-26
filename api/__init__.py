# -*- coding:utf-8 -*-
import os
import datetime
import json
from api.main.loader.queries_log_ingestor import QueriesLogIngestor

LOG_FILE_PATH = './static/file/hn_logs.tsv'
queryIngestor = QueriesLogIngestor(LOG_FILE_PATH)
queryIngestor.loadFileContent()
