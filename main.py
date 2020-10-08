import requests
import time
from datetime import datetime
from http.client import responses
import html


# API description here: https://api.stackexchange.com/docs/questions
class SoClient:
    def __init__(self):
        self.HOST_API = 'https://api.stackexchange.com'
        self.QUESTIONS_SCHEME = '/2.2/questions'
        self.USER_AGENT = {'User-Agent': 'Netology'}
        self.HEADERS = {**self.USER_AGENT}
        self.QUESTIONS_PARAMS = {'site': 'stackoverflow', 'order': 'desc', 'sort': 'activity'}

    def get_questions(self, days_ago=2, tag='python', pagesize=100):
        """Method returns list of stackoverflow questions for specified period and tag"""
        result = []
        page = 1
        try:
            while True:
                print('loading ' + str(pagesize * page) + ' items')
                fromdate = int(time.time() - 60 * 60 * 24 * days_ago)
                params = {'fromdate': fromdate, 'tagged': tag,
                          'pagesize': pagesize, 'page': page, **self.QUESTIONS_PARAMS}
                request = requests.get(self.HOST_API + self.QUESTIONS_SCHEME, params=params, headers=self.HEADERS)
                # in case of network or API error we return this error and all questions grabbed before
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
soclient = SoClient()
print(*soclient.get_questions(), sep='\n')
