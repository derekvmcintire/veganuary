import csv
import json


class CalculateResults:
    results_input_data = []
    riders = {
        "a": [],
        "b": [],
        "c": [],
        "d": []
    }
    stage_results = {
        "a": [],
        "b": [],
        "c": [],
        "d": []
    }
    overall_results = {
        "a": {
            "individual_gc": [],
            "womens_gc": [],
            "womens_sprint": [],
            "qom": [],
            "team_gc": [],
            "sprint": [],
            "kom": []
        },
        "b": {
            "individual_gc": [],
            "womens_gc": [],
            "womens_sprint": [],
            "qom": [],
            "team_gc": [],
            "sprint": [],
            "kom": []
        },
        "c": {
            "individual_gc": [],
            "womens_gc": [],
            "womens_sprint": [],
            "qom": [],
            "team_gc": [],
            "sprint": [],
            "kom": []
        },
        "d": {
            "individual_gc": [],
            "womens_gc": [],
            "womens_sprint": [],
            "qom": [],
            "team_gc": [],
            "sprint": [],
            "kom": []
        },
    }

    def __init__(self, results_input_data=[]):
        self.results_input_data = results_input_data
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
                self.riders["a"].append(rider)
            elif rider["category"] == "B":
                self.riders["b"].append(rider)
            elif rider["category"] == "C":
                self.riders["c"].append(rider)
            elif rider["category"] == "D":
                self.riders["d"].append(rider)

    def add_results_input_data(self, results_input_data):
        self.results_input_data = results_input_data

    def load_results(self):
        if (self.results_input_data):
            all_results = json.loads(self.results_input_data)["data"]
            for result in all_results:
                if result["category"] == "A":
                    self.stage_results["a"].append(result)
                elif result["category"] == "B":
                    self.stage_results["b"].append(result)
                elif result["category"] == "C":
                    self.stage_results["c"].append(result)
                elif result["category"] == "D":
                    self.stage_results["d"].append(result)

    def get_valid_riders(self, results, riders):
        # Should use ZP number instead of name - ask Chris if there is a list
        rider_names = []
        validated_riders = []
        for rider in riders:
            rider_names.append(rider["name"])
        for result in results:
            if result["name"] in rider_names:
                validated_riders.append(result)
        return validated_riders
