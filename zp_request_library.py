import requests
import json
import copy


class ZPRequests:
    # Prime data is working for stage 2
    # Prime data from ZP for stage 1 is totally wrong. If data is consistent from
    # stage to stage, this will work, but incorrect data will obviously produce
    # incorrect results
    def __init__(self, event_id=None):
        self.error = None
        self.event_id = event_id
        self.results = []
        self.prime_results = []
        self.result_url = 'https://www.zwiftpower.com/cache3/results/{id}_zwift.json'.format(id=self.event_id)
        self.prime_url = 'https://www.zwiftpower.com/api3.php?do=event_sprints&zid={id}'.format(id=self.event_id)
        self.load_event_results()
        self.load_prime_results()

    def load_event_results(self):
        try:
            response = requests.get(self.result_url)
            results = response.json()
            self.results = results
        except:
            self.error = "Loading Results"

    def load_prime_results(self):
        try:
            req = requests.options(
                self.prime_url,
                headers = {
                    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                }
            )
            self.prime_results = req.json()
        except:
            self.error = "Loading Prime Results"

    def get_results(self):
        if self.results:
            return self.results
        return []

    def get_prime_results(self):
        if self.prime_results:
            return self.prime_results
        return []
