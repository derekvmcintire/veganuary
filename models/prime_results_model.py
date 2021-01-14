import copy
import json
from dataclasses import dataclass, asdict

from data_shapes import (
    RESULTS_SHAPE,
    PRIME_RESULTS_SHAPE
)

CATEGORIES = ['a', 'b', 'c', 'd']

@dataclass
class PrimeModel:
    name: str = ""
    time: float = 0
    zwid: int = 0


class PrimeResultsCollection:
    def __init__(self, input_data, registered_zwids):
        self.input_data = input_data
        self.registered_zwids = registered_zwids
        self.winning_times = copy.deepcopy(PRIME_RESULTS_SHAPE)
        self.prime_data = copy.deepcopy(RESULTS_SHAPE)
        self.prime_results = copy.deepcopy(PRIME_RESULTS_SHAPE)
        self.load_all_prime_data(self.input_data)
        for cat in CATEGORIES:
            self.calculate_primes_results(cat)


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

    def calculate_primes_results(self, category):
        for data in self.prime_data[category]:
            primes = data["msec"].keys()
            # validate data is from a registered rider
            if data["zwid"] in self.registered_zwids[category]:
                # get all the primes from this race
                for prime in primes:
                    if len(self.prime_results[category][prime]) > 0:
                        for i in range(len(self.prime_results[category][prime])):
                            if data["msec"][prime] < self.prime_results[category][prime][i]["time"]:
                                prime_model = PrimeModel(data["name"], data["msec"][prime], data["zwid"])
                                self.prime_results[category][prime].insert(i, asdict(prime_model))
                                break
                            if (i + 1) == len(self.prime_results[category][prime]):
                                # if we are on the last entry, then add the prime result to the end
                                self.prime_results[category][prime].append(asdict(prime_model))
                                break
                    else:
                        # this should only happen on the first entry
                        prime_model = PrimeModel(data["name"], data["msec"][prime], data["zwid"])
                        self.prime_results[category][prime].append(asdict(prime_model))
        # grab only the top 10 fastest times and set the winners
        for results in self.prime_results[category]:
            primes = data["msec"].keys()
            for prime in primes:
                self.winning_times[category][prime] = self.prime_results[category][prime][:10]
