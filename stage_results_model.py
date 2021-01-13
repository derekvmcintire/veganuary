import csv
import json
import datetime
import copy
from decimal import Decimal

from data_shapes import (
    RIDERS_SHAPE,
    STAGE_RESULTS_SHAPE,
    FILTERED_STAGE_RESULTS_SHAPE,
    REGISTERED_ZWIDS_SHAPE,
    WINNING_TIMES_SHAPE,
    PRIME_RESULTS_SHAPE
)


class StageResultsModel:
    def __init__(self, results_input_data, a_prime, b_prime, c_prime, d_prime):
        # initialize class properties
        self.riders = copy.deepcopy(RIDERS_SHAPE)
        self.stage_results = copy.deepcopy(STAGE_RESULTS_SHAPE)
        self.filtered_stage_results = copy.deepcopy(FILTERED_STAGE_RESULTS_SHAPE)
        self.registered_zwids = copy.deepcopy(REGISTERED_ZWIDS_SHAPE)
        self.winning_times = copy.deepcopy(WINNING_TIMES_SHAPE)
        self.prime_results = copy.deepcopy(PRIME_RESULTS_SHAPE)
        self.results_input_data = results_input_data # set initial JSON data on the class
        self.load_rider_list() # load rider registration list from csv
        # load the registered zwids by category
        self.registered_zwids["a"] = self.get_registered_zwids(self.riders["a"])
        self.registered_zwids["b"] = self.get_registered_zwids(self.riders["b"])
        self.registered_zwids["c"] = self.get_registered_zwids(self.riders["c"])
        self.registered_zwids["d"] = self.get_registered_zwids(self.riders["d"])
        self.load_results() #load stage results from JSON data
        self.load_prime_results(a_prime, "a")
        self.load_prime_results(b_prime, "b")
        self.load_prime_results(c_prime, "c")
        self.load_prime_results(d_prime, "d")

    def clear_model(self):
        # wipe all data
        self.results_input_data = []
        self.riders = copy.deepcopy(RIDERS_SHAPE)
        self.stage_results = copy.deepcopy(STAGE_RESULTS_SHAPE)
        self.filtered_stage_results = copy.deepcopy(FILTERED_STAGE_RESULTS_SHAPE)
        self.registered_zwids = copy.deepcopy(REGISTERED_ZWIDS_SHAPE)
        self.winning_times = copy.deepcopy(WINNING_TIMES_SHAPE)
        self.prime_results = copy.deepcopy(PRIME_RESULTS_SHAPE)

    def load_rider_list(self):
        # Loads the list of riders from the csv file in this directory
        rider_list_file = open('./veganuary_data/rider_list_with_gender.csv', 'r')
        rider_list = csv.reader(rider_list_file)
        for row in rider_list:
            rider = {
                "id": row[0],
                "name": row[1],
                "team": row[2],
                "category": row[4],
                "subteam": row[3],
                "zp_name": row[5],
                "zwid": row[6],
                "gender": row[7]
            }
            if rider["category"] == "A":
                self.riders["a"].append(rider)
            elif rider["category"] == "B":
                self.riders["b"].append(rider)
            elif rider["category"] == "C":
                self.riders["c"].append(rider)
            elif rider["category"] == "D":
                self.riders["d"].append(rider)

    def load_results(self):
        # loads results from JSON and divides by category
        if (self.results_input_data):
            all_results = json.loads(self.results_input_data)["data"]
            for result in all_results:
                cat = self.get_cat_from_label(result["label"])
                if self.validate_result(result, cat):
                    # store winning times so we can calculate time difference
                    if len(self.stage_results[cat]) == 0:
                        self.winning_times[cat] = Decimal(result["race_time"][0])
                    filtered_result = self.get_filtered_result_data(result)
                    res = self.add_registered_data_to_result(filtered_result)
                    self.stage_results[cat].append(res)

    def load_prime_results(self, prime_input_data, cat):
        # loads prime results into the model
        all_primes = json.loads(prime_input_data)["data"]
        for prime in all_primes:
            self.calculate_prime_results(prime, cat)

    def calculate_prime_results(self, prime, cat):
        # sorts the prime results by fastest time over all laps
        primes_names = self.prime_results[cat].keys()
        name = prime["name"]
        if name not in primes_names:
            self.prime_results[cat][name] = []
        one = prime["rider_1"]
        two = prime["rider_2"]
        three = prime["rider_3"]
        four = prime["rider_4"]
        five = prime["rider_5"]
        six = prime["rider_6"]
        seven = prime["rider_7"]
        eight = prime["rider_8"]
        nine = prime["rider_9"]
        ten = prime["rider_10"]
        riders = [one, two, three, four, five, six, seven, eight, nine, ten]
        validated_riders = []
        for rider in riders:
            if self.validate_prime(rider, cat):
                filtered_rider = {
                    "name": rider["name"],
                    "elapsed": rider["elapsed"],
                    "zwid": rider["zwid"] if rider["zwid"] else 0
                }
                validated_riders.append(filtered_rider)
        if len(validated_riders) > 0:
            if len(self.prime_results[cat][name]) > 0:
                for rider in validated_riders:
                    for i in range(len(self.prime_results[cat][name])):
                        if rider["elapsed"] < self.prime_results[cat][name][i]["elapsed"]:
                            rider_data = {
                                "name": rider["name"],
                                "elapsed": rider["elapsed"],
                                "zwid": rider["zwid"] if rider["zwid"] else 0
                            }
                            self.prime_results[cat][name].insert(i, rider)
                            break
            else:
                self.prime_results[cat][name] = validated_riders
        return None


    def filter_emojis(self, text):
        # need to filter out emojis from ZP names
        result = text.encode('unicode-escape').decode('ascii')
        return result

    def get_filtered_result_data(self, result):
        # filters out extra data and sets time data
        cat = self.get_cat_from_label(result["label"])
        # store race time as decimal for calculations but convert to datetime
        # object for display purposes
        race_time = Decimal(result["race_time"][0])
        display_race_time = str(datetime.timedelta(seconds=result["race_time"][0]))
        time_diff = self.calculate_time_diff(self.winning_times[cat], race_time)
        filtered_result = {
            "zp_name": self.filter_emojis(result["name"]),
            "zwid": result["DT_RowId"],
            "category": cat,
            "display_race_time": display_race_time,
            "time_diff": time_diff,
            "race_time": race_time
        }
        return filtered_result

    def add_registered_data_to_result(self, result):
        # add rider info to result info
        cat = result["category"]
        new_result = dict(result)
        for rider in self.riders[cat]:
            if int(rider["zwid"]) == int(result["zwid"]):
                new_result["registered_name"] = rider["name"]
                new_result["team"] = rider["team"]
                new_result["subteam"] = rider["subteam"]
                new_result["gender"] = rider["gender"]
                return new_result

    def get_cat_from_label(self, label):
        # cats are stored as label in ZP data
        if label == "1":
            return "a"
        if label == "2":
            return "b"
        if label == "3":
            return "c"
        if label == "4":
            return "d"
        return ""

    def calculate_time_diff(self, winning_time: Decimal, race_time: Decimal):
        # because the time diff should be calculated off the first registered rider
        # and not the overall first finisher, we need to re-calculate
        if winning_time > 0:
            # convert to float for display
            diff = float(race_time - winning_time)
            return str(datetime.timedelta(seconds=diff))
        return 0

    def get_registered_zwids(self, riders):
        # returns a list of registered zwids
        zwids = []
        for rider in riders:
            zwids.append(rider["zwid"])
        return zwids

    def validate_result(self, result, cat):
        # checks if this result is from a registered rider in the correct category
        # if dq_cat is not empty, rider has been DQ'd
        if result["dq_cat"] != "":
            return False
        registered_zwids = self.registered_zwids[cat]
        if result["DT_RowId"] in registered_zwids:
            return True
        return False

    def validate_prime(self, prime, cat):
        registered_zwids = self.registered_zwids[cat]
        if str(prime["zwid"]) in registered_zwids:
            return True
        return False

    def add_rider_data_to_prime_results(self, results, cat):
        new_results = []
        for result in results:
            new_result = dict(result)
            for rider in self.riders[cat]:
                if int(rider["zwid"]) == int(result["zwid"]):
                    new_result["registered_name"] = rider["name"]
                    new_result["team"] = rider["team"]
                    new_result["subteam"] = rider["subteam"]
                    new_result["gender"] = rider["gender"]
            new_results.append(new_result)
        return new_results

    def filter_prime_results(self, results):
        # removes duplicate riders so each rider only has a single best time
        # separates womens results and adds them to the end
        filtered_results = []
        filtered_w_results = []
        in_filtered_results = False
        for r in results:
            if r["gender"] == '1':
                if len(filtered_results) > 0:
                    for f in filtered_results:
                        if r["registered_name"] == f["registered_name"]:
                            in_filtered_results = True
                if len(filtered_results) < 10 and not in_filtered_results:
                    filtered_results.append(r)
            elif r["gender"] == '2':
                if len(filtered_w_results) > 0:
                    for f in filtered_w_results:
                        if r["registered_name"] == f["registered_name"]:
                            in_filtered_results = True
                if len(filtered_w_results) < 10 and not in_filtered_results:
                    filtered_w_results.append(r)
            in_filtered_results = False
        filtered_results.extend(filtered_w_results)
        return filtered_results

    def get_veganuary_stage_results(self, category, stage):
        # attempt to create a csv from results
        data = self.stage_results[category]
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
