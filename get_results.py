from veganuary import CalculateResults
from zp_data.stage_2_results import STAGE_2_RESULTS
from zp_data.stage_2_prime_a import STAGE_2_PRIME_DATA_A
from zp_data.stage_2_prime_b import STAGE_2_PRIME_DATA_B
from zp_data.stage_2_prime_c import STAGE_2_PRIME_DATA_C
from zp_data.stage_2_prime_d import STAGE_2_PRIME_DATA_D
import pdb

# The current data doesn't include filtered data, nor doesit include sprint/KOM data
c = CalculateResults(STAGE_2_RESULTS)

c.get_veganuary_stage_results("a")
print("resolving stage results for cat A")
c.get_veganuary_stage_results("b")
print("resolving stage results for cat B")
c.get_veganuary_stage_results("c")
print("resolving stage results for cat C")
c.get_veganuary_stage_results("d")
print("resolving stage results for cat D")

c.get_veganuary_prime_results(STAGE_2_PRIME_DATA_A, "a")
print("resolving prime results for cat A")
c.get_veganuary_prime_results(STAGE_2_PRIME_DATA_B, "b")
print("resolving prime results for cat B")
c.get_veganuary_prime_results(STAGE_2_PRIME_DATA_C, "c")
print("resolving prime results for cat C")
c.get_veganuary_prime_results(STAGE_2_PRIME_DATA_D, "d")
print("resolving prime results for cat D")
