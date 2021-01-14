import pdb
from models.stage_model import StageModel
from zp_request_library import ZPRequests
from data_shapes import (SINGLE_POINTS, DOUBLE_POINTS)

STAGE_1_EVENT_ID = 1429958
STAGE_2_EVENT_ID = 1471415
stage_2_sprints = ['59', '61', '62']
stage_2_koms = ['54']
stage_1_sprints = []
stage_1_koms = ['48']

# ==========================================================#
# ================ Run script for stage 1 ==================#
# ==========================================================#
print('Fetching data for stage 1...')
stage_1 = StageModel(
STAGE_1_EVENT_ID,
stage_1_sprints,
stage_1_koms
)
stage_1.print_stage_results('a', 1)
print('Exporting Cat A results for stage 1')
stage_1.print_stage_results('b', 1)
print('Exporting Cat B results for stage 1')
stage_1.print_stage_results('c', 1)
print('Exporting Cat C results for stage 1')
stage_1.print_stage_results('d', 1)
print('Exporting Cat D results for stage 1')
stage_1.print_prime_results('a', 1)
print('Exporting Cat A sprint and KOM results for stage 1')
stage_1.print_prime_results('b', 1)
print('Exporting Cat B sprint and KOM results for stage 1')
stage_1.print_prime_results('c', 1)
print('Exporting Cat C sprint and KOM results for stage 1')
stage_1.print_prime_results('d', 1)
print('Exporting Cat D sprint and KOM results for stage 1')
print('Done!')

# ==========================================================#
# ================ Run script for stage 2 ==================#
# ==========================================================#
print('Fetching data for stage 2...')
stage_2 = StageModel(
STAGE_2_EVENT_ID,
stage_2_sprints,
stage_2_koms
)
stage_2.print_stage_results('a', 2)
print('Exporting Cat A results for stage 2')
stage_2.print_stage_results('b', 2)
print('Exporting Cat B results for stage 2')
stage_2.print_stage_results('c', 2)
print('Exporting Cat C results for stage 2')
stage_2.print_stage_results('d', 2)
print('Exporting Cat D results for stage 2')
stage_2.print_prime_results('a', 2)
print('Exporting Cat A sprint and KOM results for stage 2')
stage_2.print_prime_results('b', 2)
print('Exporting Cat B sprint and KOM results for stage 2')
stage_2.print_prime_results('c', 2)
print('Exporting Cat C sprint and KOM results for stage 2')
stage_2.print_prime_results('d', 2)
print('Exporting Cat D sprint and KOM results for stage 2')
print('Done!')
