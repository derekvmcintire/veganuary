import copy
import json
from dataclasses import dataclass, asdict

from models.riders_model import RidersCollection

from data_shapes import (
    RESULTS_SHAPE,
    PRIME_RESULTS_SHAPE,
    SINGLE_POINTS,
    DOUBLE_POINTS,
    SPRINT_TYPE,
    KOM_TYPE
)

CATEGORIES = ['a', 'b', 'c', 'd']

@dataclass
class PrimeModel:
    zp_name: str = ""
    time: float = 0
    zwid: int = 0
    registered_name: str = ""
    points: int = 0


class PrimeResultsCollection:
    def __init__(self, input_data, riders_collection: RidersCollection, sprints = [], koms = [], sprint_points = DOUBLE_POINTS, kom_points = SINGLE_POINTS):
        self.input_data = input_data
        self.prime_data = copy.deepcopy(RESULTS_SHAPE)
        self.riders_collection = riders_collection
        self.sprints = sprints
        self.koms = koms
        self.sprint_points = sprint_points
        self.kom_points = kom_points
        self.winning_times = copy.deepcopy(PRIME_RESULTS_SHAPE)
        self.prime_results = copy.deepcopy(PRIME_RESULTS_SHAPE)
        self.load_prime_data()
        for cat in CATEGORIES:
            self.calculate_primes_results(cat)

    def load_prime_data(self):
        primes = self.input_data[0]["msec"].keys()
        for key in primes:
            self.prime_results["a"][key] = []
            self.prime_results["b"][key] = []
            self.prime_results["c"][key] = []
            self.prime_results["d"][key] = []
        for data in self.input_data:
            cat = data["category"].lower()
            self.prime_data[cat].append(data)

    def calculate_primes_results(self, category):
        for data in self.prime_data[category]:
            primes = data["msec"].keys()
            # validate data is from a registered rider
            if data["zwid"] in self.riders_collection.registered_zwids[category]:
                # get all the primes from this race
                for prime in primes:
                    if len(self.prime_results[category][prime]) > 0:
                        for i in range(len(self.prime_results[category][prime])):
                            if data["msec"][prime] < self.prime_results[category][prime][i]["time"]:
                                prime_model = self.build_prime_model(data, prime)
                                self.prime_results[category][prime].insert(i, asdict(prime_model))
                                break
                            if (i + 1) == len(self.prime_results[category][prime]):
                                # if we are on the last entry, then add the prime result to the end
                                prime_model = self.build_prime_model(data, prime)
                                self.prime_results[category][prime].append(asdict(prime_model))
                                break
                    else:
                        # this should only happen on the first entry
                        prime_model = self.build_prime_model(data, prime)
                        self.prime_results[category][prime].append(asdict(prime_model))
        # grab only the top 10 fastest times and set the winners
        for results in self.prime_results[category]:
            primes = data["msec"].keys()
            for prime in primes:
                results_with_points = self.award_points(prime, self.prime_results[category][prime][:10])
                self.winning_times[category][prime] = results_with_points

    def build_prime_model(self, data, prime):
        prime_model = PrimeModel(zp_name = data["name"], time = data["msec"][prime], zwid = data["zwid"])
        registered_name = self.riders_collection.get_rider_by_zwid(data["zwid"])
        prime_model.registered_name = registered_name
        return prime_model

    def award_points(self, prime_id, results):
        points = 0
        for i in range(len(results)):
            if prime_id in self.sprints:
                points = self.sprint_points[i]
            elif prime_id in self.koms:
                points = self.kom_points[i]
            if points > 0:
                results[i]["points"] = points
        return results
