# -*- coding:utf-8 -*-
import sys
sys.path.append('/usr/src/app/api')
import falcon
from main.ressource.search_analytics_ressource import SearchAnalyticsRessource
from main.helpers.helpers import CORSComponent
from falcon_swagger_ui import register_swaggerui_app
from main.utilities.constants import SWAGGERUI_URL, PAGE_TITLE, SCHEMA_URL,FAVICON_URL, SWAGGER_CONF
import pathlib

STATIC_PATH = '/usr/src/app/api/static'

# main api app
app = falcon.API()

#set up middle war
app = falcon.API(middleware=[
    CORSComponent()
])

searchAnalytics = SearchAnalyticsRessource()

# handle all requests to the /1/queries URL
base_jobplatform_route = '/1/queries'

app.add_route(base_jobplatform_route+'/count/{date}', searchAnalytics, suffix='queries_count')
app.add_route(base_jobplatform_route+'/popular/{date}', searchAnalytics, suffix='popular_queries')

app.add_static_route('/static', str(STATIC_PATH))

register_swaggerui_app(app, SWAGGERUI_URL, SCHEMA_URL, page_title = PAGE_TITLE, favicon_url = FAVICON_URL, config = SWAGGER_CONF)