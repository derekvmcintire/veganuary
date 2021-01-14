import csv
import json
import datetime
import copy
from decimal import Decimal
from riders_model import RidersCollection
from result_model import ResultsCollection
from prime_results_model import PrimeResultsCollection

from data_shapes import (
    RIDERS_SHAPE,
    RESULTS_SHAPE,
    FILTERED_STAGE_RESULTS_SHAPE,
    REGISTERED_ZWIDS_SHAPE,
    WINNING_TIMES_SHAPE,
    PRIME_RESULTS_SHAPE
)


class StageModel:
    def __init__(self, results_input_data, prime_input_data):
        # initialize class properties
        self.results_input_data = results_input_data # set initial JSON data on the class
        self.prime_input_data = prime_input_data
        # instantiate a new RidersCollection and load rider data
        self.riders_collection = RidersCollection()
        # instantiate a new ResultsCollection and load stage results
        self.results_collection = ResultsCollection(self.results_input_data, self.riders_collection.registered_zwids, self.riders_collection.registered_riders)
        # instantiate a new PrimeResultsCollection and load prime results
        self.prime_results_collection = PrimeResultsCollection(self.prime_input_data, self.riders_collection.registered_zwids)

    def clear_model(self):
        # wipe all data
        self.results_input_data = []
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
                dict_writer = csv.DictWriter(output_file, ["name", "time", "zwid"])
                dict_writer.writeheader()
                dict_writer.writerows(data[key])
