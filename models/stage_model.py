import csv
import json
import datetime
import copy
from decimal import Decimal
from models.riders_model import RidersCollection
from models.result_model import ResultsCollection
from models.prime_results_model import PrimeResultsCollection
from zp_request_library import ZPRequests

from data_shapes import (
    CATEGORY_SHAPE,
    WINNING_TIMES_SHAPE,
    PRIME_CATEGORY_SHAPE,
    SINGLE_POINTS,
    DOUBLE_POINTS,
    CATEGORIES
)


class StageModel:
    def __init__(
            self,
            event_id,
            sprints = [],
            koms = [],
            sprint_points = DOUBLE_POINTS,
            kom_points = SINGLE_POINTS,
            finish_sprint = False,
            finish_points = DOUBLE_POINTS
        ):
        '''
            event_id: (int) the zwift power event id
            sprints: (list) list of sprint ids
            koms: (list) list of kom ids
        '''
        # initialize class properties
        self.event_id = event_id
        print(f'Setting up model and fetching data for Zwift Power event ID {self.event_id}...')
        self.sprints = sprints
        self.koms = koms
        self.finish_sprint = finish_sprint
        self.finish_points = finish_points
        self.custom_primes = copy.deepcopy(PRIME_CATEGORY_SHAPE)

        ## network requests to get data ##
        self.zp_requests = ZPRequests(event_id)
        self.results_data = self.zp_requests.get_results()["data"]
        self.prime_data = self.zp_requests.get_prime_results()["data"]

        # instantiate a new RidersCollection model - loads rider data
        self.riders_collection = RidersCollection()

        # instantiate a new ResultsCollection model - loads stage results
        self.results_collection = ResultsCollection(self.results_data, self.riders_collection.registered_zwids, self.riders_collection.registered_riders)

        # instantiate a new PrimeResultsCollection model - loads sprint and kom results
        if self.prime_data:
            self.prime_data = self.zp_requests.prime_results["data"]
            self.prime_results_collection = PrimeResultsCollection(self.prime_data, self.riders_collection, self.sprints, self.koms)
            if self.finish_sprint:
                for cat in CATEGORIES:
                    self.calculate_finish_line_sprint_points(cat)

    def is_valid_prime(self, prime):
        # check if this prime is valid
        if prime in self.sprints:
            return True
        if prime in self.koms:
            return True
        if self.finish_sprint and prime == "finish":
            return True
        return False

    def calculate_finish_line_sprint_points(self, category):
        # assign sprint points at finish times
        results = self.convert_results_to_prime_results(self.results_collection.results[category][:10])
        results_with_points = self.prime_results_collection.add_points_to_custom_prime(results, self.finish_points)
        self.custom_primes[category]["finish"] = results_with_points

    def convert_results_to_prime_results(self, results):
        # used to to assign sprint points to finish line
        res_copy = copy.deepcopy(results)
        converted_results = []
        for rider in res_copy:
            prime_result = {
                "zp_name": rider["zp_name"],
                "time": rider["race_time"],
                "zwid": rider["zwid"],
                "registered_name": rider["registered_name"],
                "points": 0,
                "gender": rider["gender"]
            }
            converted_results.append(prime_result)
        return converted_results

    def print_all_results(self, stage):
        # attempt to print both stage results and prime results for all cats
        for cat in CATEGORIES:
            print(f'Exporting Cat {cat.upper()} results for stage {stage}: Zwift Power event ID {self.event_id}')
            self.print_stage_results(cat, stage)
            print(f'Exporting Cat A sprint and KOM results for stage {stage}: Zwift Power event ID {self.event_id}')
            self.print_prime_results(cat, stage)

    def print_stage_results(self, category, stage):
        # attempt to create a csv from results
        data = self.results_collection.results[category]
        keys = data[0].keys()
        with open(f'./results/stage_{stage}/stage_{stage}_results_{category}.csv', 'w', newline='')  as output_file:
            dict_writer = csv.DictWriter(output_file, ["registered_name", "category", "gender", "display_race_time", "race_time", "time_diff", "zwid", "zp_name", "team", "subteam"])
            dict_writer.writeheader()
            dict_writer.writerows(data)

    def print_prime_results(self, category, stage):
        # kick off printing results for m, w and special primes
        m_data = self.prime_results_collection.m_winning_times[category]
        self.create_prime_csv(m_data, category, stage, 'm')
        w_data = self.prime_results_collection.w_winning_times[category]
        self.create_prime_csv(w_data, category, stage, 'w')
        special_primes = self.custom_primes[category]
        if self.finish_sprint and special_primes:
            self.create_prime_csv(special_primes, category, stage, 'a')

    def create_prime_csv(self, data, category, stage, gender):
        # attempt to create a csv from prime results
        keys = data.keys()
        for key in keys:
            if data[key] and self.is_valid_prime(key):
                with open(f'./results/stage_{stage}/{gender}_prime_results_{category}_{key}.csv', 'w', newline='')  as output_file:
                    dict_writer = csv.DictWriter(output_file, ["registered_name", "gender", "time", "zwid", "zp_name", "points"])
                    dict_writer.writeheader()
                    dict_writer.writerows(data[key])
