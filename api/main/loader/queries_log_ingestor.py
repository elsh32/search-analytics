import csv
from api.main.computer.analytics_computer import AnalyticsComputer, SearchLogEvent
from api.main.helpers.helpers  import getlogger
from api.main.utilities import constants as cst

log = getlogger(cst.LOGGER['LOG_INGESTOR'])

class QueriesLogIngestor:

    def __init__(self, filePath):
        self._filePath = filePath
        self._analyticsComputer = AnalyticsComputer()

    def loadFileContent(self):
        log.info('------------Loading TSV log queries file------------')
        log.info(self._filePath)
        tsvData = []
        with open(self._filePath) as tsvLogIn:
            log.info('Just open file')
            tsvData = csv.reader(tsvLogIn, delimiter='\t')
            #log.info(list(tsvData))
            for row in tsvData:
                currentSearchLogEvent = SearchLogEvent(row[0], row[1])
                self._analyticsComputer.ingestLog(currentSearchLogEvent)
        log.info('--------------Done loading File --------------------')
        return True
