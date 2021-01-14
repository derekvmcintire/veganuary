import csv
import json
from decimal import Decimal


class OverallStandingsModel:
    stages_results = []
    valid_zwids = []

    def __init__(self, last_stage: int, valid_zwids):
        self.last_stage = last_stage
        self.valid_zwids = valid_zwids
        self.registered_zwids = copy.deepcopy(REGISTERED_ZWIDS_SHAPE)

    def load_stages_results(self):
        # Loads the results data
        for i in range(self.last_stage):
            if i > 0:
                file_a = open(f'./results/stage_{i}/stage_{i}_results_a.csv', 'r')
                file_b = open(f'./results/stage_{i}/stage_{i}_results_b.csv', 'r')
                file_c = open(f'./results/stage_{i}/stage_{i}_results_c.csv', 'r')
                file_d = open(f'./results/stage_{i}/stage_{i}_results_d.csv', 'r')
                reader_a = csv.reader(file_a)
                reader_b = csv.reader(file_b)
                reader_c = csv.reader(file_c)
                reader_d = csv.reader(file_d)
                next(reader_a)
                next(reader_b)
                next(reader_c)
                next(reader_d)
                stage_results = {"stage": str(i)}
                stage_results["a"] = self.build_results(reader_a)
                stage_results["b"] = self.build_results(reader_b)
                stage_results["c"] = self.build_results(reader_c)
                stage_results["d"] = self.build_results(reader_d)
                self.stages_results.append(stage_results)

    def build_results(self, csv):
        results = []
        for row in csv:
            result = {
                "registered_name": row[0],
                "category": row[1],
                "gender": row[2],
                "race_time": row[3],
                "time_diff": row[4],
                "zid": row[5],
                "zp_name": row[6],
                "team,subteam": row[7]
            }
            results.append(result)
        return results

    def get_gc_times(self, category):
        gc_results = []
        for r in self.stages_results[0][category]:
            gc_times = [r["race_time"]]
            rider_gc_time = 0
            for i in range(self.last_stage - 1):
                for z in self.stages_results[i][category]:
                    if r["zid"] == z["zid"]:
                        gc_times.append(Decimal(float(z["race_time"])))
                if len(gc_times) == self.last_stage:
                    rider_gc_time = sum(gc_times)
            if rider_gc_time > 0:
                r["gc_time"] = rider_gc_time
                gc_results.append(r)
        return gc_results

    def get_gc_results(self, category):
        data = self.get_gc_times(category)
        breakpoint()
        # keys = data[0].keys()
        # with open(f'./results/overall/gc/{category}.csv', 'w', newline='')  as output_file:
        #     dict_writer = csv.DictWriter(output_file, keys)
        #     dict_writer.writeheader()
        #     dict_writer.writerows(data)
