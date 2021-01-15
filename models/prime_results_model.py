import copy
import json
from dataclasses import dataclass, asdict

from models.riders_model import RidersCollection

from data_shapes import (
    CATEGORY_SHAPE,
    PRIME_CATEGORY_SHAPE,
    SINGLE_POINTS,
    DOUBLE_POINTS,
    SPRINT_TYPE,
    KOM_TYPE,
    CATEGORIES
)



@dataclass
class PrimeModel:
    zp_name: str = ""
    time: float = 0
    zwid: int = 0
    registered_name: str = ""
    points: int = 0
    gender: int = 1


class PrimeResultsCollection:
    def __init__(
            self,
            input_data,
            riders_collection: RidersCollection,
            sprints = [],
            koms = [],
            sprint_points = DOUBLE_POINTS,
            kom_points = SINGLE_POINTS
        ):
        self.input_data = input_data
        self.prime_data = copy.deepcopy(CATEGORY_SHAPE)
        self.riders_collection = riders_collection
        self.sprints = sprints
        self.koms = koms
        self.sprint_points = sprint_points
        self.kom_points = kom_points
        self.m_winning_times = copy.deepcopy(PRIME_CATEGORY_SHAPE)
        self.w_winning_times = copy.deepcopy(PRIME_CATEGORY_SHAPE)
        self.prime_results = copy.deepcopy(PRIME_CATEGORY_SHAPE)
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

    def build_prime_results(self, data, prime, category):
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

    def get_prime_results_by_gender(self, results, gender):
        g_results = []
        for r in results:
            if int(r["gender"]) == gender:
                g_results.append(r)
        return g_results

    def calculate_primes_results(self, category):
        for data in self.prime_data[category]:
            primes = data["msec"].keys()
            # validate data is from a registered rider
            if data["zwid"] in self.riders_collection.registered_zwids[category]:
                # get all the primes from this race
                for prime in primes:
                    self.build_prime_results(data, prime, category)
        for results in self.prime_results[category]:
            primes = data["msec"].keys()
            for prime in primes:
                m_results = self.get_prime_results_by_gender(self.prime_results[category][prime], 1)
                w_results = self.get_prime_results_by_gender(self.prime_results[category][prime], 2)
                m_results_with_points = self.award_points(prime, m_results[:10])
                w_results_with_points = self.award_points(prime, w_results[:10])
                self.m_winning_times[category][prime] = m_results_with_points
                self.w_winning_times[category][prime] = w_results_with_points

    def build_prime_model(self, data, prime):
        prime_model = PrimeModel(zp_name = data["name"], time = data["msec"][prime], zwid = data["zwid"])
        rider_data = self.riders_collection.get_rider_by_zwid(data["zwid"])
        registered_name = rider_data.name
        gender = rider_data.gender
        prime_model.registered_name = registered_name
        prime_model.gender = gender
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

    def add_points_to_custom_prime(self, results, point_system = DOUBLE_POINTS):
        # similar to above, but with no verification so it can be called from outside the class
        results_copy = copy.deepcopy(results)
        for i in range(len(results_copy)):
            try:
                points = point_system[i]
                results_copy[i]["points"] = points
            except:
                return None
        return results_copy
