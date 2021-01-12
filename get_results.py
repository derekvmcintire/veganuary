import pdb
from stage_results_model import StageResultsModel
# import stage 1 data
from zp_data.stage_1.stage_1_results import STAGE_1_RESULTS
from zp_data.stage_1.stage_1_prime_a import STAGE_1_PRIME_DATA_A
from zp_data.stage_1.stage_1_prime_b import STAGE_1_PRIME_DATA_B
from zp_data.stage_1.stage_1_prime_c import STAGE_1_PRIME_DATA_C
from zp_data.stage_1.stage_1_prime_d import STAGE_1_PRIME_DATA_D
# import stage 2 data
from zp_data.stage_2.stage_2_results import STAGE_2_RESULTS
from zp_data.stage_2.stage_2_prime_a import STAGE_2_PRIME_DATA_A
from zp_data.stage_2.stage_2_prime_b import STAGE_2_PRIME_DATA_B
from zp_data.stage_2.stage_2_prime_c import STAGE_2_PRIME_DATA_C
from zp_data.stage_2.stage_2_prime_d import STAGE_2_PRIME_DATA_D

# Run script for stage 1
stage_1_model = StageResultsModel(STAGE_1_RESULTS)
# stage results by cat
stage_1_model.get_veganuary_stage_results("a", 1)
print("resolving stage results for cat A")
stage_1_model.get_veganuary_stage_results("b", 1)
print("resolving stage results for cat B")
stage_1_model.get_veganuary_stage_results("c", 1)
print("resolving stage results for cat C")
stage_1_model.get_veganuary_stage_results("d", 1)
print("resolving stage results for cat D")
# prime results by cat
stage_1_model.get_veganuary_prime_results(STAGE_1_PRIME_DATA_A, "a", 1)
print("resolving prime results for cat A")
stage_1_model.get_veganuary_prime_results(STAGE_1_PRIME_DATA_B, "b", 1)
print("resolving prime results for cat B")
stage_1_model.get_veganuary_prime_results(STAGE_1_PRIME_DATA_C, "c", 1)
print("resolving prime results for cat C")
stage_1_model.get_veganuary_prime_results(STAGE_1_PRIME_DATA_D, "d", 1)
print("resolving prime results for cat D")

# Run script for stage 2
stage_2_model = StageResultsModel(STAGE_2_RESULTS)
# stage results by cat
stage_2_model.get_veganuary_stage_results("a", 2)
print("resolving stage results for cat A")
stage_2_model.get_veganuary_stage_results("b", 2)
print("resolving stage results for cat B")
stage_2_model.get_veganuary_stage_results("c", 2)
print("resolving stage results for cat C")
stage_2_model.get_veganuary_stage_results("d", 2)
print("resolving stage results for cat D")
# prime results by cat
stage_2_model.get_veganuary_prime_results(STAGE_2_PRIME_DATA_A, "a", 2)
print("resolving prime results for cat A")
stage_2_model.get_veganuary_prime_results(STAGE_2_PRIME_DATA_B, "b", 2)
print("resolving prime results for cat B")
stage_2_model.get_veganuary_prime_results(STAGE_2_PRIME_DATA_C, "c", 2)
print("resolving prime results for cat C")
stage_2_model.get_veganuary_prime_results(STAGE_2_PRIME_DATA_D, "d", 2)
print("resolving prime results for cat D")
