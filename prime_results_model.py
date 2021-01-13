import copy
import json
from dataclasses import dataclass, asdict

from data_shapes import (
    WINNING_TIMES_SHAPE,
    RESULTS_SHAPE,
    PRIME_RESULTS_SHAPE
)

@dataclass
class PrimeModel:
    name: str = ""
    time: float = 0
    zwid: int = 0


class PrimeResultsCollection:
    def __init__(self, input_data):
        self.input_data = input_data
        self.winning_times = copy.deepcopy(WINNING_TIMES_SHAPE)
        self.prime_data = copy.deepcopy(RESULTS_SHAPE)
        self.prime_results = copy.deepcopy(PRIME_RESULTS_SHAPE)
        self.load_all_prime_data(self.input_data)
        self.calculate_winning_primes("a")

    def load_all_prime_data(self, input_data):
        # loads prime results into the model
        prime_data = json.loads(input_data)["data"]
        self.load_prime_data(prime_data)

    def load_prime_data(self, prime_data):
        primes = prime_data[0]["msec"].keys()
        for key in primes:
            self.prime_results["a"][key] = []
            self.prime_results["b"][key] = []
            self.prime_results["c"][key] = []
            self.prime_results["d"][key] = []
        for data in prime_data:
            cat = data["category"].lower()
            self.prime_data[cat].append(data)

    def calculate_winning_primes(self, category):
        for data in self.prime_data[category]:
            primes = data["msec"].keys()
            for prime in primes:
                if len(self.prime_results[category][prime]) > 0:
                    for i in range(len(self.prime_results[category][prime])):
                        if data["msec"][prime] < self.prime_results[category][prime][i].time:
                            prime_model = PrimeModel(data["name"], data["msec"][prime], data["zwid"])
                            self.prime_results[category][prime].insert(i, prime_model)
                else:
                    prime_model = PrimeModel(data["name"], data["msec"][prime], data["zwid"])
                    self.prime_results[category][prime].append(prime_model)
        breakpoint()

    def validate_prime(self, prime, cat):
        registered_zwids = self.riders_collection.registered_zwids[cat]
        if str(prime["zwid"]) in registered_zwids:
            return True
        return False

    def add_rider_data_to_prime_results(self, results, cat):
        pass

    def filter_prime_results(self, results):
        pass
