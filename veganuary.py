import csv
import json

from data_shapes import (
    RIDERS_SHAPE,
    STAGE_RESULTS_SHAPE,
    FILTERED_STAGE_RESULTS_SHAPE,
    REGISTERED_ZIDS_SHAPE
)


class CalculateResults:
    # initialize class properties
    results_input_data = []
    riders = RIDERS_SHAPE
    stage_results = STAGE_RESULTS_SHAPE
    filtered_stage_results = FILTERED_STAGE_RESULTS_SHAPE
    registered_zids = REGISTERED_ZIDS_SHAPE


    def __init__(self, results_input_data=""):
        self.results_input_data = results_input_data # set initial JSON data on the class
        self.load_rider_list() # load rider registration list from csv
        # load the registered zids by category
        self.registered_zids["a"] = self.get_registered_zids(self.riders["a"])
        self.registered_zids["b"] = self.get_registered_zids(self.riders["b"])
        self.registered_zids["c"] = self.get_registered_zids(self.riders["c"])
        self.registered_zids["d"] = self.get_registered_zids(self.riders["d"])
        self.load_results() #load stage results from JSON data

    def load_rider_list(self):
        # Loads the list of riders from the csv file in this directory
        rider_list_file = open('./rider_list.csv', 'r')
        rider_list = csv.reader(rider_list_file)
        for row in rider_list:
            rider = {
                "id": row[0],
                "name": row[1],
                "team": row[2],
                "category": row[4],
                "subteam": row[3],
                "zp_name": row[5],
                "zid": row[6]
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
                    filtered_result = self.get_filtered_result_data(result)
                    result_with_rider_data = self.add_registered_data_to_result(filtered_result)
                    self.stage_results[cat].append(result_with_rider_data)

    def get_filtered_result_data(self, result):
        filtered_result = {
            "zp_name": result["name"],
            "zid": result["DT_RowId"],
            "category": self.get_cat_from_label(result["label"]),
            "race_time": result["race_time"],
            "time_diff": result["time_diff"]
        }
        return filtered_result

    def add_registered_data_to_result(self, result):
        # add rider info to result info
        cat = result["category"]
        for rider in self.riders[cat]:
            if rider["zid"] == result["zid"]:
                result["registered_name"] = rider["name"]
                result["team"] = rider["team"],
                result["subteam"] = rider["subteam"]
            return result

    def get_cat_from_label(self, label):
        if label == "1":
            return "a"
        if label == "2":
            return "b"
        if label == "3":
            return "c"
        if label == "4":
            return "d"
        return ""

    def get_registered_zids(self, riders):
        # returns a list of registered zids
        zids = []
        for rider in riders:
            zids.append(rider["zid"])
        return zids


    def validate_result(self, result, cat):
        # checks if this result is from a registered rider in the correct category
        # if dq_cat is not empty, rider has been DQ'd
        if result["dq_cat"] != "":
            return False
        registered_zids = self.registered_zids[cat]
        if result["DT_RowId"] in registered_zids:
            return True
        return False

    def get_veganuary_stage_results(self, category):
        # attempt to create a csv from results
        data = self.stage_results[category]
        print (data)
        # keys = data[0].keys()
        #
        # with open('veganuary_stage_results.csv', 'w', newline='')  as output_file:
        #     dict_writer = csv.DictWriter(output_file, keys)
        #     dict_writer.writeheader()
        #     dict_writer.writerows(data)
