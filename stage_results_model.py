import csv
import json
import datetime
import copy
from decimal import Decimal
from riders_model import RidersCollection
from result_model import ResultsCollection

from data_shapes import (
    RIDERS_SHAPE,
    RESULTS_SHAPE,
    FILTERED_STAGE_RESULTS_SHAPE,
    REGISTERED_ZWIDS_SHAPE,
    WINNING_TIMES_SHAPE,
    PRIME_RESULTS_SHAPE
)


class StageResultsModel:
    def __init__(self, results_input_data, a_prime, b_prime, c_prime, d_prime):
        # initialize class properties
        self.riders_collection = RidersCollection()
        self.riders_collection.load_rider_list()
        self.stage_results = copy.deepcopy(RESULTS_SHAPE)
        self.filtered_stage_results = copy.deepcopy(FILTERED_STAGE_RESULTS_SHAPE)
        # self.registered_zwids = copy.deepcopy(REGISTERED_ZWIDS_SHAPE)
        self.winning_times = copy.deepcopy(WINNING_TIMES_SHAPE)
        self.prime_results = copy.deepcopy(PRIME_RESULTS_SHAPE)
        self.results_input_data = results_input_data # set initial JSON data on the class
        # self.load_results() #load stage results from JSON data
        self.results_collection = ResultsCollection(self.results_input_data, self.riders_collection.registered_zwids)
        self.results_collection.load_results(self.riders_collection.registered_riders)
        # self.load_prime_results(a_prime, "a")
        # self.load_prime_results(b_prime, "b")
        # self.load_prime_results(c_prime, "c")
        # self.load_prime_results(d_prime, "d")

    def clear_model(self):
        # wipe all data
        self.results_input_data = []
        self.riders = copy.deepcopy(RIDERS_SHAPE)
        self.stage_results = copy.deepcopy(RESULTS_SHAPE)
        self.filtered_stage_results = copy.deepcopy(FILTERED_STAGE_RESULTS_SHAPE)
        # self.registered_zwids = copy.deepcopy(REGISTERED_ZWIDS_SHAPE)
        self.winning_times = copy.deepcopy(WINNING_TIMES_SHAPE)
        self.prime_results = copy.deepcopy(PRIME_RESULTS_SHAPE)

    # def load_prime_results(self, prime_input_data, cat):
    #     # loads prime results into the model
    #     all_primes = json.loads(prime_input_data)["data"]
    #     for prime in all_primes:
    #         self.calculate_prime_results(prime, cat)
    #
    # def calculate_prime_results(self, prime, cat):
    #     # sorts the prime results by fastest time over all laps
    #     primes_names = self.prime_results[cat].keys()
    #     name = prime["name"]
    #     if name not in primes_names:
    #         self.prime_results[cat][name] = []
    #     one = prime["rider_1"]
    #     two = prime["rider_2"]
    #     three = prime["rider_3"]
    #     four = prime["rider_4"]
    #     five = prime["rider_5"]
    #     six = prime["rider_6"]
    #     seven = prime["rider_7"]
    #     eight = prime["rider_8"]
    #     nine = prime["rider_9"]
    #     ten = prime["rider_10"]
    #     riders = [one, two, three, four, five, six, seven, eight, nine, ten]
    #     validated_riders = []
    #     for rider in riders:
    #         if self.validate_prime(rider, cat):
    #             filtered_rider = {
    #                 "name": rider["name"],
    #                 "elapsed": rider["elapsed"],
    #                 "zwid": rider["zwid"] if rider["zwid"] else 0
    #             }
    #             validated_riders.append(filtered_rider)
    #     if len(validated_riders) > 0:
    #         if len(self.prime_results[cat][name]) > 0:
    #             for rider in validated_riders:
    #                 for i in range(len(self.prime_results[cat][name])):
    #                     if rider["elapsed"] < self.prime_results[cat][name][i]["elapsed"]:
    #                         rider_data = {
    #                             "name": rider["name"],
    #                             "elapsed": rider["elapsed"],
    #                             "zwid": rider["zwid"] if rider["zwid"] else 0
    #                         }
    #                         self.prime_results[cat][name].insert(i, rider)
    #                         break
    #         else:
    #             self.prime_results[cat][name] = validated_riders
    #     return None
    #
    # def validate_prime(self, prime, cat):
    #     registered_zwids = self.riders_collection.registered_zwids[cat]
    #     if str(prime["zwid"]) in registered_zwids:
    #         return True
    #     return False
    #
    # def add_rider_data_to_prime_results(self, results, cat):
    #     new_results = []
    #     for result in results:
    #         new_result = dict(result)
    #         for rider in self.riders_collection.registered_riders[cat]:
    #             if int(rider.zwid) == int(result["zwid"]):
    #                 new_result["registered_name"] = rider.name
    #                 new_result["team"] = rider.team
    #                 new_result["subteam"] = rider.subteam
    #                 new_result["gender"] = rider.gender
    #         new_results.append(new_result)
    #     return new_results
    #
    # def filter_prime_results(self, results):
    #     # removes duplicate riders so each rider only has a single best time
    #     # separates womens results and adds them to the end
    #     filtered_results = []
    #     filtered_w_results = []
    #     in_filtered_results = False
    #     for r in results:
    #         if r["gender"] == '1':
    #             if len(filtered_results) > 0:
    #                 for f in filtered_results:
    #                     if r["registered_name"] == f["registered_name"]:
    #                         in_filtered_results = True
    #             if len(filtered_results) < 10 and not in_filtered_results:
    #                 filtered_results.append(r)
    #         elif r["gender"] == '2':
    #             if len(filtered_w_results) > 0:
    #                 for f in filtered_w_results:
    #                     if r["registered_name"] == f["registered_name"]:
    #                         in_filtered_results = True
    #             if len(filtered_w_results) < 10 and not in_filtered_results:
    #                 filtered_w_results.append(r)
    #         in_filtered_results = False
    #     filtered_results.extend(filtered_w_results)
    #     return filtered_results

    def get_veganuary_stage_results(self, category, stage):
        # attempt to create a csv from results
        data = self.results_collection.results[category]
        keys = data[0].keys()
        with open(f'./results/stage_{stage}/stage_{stage}_results_{category}.csv', 'w', newline='')  as output_file:
            dict_writer = csv.DictWriter(output_file, ["registered_name", "category", "gender", "display_race_time", "race_time", "time_diff", "zwid", "zp_name", "team", "subteam"])
            dict_writer.writeheader()
            dict_writer.writerows(data)

    def get_veganuary_prime_results(self, category, stage):
        # attempt to create a csv from results
        data = self.prime_results[category]
        keys = data.keys()
        for key in keys:
            results_with_rider_data = self.add_rider_data_to_prime_results(data[key], category)
            final_results = self.filter_prime_results(results_with_rider_data)
            with open(f'./results/stage_{stage}/veganuary_prime_results_{category}_{key.replace(" ", "_")}.csv', 'w', newline='')  as output_file:
                dict_writer = csv.DictWriter(output_file, ["registered_name", "gender", "elapsed", "zwid", "name", "team", "subteam"])
                dict_writer.writeheader()
                dict_writer.writerows(final_results)
