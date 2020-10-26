# -*- coding:utf-8 -*-
import sys
sys.path.append('/usr/src/app')
import falcon
from api.main.helpers.helpers  import getlogger, response, is_supported_date, is_valid_int
from api.main.service.search_analytics_service import SearchAnalyticsService
from api.main.utilities import constants as cst

log = getlogger(cst.LOGGER['ANALYTICS_RESSOURCE'])

class SearchAnalyticsRessource(object):
    def on_get_queries_count(self, req, resp, date):
        try:
            if not is_supported_date(date):
                resp.status = falcon.HTTP_400
                error = {
                    'code': cst.ERROR_CODE['BAD_DATA_DATE'],
                    'params': 'date',
                }
                log.info(error)
                resp.body = response(cst.HTTP_STATUS['HTTP_400'], cst.ERROR_TITLES['HTTP_400'], data=error)
                return

            log.info('Getting distinct queries count')
            status, ret, err = SearchAnalyticsService().getQueriesCount(date)
            log.debug(status)
            if not status:
                resp.status = str(cst.HTTP_STATUS[ret]) + ' ' + cst.ERROR_TITLES[ret]
                error = {
                    'code': err
                }
                resp.body = response(cst.HTTP_STATUS[ret], cst.ERROR_TITLES[ret], error = error)
                return
            ret = {
                'count': ret
            }
            resp.status = falcon.HTTP_OK
            resp.body = response(cst.HTTP_STATUS['HTTP_200'], cst.HTTP_STATUS['HTTP_200'], data=ret)
            return
        except Exception as e:
            log.info('Failed getting queries counts : %s' %e)
            resp.status = falcon.HTTP_500
            resp.body = response(cst.HTTP_STATUS['HTTP_500'], cst.ERROR_TITLES['HTTP_500'])
            return

    def on_get_popular_queries(self, req, resp, date):
        try:
            if not is_supported_date(date):
                resp.status = falcon.HTTP_400
                error = {
                    'code': cst.ERROR_CODE['BAD_DATA_DATE'],
                    'params': 'date',
                }
                log.info(error)
                resp.body = response(cst.HTTP_STATUS['HTTP_400'], cst.ERROR_TITLES['HTTP_400'], data=error)
                return
            log.info('Getting distinct popular queries')
            size = req.get_param('size', required=False, default=5)
            log.info(size)
            if not is_valid_int(size):
                resp.status = falcon.HTTP_400
                error = {
                    'code': cst.ERROR_CODE['BAD_DATA_INT'],
                    'params': 'size',
                }
                log.info(error)
                resp.body = response(cst.HTTP_STATUS['HTTP_400'], cst.ERROR_TITLES['HTTP_400'], data=error)
                return
            status, ret, err = SearchAnalyticsService().getPopularQueries(date, int(size))
            log.info('Done getting popular queries')
            log.debug(ret)
            log.debug(status)
            if not status:
                resp.status = str(cst.HTTP_STATUS[ret]) + ' ' + cst.ERROR_TITLES[ret]
                error = {
                    'code': err
                }
                resp.body = response(cst.HTTP_STATUS[ret], cst.ERROR_TITLES[ret], error = error)
                return
            ret = {
                'queries': ret
            }
            resp.status = falcon.HTTP_OK
            resp.body = response(cst.HTTP_STATUS['HTTP_200'], cst.HTTP_STATUS['HTTP_200'], data=ret)
            return
        except Exception as e:
            log.info('Failed getting popular queries : %s' %e)
            resp.status = falcon.HTTP_500
            resp.body = response(cst.HTTP_STATUS['HTTP_500'], cst.ERROR_TITLES['HTTP_500'])
            return