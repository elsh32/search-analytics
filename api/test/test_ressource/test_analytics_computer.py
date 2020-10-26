import falcon
from falcon import testing
import json
import pytest
from api.server import app

@pytest.fixture()
def client():
    return app


def test_get_queries_count(client):
    doc_count_2015 = {
        'count': 573697
    }
    doc_count_2015_08_03_00_04 = { 'count': 617 }

    count_2015 = client.simulate_get('/1/queries/count/2015')
    count_2015_08 =  client.simulate_get('/1/queries/count/2015-08')
    count_2015_08_03_00_04 = client.simulate_get('/1/queries/count/2015-08-01 00:04')

    assert count_2015.json == doc_count_2015
    assert count_2015_08.json == doc_count_2015
    assert count_2015_08_03_00_04.json == doc_count_2015_08_03_00_04


def test_get_popular_queries(client):

    top_3_expected =  {
      queries: [
        { 'query': 'http%3A%2F%2Fwww.getsidekick.com%2Fblog%2Fbody-language-advice', 'count': 6675 },
        { 'query': 'http%3A%2F%2Fwebboard.yenta4.com%2Ftopic%2F568045', 'count': 4652 },
        { 'query': 'http%3A%2F%2Fwebboard.yenta4.com%2Ftopic%2F379035%3Fsort%3D1', 'count': 3100 }
      ]
    }

    top_5_expected = {
      queries: [
        { 'query': 'http%3A%2F%2Fwww.getsidekick.com%2Fblog%2Fbody-language-advice', 'count': 2283 },
        { 'query': 'http%3A%2F%2Fwebboard.yenta4.com%2Ftopic%2F568045', 'count': 1943 },
        { 'query': 'http%3A%2F%2Fwebboard.yenta4.com%2Ftopic%2F379035%3Fsort%3D1', 'count': 1358 },
        { 'query': 'http%3A%2F%2Fjamonkey.com%2F50-organizing-ideas-for-every-room-in-your-house%2F', 'count': 890 },
        { 'query': 'http%3A%2F%2Fsharingis.cool%2F1000-musicians-played-foo-fighters-learn-to-fly-and-it-was-epic', 'count': 701 }
      ]
    }

    top_3_actual = client.simulate_get('/1/queries/popular/2015?size=3')
    top_5_actual = client.simulate_get('/1/queries/popular/2015-08-02?size=5')

    assert top_5_actual.json == top_5_expected
    assert top_3_actual.json == top_3_expected


