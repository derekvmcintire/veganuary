from veganuary import CalculateResults
import stage_2_rider_data

c = CalculateResults(stage_2_rider_data.STAGE_2_RESULTS)
print("Number of A Riders:", len(c.riders["a"]))
print("Number of A Rider Rsults:", len(c.stage_results["a"]))
# validate riders to filter out results from those not participating in veganuary
valid_riders = c.get_valid_riders(c.stage_results["a"], c.riders["a"])
print("Number of valid riders for A cat:", len(valid_riders))
