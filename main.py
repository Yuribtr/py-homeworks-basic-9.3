import requests
import time
from datetime import datetime
from http.client import responses
import html


# API description here: https://api.stackexchange.com/docs/questions
class SOClient:
    def __init__(self, token=None):
        # self.TOKEN = {'Authorization': 'OAuth ' + token}
        self.HOST_API = 'https://api.stackexchange.com'
        self.QUESTIONS_SCHEME = '/2.2/questions'
        self.USER_AGENT = {"User-Agent": "Netology"}
        # self.HEADERS = {**self.USER_AGENT, **self.TOKEN}
        self.HEADERS = {**self.USER_AGENT}
        self.QUESTIONS_PARAMS = {'site': 'stackoverflow', 'order': 'desc', 'sort': 'activity'}

    def __do_request(self, method='get', url=None, params=None, headers=None, files=None):
        """This private method is middleware for insertion headers and other info in request in same manner"""
        if headers is None:
            headers = self.HEADERS
        if params is None:
            params = {}
        if url is None:
            url = self.HOST_API + self.QUESTIONS_SCHEME
        if method == 'get':
            return requests.get(url, params=params, headers=headers)
        if method == 'put':
            return requests.put(url, params=params, headers=headers, files=files)
        if method == 'post':
            return requests.post(url, params=params, headers=headers)
        return 'method not defined'

    def get_questions(self, days_ago=2, tag='python', pagesize=100):
        result = []
        page = 1
        try:
            while True:
                print('loading ' + str(pagesize*page) + ' items')
                fromdate = int(time.time() - 60 * 60 * 24 * days_ago)
                params = {'fromdate': fromdate, 'tagged': tag,
                          'pagesize': pagesize, 'page': page, **self.QUESTIONS_PARAMS}
                request = self.__do_request('get', url=self.HOST_API + self.QUESTIONS_SCHEME, params=params)
                if not (200 <= request.status_code < 300):
                    result += [f'Request failed. Error code: {request.status_code} ('
                               f'{responses[request.status_code]})']
                    return result
                res_json = request.json()
                result += [f'{datetime.fromtimestamp(x["creation_date"])} - {html.unescape(x["title"])}'
                          for x in res_json['items']]
                if not res_json['has_more']:
                    result += [f'Found {len(result)} topics. Left {str(res_json["quota_remaining"])} quotas from '
                               f'{str(res_json["quota_max"])}']
                    break
                page += 1
        except Exception as err:
            result += ['Exception raised. Error code: {0}'.format(err)]
            return result
        return result


print('Loading questions. Please wait...')
soclient = SOClient()
print(*soclient.get_questions(), sep='\n')
