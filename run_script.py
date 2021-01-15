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

get_stage_1_results = True
get_stage_2_results = True

def print_stage_results(stage_model, stage_number):
    stage_model.print_stage_results('a', stage_number)
    print(f'Exporting Cat A results for stage {stage_number}')
    stage_model.print_stage_results('b', stage_number)
    print(f'Exporting Cat B results for stage {stage_number}')
    stage_model.print_stage_results('c', stage_number)
    print(f'Exporting Cat C results for stage {stage_number}')
    stage_model.print_stage_results('d', stage_number)
    print(f'Exporting Cat D results for stage {stage_number}')
    stage_model.print_prime_results('a', stage_number)
    print(f'Exporting Cat A sprint and KOM results for stage {stage_number}')
    stage_model.print_prime_results('b', stage_number)
    print(f'Exporting Cat B sprint and KOM results for stage {stage_number}')
    stage_model.print_prime_results('c', stage_number)
    print(f'Exporting Cat C sprint and KOM results for stage {stage_number}')
    stage_model.print_prime_results('d', stage_number)
    print(f'Exporting Cat D sprint and KOM results for stage {stage_number}')
    print('Done!')

# ==========================================================#
# ================ Run script for stage 1 ==================#
# ==========================================================#
if get_stage_1_results:
    stage_1 = StageModel(
    STAGE_1_EVENT_ID,
    stage_1_sprints,
    stage_1_koms,
    SINGLE_POINTS,
    DOUBLE_POINTS,
    True,
    DOUBLE_POINTS
    )
    print_stage_results(stage_1, 1)

# ==========================================================#
# ================ Run script for stage 2 ==================#
# ==========================================================#
if get_stage_2_results:
    stage_2 = StageModel(
    STAGE_2_EVENT_ID,
    stage_2_sprints,
    stage_2_koms,
    SINGLE_POINTS,
    DOUBLE_POINTS,
    True,
    DOUBLE_POINTS
    )
    print_stage_results(stage_2, 2)
