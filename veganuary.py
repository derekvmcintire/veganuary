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
        self.get_registered_zids(self.riders["a"])
        self.get_registered_zids(self.riders["b"])
        self.get_registered_zids(self.riders["c"])
        self.get_registered_zids(self.riders["d"])
        self.load_results() #load stage results from JSON data

    def load_rider_list(self):
        # Loads the list of riders from the csv file in this directory
        rider_list_file = open('./riders.csv', 'r')
        rider_list = csv.reader(rider_list_file)
        for row in rider_list:
            rider = {
                "id": row[0],
                "name": row[1],
                "team": row[2],
                "category": row[4],
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
                if result["category"] == "A":
                    if self.validate_result(result):
                        self.stage_results["a"].append(result)
                elif result["category"] == "B":
                    if self.validate_result(result):
                        self.stage_results["b"].append(result)
                elif result["category"] == "C":
                    if self.validate_result(result):
                        self.stage_results["c"].append(result)
                elif result["category"] == "D":
                    if self.validate_result(result):
                        self.stage_results["d"].append(result)

    def get_registered_zids(self, riders):
        # returns a list of registered zids
        zids = []
        for rider in riders:
            zids.append(rider["zid"])
        return zids


    def validate_result(self, result):
        # checks if this result is from a registered rider in the correct category
        if result["zid"] in self.registered_zids[result["category"]]:
            return True
        return False

    def get_veganuary_results(self, category):
        # attempt to create a csv from results
        keys = stage_results[category].keys()
        with open('veganuary_stage_results.csv', 'w', newline='')  as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(toCSV)
