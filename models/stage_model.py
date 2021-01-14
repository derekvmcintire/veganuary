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
    RIDERS_SHAPE,
    RESULTS_SHAPE,
    FILTERED_STAGE_RESULTS_SHAPE,
    REGISTERED_ZWIDS_SHAPE,
    WINNING_TIMES_SHAPE,
    PRIME_RESULTS_SHAPE,
    SINGLE_POINTS,
    DOUBLE_POINTS
)


class StageModel:
    def __init__(self, event_id, sprints = [], koms = [], sprint_points = DOUBLE_POINTS, kom_points = SINGLE_POINTS):
        '''
            event_id: (int) the zwift power event id
            sprints: (list) list of sprint ids
            koms: (list) list of kom ids
        '''
        # initialize class properties
        self.event_id = event_id
        self.sprints = sprints
        self.koms = koms
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
        self.riders = copy.deepcopy(RIDERS_SHAPE)
        self.stage_results = copy.deepcopy(RESULTS_SHAPE)
        self.filtered_stage_results = copy.deepcopy(FILTERED_STAGE_RESULTS_SHAPE)
        # self.registered_zwids = copy.deepcopy(REGISTERED_ZWIDS_SHAPE)
        self.winning_times = copy.deepcopy(WINNING_TIMES_SHAPE)
        self.prime_results = copy.deepcopy(PRIME_RESULTS_SHAPE)

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
        data = self.prime_results_collection.winning_times[category]
        keys = data.keys()
        for key in keys:
            with open(f'./results/stage_{stage}/veganuary_prime_results_{category}_{key}.csv', 'w', newline='')  as output_file:
                dict_writer = csv.DictWriter(output_file, ["registered_name", "time", "zwid", "zp_name", "points"])
                dict_writer.writeheader()
                dict_writer.writerows(data[key])
