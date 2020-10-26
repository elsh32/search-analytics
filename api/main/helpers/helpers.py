# -*- coding:utf-8 -*-
import sys
import json
import logging
import falcon
import datetime

LOG_BASE_DIR = '/usr/src/app/log'


class CORSComponent(object):
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'content-type, HTTP_AGENT')
        resp.set_header('Access-Control-Expose-Headers', '*')
        resp.set_header('Access-Control-Max-Age', 1728000)  # 20 days
        if req.method == 'OPTIONS':
            raise falcon.HTTPStatus(falcon.HTTP_200, body='\n')
    def process_response(self, req, resp, resource,req_succeeded):
        if 'result' not in resp.context:
            return
        resp.body = json.dumps(resp.context['result'])

#log creator
def getlogger(name, log_level = 'INFO'):
    log_filename = name+ '.log'
    importer_logger = logging.getLogger(name)
    importer_logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(msecs)d - %(funcName)s - %(lineno)d : %(levelname)s : %(message)s')

    fh = logging.FileHandler(filename=LOG_BASE_DIR + log_filename)
    fh.setLevel(log_level)
    fh.setFormatter(formatter)
    importer_logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(log_level)
    sh.setFormatter(formatter)
    importer_logger.addHandler(sh)

    return importer_logger


def max_body(limit):
    def hook(req, resp, resource, params):
        length = req.content_length
        if length is not None and length > limit:
            msg = ('The size of the request is too large. The body must not '
                   'exceed ' + str(limit) + ' bytes in length.')

            raise falcon.HTTPRequestEntityTooLarge(
                'Request body is too large', msg)
    return hook


def response(status, message, data={}, error={}):
    return json.dumps(data)

def is_supported_date(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return True
    except Exception as e:
        print('Not %Y-%m-%d %H:%M:%S')

    try:
        datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
        return True
    except Exception as e:
        print('Not %Y-%m-%d %H:%M')

    try:
        datetime.datetime.strptime(date, '%Y-%m-%d %H')
        return True
    except Exception as e:
        print('Not %Y-%m-%d %H')

    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except Exception as e:
        print('Not %Y-%m-%d')

    try:
        datetime.datetime.strptime(date, '%Y-%m')
        return True
    except Exception as e:
        print('Not %Y-%m')

    try:
        datetime.datetime.strptime(date, '%Y')
        return True
    except Exception as e:
        print('Not %Y')

    return False


def is_valid_int(x):
    try:
        int(x)
        return True
    except Exception as e:
        print('Not  a valid int')

    return False



log = getlogger('searchQueryAnalytics')

