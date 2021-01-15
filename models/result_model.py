import csv
import copy
import datetime
import json
from dataclasses import dataclass, asdict
from decimal import Decimal

from data_shapes import (
    WINNING_TIMES_SHAPE,
    CATEGORY_SHAPE
)


@dataclass
class ResultModel:
    zp_name: str = ""
    zwid: int = 0
    category: str = ""
    display_race_time: str = ""
    race_time: float = 0
    time_diff: float = 0
    registered_name: str = ""
    team: str = ""
    subteam: str = ""
    gender: str = ""

class ResultsCollection:
    def __init__(self, input_data, registered_zwids, riders):
        self.input_data = input_data
        self.registered_zwids = registered_zwids
        self.riders = riders
        self.winning_times = copy.deepcopy(WINNING_TIMES_SHAPE)
        self.results = copy.deepcopy(CATEGORY_SHAPE)
        self.load_results()

    def load_results(self):
        for result in self.input_data:
            cat = self.get_cat_from_label(result["label"])
            if self.validate_result(result, cat, self.registered_zwids[cat]):
                # store winning times so we can calculate time difference
                if len(self.results[cat]) == 0:
                    self.winning_times[cat] = Decimal(result["race_time"][0])
                filtered_result = self.get_filtered_result_data(result, cat)
                res = self.add_rider_data_to_result(filtered_result, self.riders)
                self.results[cat].append(res)


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

    def validate_result(self, result, cat, registered_zwids):
        # checks if this result is from a registered rider in the correct category
        # if dq_cat is not empty, rider has been DQ'd
        if result["dq_cat"] != "":
            return False
        if int(result["zwid"]) in self.registered_zwids[cat]:
            return True
        return False

    def filter_emojis(self, text):
        # need to filter out emojis from ZP names
        result = text.encode('unicode-escape').decode('ascii')
        return result

    def calculate_time_diff(self, winning_time: Decimal, race_time: Decimal):
        # because the time diff should be calculated off the first registered rider
        # and not the overall first finisher, we need to re-calculate
        if winning_time > 0:
            # convert to float for display
            diff = float(race_time - winning_time)
            return str(datetime.timedelta(seconds=diff))
        return 0

    def get_filtered_result_data(self, result, cat):
        # filters out extra data and sets time data
        # store race time as decimal for calculations but convert to datetime
        # object for display purposes
        race_time = Decimal(result["race_time"][0])
        display_race_time = str(datetime.timedelta(seconds=result["race_time"][0]))
        time_diff = self.calculate_time_diff(self.winning_times[cat], race_time)
        filtered_result = ResultModel()
        filtered_result.zp_name = self.filter_emojis(result["name"])
        filtered_result.zwid = int(result["zwid"])
        filtered_result.category = cat
        filtered_result.display_race_time = display_race_time
        filtered_result.race_time = race_time
        filtered_result.time_diff = time_diff
        return filtered_result

    def add_rider_data_to_result(self, result, riders):
        # add rider info to result info
        cat = result.category
        # new_result = dict(result)
        for rider in riders[cat]:
            if rider.zwid == result.zwid:
                result.registered_name = rider.name
                result.team = rider.team
                result.subteam = rider.subteam
                result.gender = rider.gender
                return asdict(result)
