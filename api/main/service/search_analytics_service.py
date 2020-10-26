import os
from api.main.computer.analytics_computer import AnalyticsComputer
from api.main.helpers.helpers  import getlogger
from api.main.utilities import constants as cst

log = getlogger(cst.LOGGER['SEARCH_ANALYTICS_SERVICE'])

class SearchAnalyticsService:

    def __init__(self):
        self._analyticsComputer = AnalyticsComputer()
    def getQueriesCount(self, date):
        resp = self._analyticsComputer.getDistinctQueriesCount(date)
        return True, resp, ''
    def getPopularQueries(self, date, size):
        resp = self._analyticsComputer.getTopPopularQueries(date, size)
        return True, resp, ''