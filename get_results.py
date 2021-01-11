from veganuary import CalculateResults
import stage_2_rider_data

# The current data doesn't include filtered data, nor doesit include sprint/KOM data
c = CalculateResults(stage_2_rider_data.STAGE_2_RESULTS)
print("Number of A Riders:", len(c.riders["a"]))
print("Number of valid A Rider Rsults:", len(c.stage_results["a"]))
print("Number of B Riders:", len(c.riders["b"]))
print("Number of valid B Rider Rsults:", len(c.stage_results["b"]))
print("Number of C Riders:", len(c.riders["c"]))
print("Number of valid C Rider Rsults:", len(c.stage_results["c"]))
print("Number of D Riders:", len(c.riders["d"]))
print("Number of valid D Rider Rsults:", len(c.stage_results["d"]))
c.get_veganuary_stage_results("a")
# c.get_veganuary_stage_results("b")
# c.get_veganuary_stage_results("c")
# c.get_veganuary_stage_results("d")
