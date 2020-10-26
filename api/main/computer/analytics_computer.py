import os
import datetime
from api.main.helpers.helpers  import getlogger
from api.main.utilities import constants as cst

log = getlogger(cst.LOGGER['ANALYTICS_COMPUTER'])

class SearchLogEvent:
    def __init__(self, eventDateTimeString, eventLogQuery):
        self.date = datetime.datetime.strptime(eventDateTimeString, '%Y-%m-%d %H:%M:%S')
        self.query = eventLogQuery

class AnalyticsComputer:
    class __AnalyticsComputer:
        def __init__(self):
            self._searchQueriesLogs = []
            self._precomputedSearchQueriesStats = {}

    _instance = None
    def __init__(self):
        if not AnalyticsComputer._instance:
            AnalyticsComputer._instance = AnalyticsComputer.__AnalyticsComputer()

    def ingestLog(self, searchLogEvent):
        # self._instance._searchQueriesLogs.append(searchLogEvent)
        self._computeSearchQueriesStats(searchLogEvent)
        return

    def _computeSearchQueriesStats(self, searchLogEvent):
        # set year based stats
        currentEventYear = str(searchLogEvent.date.year)
        self._setPeriodBasedStats(currentEventYear, searchLogEvent.query)
        # set month based stats
        currentEventMonth = searchLogEvent.date.strftime('%Y-%m')
        self._setPeriodBasedStats(currentEventMonth, searchLogEvent.query)
        # set day based stats
        currentEventDay = searchLogEvent.date.strftime('%Y-%m-%d')
        self._setPeriodBasedStats(currentEventDay, searchLogEvent.query)
        # set hour based stats
        currentEventHour= searchLogEvent.date.strftime('%Y-%m-%d %H')
        self._setPeriodBasedStats(currentEventHour, searchLogEvent.query)
        # set minute based stats
        currentEventMinute = searchLogEvent.date.strftime('%Y-%m-%d %H:%M')
        self._setPeriodBasedStats(currentEventMinute, searchLogEvent.query)
        # set year based stats
        currentEventSecond = searchLogEvent.date.strftime('%Y-%m-%d %H:%M:%S')
        self._setPeriodBasedStats(currentEventSecond, searchLogEvent.query)
        return

    def _setPeriodBasedStats(self, period, query):
        if period not in self._instance._precomputedSearchQueriesStats:
            self._instance._precomputedSearchQueriesStats[period] = {'count': 0, 'queriesCount': {}, 'sortedDinstinctQueries': [], 'isSortedDistinctQueriesUpToDate': False}
        if query not in self._instance._precomputedSearchQueriesStats[period]['queriesCount']:
            self._instance._precomputedSearchQueriesStats[period]['count'] += 1
            self._instance._precomputedSearchQueriesStats[period]['queriesCount'][query] = 0
        self._instance._precomputedSearchQueriesStats[period]['queriesCount'][query] += 1
        return

    def _sortDistinctSearchQueryPerPeriod(self, period):
        self._instance._precomputedSearchQueriesStats[period]['sortedDinstinctQueries'] = [{'query': query, 'count': self._instance._precomputedSearchQueriesStats[period]['queriesCount'][query]} for query in sorted(self._instance._precomputedSearchQueriesStats[period]['queriesCount'], key=self._instance._precomputedSearchQueriesStats[period]['queriesCount'].get, reverse=True)]
        self._instance._precomputedSearchQueriesStats[period]['isSortedDistinctQueriesUpToDate'] = True
        return

    def getDistinctQueriesCount(self, date):
        return self._instance._precomputedSearchQueriesStats[date]['count'] if date in self._instance._precomputedSearchQueriesStats else 0

    def getTopPopularQueries(self, date, size):
        if date not in self._instance._precomputedSearchQueriesStats:
            return []
        if not self._instance._precomputedSearchQueriesStats[date]['isSortedDistinctQueriesUpToDate']:
            self._sortDistinctSearchQueryPerPeriod(date)
        return self._instance._precomputedSearchQueriesStats[date]['sortedDinstinctQueries'][0:max(size, 0)]
















