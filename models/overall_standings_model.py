import csv
import json
import copy
import datetime
from decimal import *

from models.riders_model import RidersCollection

from data_shapes import (
    CATEGORY_SHAPE,
    CATEGORIES,
    KOM_TYPE,
    SPRINT_TYPE,
    PRIME_IDS
)

# This sets the precision of the Decimal module to 9 places
getcontext().prec = 9

class OverallStandingsModel:
    def __init__(self, last_stage: int):
        self.last_stage = last_stage
        self.stage_keys = list(range(1, (self.last_stage + 1)))
        self.sprint_keys = []
        self.kom_keys = []
        self.sprint_data = {}
        self.kom_data = {}
        self.ranked_gc = copy.deepcopy(CATEGORY_SHAPE)
        self.ranked_wgc = copy.deepcopy(CATEGORY_SHAPE)
        self.gc_calculated_successful = False
        # instantiate a new RidersCollection and load rider data
        self.riders_collection = RidersCollection()
        self.stages_results = {}
        self.load_stages_results()
        try:
            # try loading existing results and then calculate and rank gc times
            self.gc_results = copy.deepcopy(self.stages_results['1'])
            self.rank_gc()
            self.gc_calculated_successful = True
        except:
            print('Error while trying to calculate GC standings')
        try:
            # try to load existing prime results
            self.load_prime_gc_results('m', SPRINT_TYPE)
            self.load_prime_gc_results('m', KOM_TYPE)
            # need to write functions for caluclating and ranking sprint/kom points
        except:
            print('Error while trying to calculate sprint and K/QOM GC standings')

    def load_prime_gc_results(self, gender, type):
        # Loads existing results data for primes
        prime_gc_results = {}
        for i in range(len(self.stage_keys)):
            stage = i + 1
            for prime in PRIME_IDS[str(stage)][type]:
                prime_gc_results[str(stage)] = {}
                prime_gc_results[str(stage)][prime] = copy.deepcopy(CATEGORY_SHAPE)
                for cat in CATEGORIES:
                    file = open(f'./results/stage_{stage}/{gender}_prime_results_{cat}_{prime}.csv', 'r')
                    reader = csv.reader(file)
                    next(reader)
                    prime_gc_results[str(stage)][prime][cat] = self.build_prime_results(reader)
        if type == KOM_TYPE:
            self.kom_data = prime_gc_results
        if type == SPRINT_TYPE:
            self.sprint_data = prime_gc_results

    def load_stages_results(self):
        # Loads existing results data
        for i in range(len(self.stage_keys)):
            stage = i + 1
            stage_results = {}
            for cat in CATEGORIES:
                file = open(f'./results/stage_{stage}/stage_{stage}_results_{cat}.csv', 'r')
                reader = csv.reader(file)
                next(reader)
                stage_results[cat] = self.build_results(reader)
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

    def build_prime_results(self, csv):
        results = []
        for row in csv:
            result = {
                "registered_name": row[0],
                "gender": row[1],
                "time": row[2],
                "zwid": row[3],
                "team": row[4],
                "zp_name": row[5],
                "points": row[6]
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
                    calculated_result["display_race_time"] = updated_display_time
                    calculated_result["registered_name"] = result["registered_name"]
                    calculated_result["zwid"] = result["zwid"]
                    calculated_result["team"] = result["team"]
                    calculated_result["category"] = result["category"]
                    calculated_result["gender"] = result["gender"]
                    calculated_result["zp_name"] = result["zp_name"]
                    calculated_result["subteam"] = result["subteam"]
                    if current_gc_time > 0:
                        cat_calculated_results.append(calculated_result)
                self.gc_results[cat] = cat_calculated_results

    def get_rider_gc_time(self, rider_result):
        for result in self.gc_results[rider_result['category']]:
            if result["zwid"] == rider_result['zwid']:
                return result["race_time"]
        return 0

    def rank_gc(self):
        # calculate gc times for all riders before we rank them in order
        self.calculate_gc_times()
        for cat in CATEGORIES:
            for result in self.gc_results[cat]:
                if len(self.ranked_gc[cat]) > 0:
                    for i in range(len(self.ranked_gc[cat])):
                        if result["race_time"] < self.ranked_gc[cat][i]["race_time"]:
                            self.ranked_gc[cat].insert(i, result)
                            if result["gender"] == '2':
                                self.ranked_wgc[cat].insert(i, result)
                            break
                        if (i + 1) == len(self.ranked_gc[cat]):
                            # if we are on the last entry, then add the result to the end
                            self.ranked_gc[cat].append(result)
                            if result["gender"] == '2':
                                self.ranked_wgc[cat].append(result)
                            break
                else:
                    self.ranked_gc[cat].append(result)
                    if result["gender"] == '2':
                        self.ranked_wgc[cat].append(result)
        
    def print_all_gc_results(self):
        if self.gc_calculated_successful:
            print('===== Success calculating GC standings, printing all categories now! =====')
            for cat in CATEGORIES:
                self.print_gc_results(cat, self.ranked_gc[cat], 'a')
                self.print_gc_results(cat, self.ranked_wgc[cat], 'w')

    def print_gc_results(self, category, data, gender):
        # attempt to create a csv from results
        with open(f'./results/gc/cat_{category}_{gender}_results.csv', 'w', newline='')  as output_file:
            dict_writer = csv.DictWriter(output_file, ["registered_name", "category", "gender", "display_race_time", "race_time", "zwid", "zp_name", "team", "subteam"])
            dict_writer.writeheader()
            dict_writer.writerows(data)
