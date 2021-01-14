import requests
import json
import copy


class ZPRequests:
    def __init__(self, event_id):
        self.event_id = event_id
        self.url = 'https://www.zwiftpower.com/cache3/results/{id}_zwift.json?_=1610548964682'.format(id=self.event_id)
        self.load_event_results()

    def load_event_results(self):
        # url = RESULT_BASE_URL.format(event_id=self.event_id)
        response = requests.get(self.url)
        results = response.json()
        self.results = results

    def get_results(self):
        return self.results
