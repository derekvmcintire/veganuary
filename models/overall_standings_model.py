import csv
import json
import copy
import datetime
from decimal import *

from models.riders_model import RidersCollection

from data_shapes import (
    CATEGORY_SHAPE,
    CATEGORIES
)

# This sets the precision of the Decimal module to 9 places
getcontext().prec = 9

class OverallStandingsModel:
    def __init__(self, last_stage: int):
        self.last_stage = last_stage
        self.stage_keys = list(range(1, (self.last_stage + 1)))
        self.ranked_gc = copy.deepcopy(CATEGORY_SHAPE)
        # instantiate a new RidersCollection and load rider data
        self.riders_collection = RidersCollection()
        self.stages_results = {}
        self.load_stages_results()
        try:
            self.gc_results = copy.deepcopy(self.stages_results['1'])
            self.calculate_gc_times()
            self.rank_gc()
            print('Success calculating GC standings, but still need to write functions to print!')
        except:
            print('Error while trying to calculate GC standings')

    def load_stages_results(self):
        # Loads the results data
        for i in range(len(self.stage_keys)):
            stage = i + 1
            file_a = open(f'./results/stage_{stage}/stage_{stage}_results_a.csv', 'r')
            file_b = open(f'./results/stage_{stage}/stage_{stage}_results_b.csv', 'r')
            file_c = open(f'./results/stage_{stage}/stage_{stage}_results_c.csv', 'r')
            file_d = open(f'./results/stage_{stage}/stage_{stage}_results_d.csv', 'r')
            reader_a = csv.reader(file_a)
            reader_b = csv.reader(file_b)
            reader_c = csv.reader(file_c)
            reader_d = csv.reader(file_d)
            next(reader_a)
            next(reader_b)
            next(reader_c)
            next(reader_d)
            stage_results = {}
            stage_results["a"] = self.build_results(reader_a)
            stage_results["b"] = self.build_results(reader_b)
            stage_results["c"] = self.build_results(reader_c)
            stage_results["d"] = self.build_results(reader_d)
            self.stages_results[str(stage)] = stage_results

    def build_results(self, csv):
        results = []
        for row in csv:
            result = {
                "registered_name": row[0],
                "category": row[1],
                "gender": row[2],
                "display_time": row[3],
                "race_time": row[4],
                "time_diff": row[5],
                "zwid": row[6],
                "zp_name": row[7],
                "team": row[8],
                "subteam": row[9]
            }
            results.append(result)
        return results

    def calculate_gc_times(self):
        for stage in self.stage_keys[1:]:
            for cat in self.stages_results[str(stage)]:
                cat_calculated_results = []
                for result in self.stages_results[str(stage)][cat]:
                    calculated_result = {}
                    current_gc_time = Decimal(self.get_rider_gc_time(result))
                    updated_gc_time = Decimal(result["race_time"]) + current_gc_time
                    updated_display_time = str(datetime.timedelta(seconds=float(updated_gc_time)))
                    calculated_result["race_time"] = updated_gc_time
                    calculated_result["display_time"] = updated_display_time
                    calculated_result["registered_name"] = result["registered_name"]
                    calculated_result["zwid"] = result["zwid"]
                    calculated_result["team"] = result["team"]
                    if current_gc_time > 0:
                        cat_calculated_results.append(calculated_result)
                self.gc_results[cat] = cat_calculated_results

    def get_rider_gc_time(self, rider_result):
        for result in self.gc_results[rider_result['category']]:
            if result["zwid"] == rider_result['zwid']:
                return result["race_time"]
        return 0

    def rank_gc(self):
        for cat in CATEGORIES:
            for result in self.gc_results[cat]:
                if len(self.ranked_gc[cat]) > 0:
                    for i in range(len(self.ranked_gc[cat])):
                        if result["race_time"] < self.ranked_gc[cat][i]["race_time"]:
                            self.ranked_gc[cat].insert(i, result)
                            break
                        if (i + 1) == len(self.ranked_gc[cat]):
                            # if we are on the last entry, then add the result to the end
                            self.ranked_gc[cat].append(result)
                            break
                else:
                    self.ranked_gc[cat].append(result)
