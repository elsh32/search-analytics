# -*- coding: UTF-8 -*-
import os

# Documentation settings
SWAGGERUI_URL = '/v1/doc'
SCHEMA_URL = '/static/v1/swagger.json'
PAGE_TITLE = 'TeraJob XP API Doc'
SUPPORTED_SUBMIT_METHODS = ['get', 'post', 'put', 'delete']
SWAGGER_CLIENT_REALM = 'MyTeraJobAPIRealm'
SWAGGER_CLIENT_ID = 'MyTeraJobAPIID'
SWAGGER_CLIENT_SECRET = 'A1Zsez4327?kdgdie436$@fd'
SWAGGER_CONF = {'supportedSubmitMethods': SUPPORTED_SUBMIT_METHODS,
                'client_realm': SWAGGER_CLIENT_REALM,
                'client_id': SWAGGER_CLIENT_ID,
                'client_secret': SWAGGER_CLIENT_SECRET
                }
FAVICON_URL = 'faveicon.ico'
U_DOC_KEY = 'A1Zsez4327kdgdie436fd'
LOGGER = {
    'ANALYTICS_RESSOURCE': 'analytics_ressource',
    'LOG_INGESTOR': 'log_ingestor',
    'SEARCH_ANALYTICS_SERVICE': 'search_analytics_service',
    'ANALYTICS_COMPUTER': 'analytics_computer'
}

HTTP_STATUS = {
    'HTTP_400': 400,
    'HTTP_500': 500,
    'HTTP_202': 202,
    'HTTP_200': 200,
    'HTTP_401': 401,
    'HTTP_403': 403
}


ERROR_TITLES = {
    'HTTP_400': 'Forbidden',
    'HTTP_500': 'Unhandled Exception',
    'HTTP_202': 'Accepted',
    'HTTP_200': 'Ok',
    'HTTP_401': 'Unauthorized',
    'HTTP_403': 'Forbidden'
}

ERROR_CODE = {
    'BAD_DATA_DATE': 'Ensure your provided date is at least one of the following format: %Y-%m-%d %H:%M:%S, %Y-%m-%d %H:%M, %Y-%m-%d %H, %Y-%m-%d, %Y-%m, %Y',
    'BAD_DATA_INT': 'The size parameter must be of type Integer'
}
