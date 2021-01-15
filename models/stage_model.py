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
    DOUBLE_POINTS
)


class StageModel:
    def __init__(
            self, event_id,
            finish_sprint = False,
            sprints = [],
            koms = [],
            sprint_points = DOUBLE_POINTS,
            kom_points = SINGLE_POINTS,
            finish_points = DOUBLE_POINTS
        ):
        '''
            event_id: (int) the zwift power event id
            sprints: (list) list of sprint ids
            koms: (list) list of kom ids
        '''
        # initialize class properties
        self.event_id = event_id
        self.sprints = sprints
        self.koms = koms
        self.finish_sprint = finish_sprint
        self.finish_points = finish_points
        self.zp_requests = ZPRequests(event_id)
        self.results_data = self.zp_requests.get_results()["data"]
        self.prime_data = self.zp_requests.get_prime_results()["data"]
        # instantiate a new RidersCollection and load rider data
        self.riders_collection = RidersCollection()
        # instantiate a new ResultsCollection and load stage results
        self.results_collection = ResultsCollection(self.results_data, self.riders_collection.registered_zwids, self.riders_collection.registered_riders)
        if self.prime_data:
            self.prime_data = self.zp_requests.prime_results["data"]
            # instantiate a new PrimeResultsCollection and load prime results
            self.prime_results_collection = PrimeResultsCollection(self.prime_data, self.riders_collection, self.sprints, self.koms)

    def clear_model(self):
        # wipe all data
        self.results_data = []
        self.riders = copy.deepcopy(CATEGORY_SHAPE)
        self.stage_results = copy.deepcopy(CATEGORY_SHAPE)
        self.filtered_stage_results = copy.deepcopy(CATEGORY_SHAPE)
        # self.registered_zwids = copy.deepcopy(CATEGORY_SHAPE)
        self.winning_times = copy.deepcopy(WINNING_TIMES_SHAPE)
        self.prime_results = copy.deepcopy(PRIME_CATEGORY_SHAPE)

    def print_stage_results(self, category, stage):
        # attempt to create a csv from results
        data = self.results_collection.results[category]
        keys = data[0].keys()
        with open(f'./results/stage_{stage}/stage_{stage}_results_{category}.csv', 'w', newline='')  as output_file:
            dict_writer = csv.DictWriter(output_file, ["registered_name", "category", "gender", "display_race_time", "race_time", "time_diff", "zwid", "zp_name", "team", "subteam"])
            dict_writer.writeheader()
            dict_writer.writerows(data)

    def print_prime_results(self, category, stage):
        # attempt to create a csv from results
        m_data = self.prime_results_collection.m_winning_times[category]
        self.create_prime_csv(m_data, category, stage, 'm')
        w_data = self.prime_results_collection.w_winning_times[category]
        self.create_prime_csv(w_data, category, stage, 'w')

    def create_prime_csv(self, data, category, stage, gender):
        keys = data.keys()
        for key in keys:
            with open(f'./results/stage_{stage}/{gender}_prime_results_{category}_{key}.csv', 'w', newline='')  as output_file:
                dict_writer = csv.DictWriter(output_file, ["registered_name", "gender", "time", "zwid", "zp_name", "points"])
                dict_writer.writeheader()
                dict_writer.writerows(data[key])

    # @TODO - use this function to calculate sprint points for finish line
    def calculate_finish_line_sprint_points(self, category):
        results = self.results_collection.winning_times[category]
        results_with_points = self.prime_results_collection.add_points_to_custom_prime(results, finish_points)
        self.prime_results_collection.custom_primes[category]["finish"] = results_with_points
