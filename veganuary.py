import csv
import json


class CalculateResults:
    rider_data = []
    stage_results = []
    a_riders = []
    b_riders = []
    c_riders = []
    d_riders = []
    a_results = []
    b_results = []
    c_results = []
    d_results = []

    def __init__(self, rider_data=[]):
        self.rider_data = rider_data
        self.load_rider_list()
        self.load_results()

    def load_rider_list(self):
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
                self.a_riders.append(rider)
            elif rider["category"] == "B":
                self.b_riders.append(rider)
            elif rider["category"] == "C":
                self.c_riders.append(rider)
            elif rider["category"] == "D":
                self.d_riders.append(rider)

    def load_stage_results(self):
        self.stage_results = json.loads(self.rider_data)["data"]

    def load_results(self):
        if not self.stage_results:
            self.load_stage_results()
        for result in self.stage_results:
            if result["category"] == "A":
                self.a_results.append(result)
            elif result["category"] == "B":
                self.b_results.append(result)
            elif result["category"] == "C":
                self.c_results.append(result)
            elif result["category"] == "D":
                self.d_results.append(result)

    def get_valid_riders(self, results, riders):
        rider_names = []
        validated_riders = []
        for rider in riders:
            rider_names.append(rider["name"])
        for result in results:
            if result["name"] in rider_names:
                validated_riders.append(result)
        return validated_riders
