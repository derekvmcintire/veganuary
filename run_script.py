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

# ==========================================================#
# ================ Run script for stage 1 ==================#
# ==========================================================#
# easy on/off toggle for testing
if get_stage_1_results:
    # create new model
    stage_1 = StageModel(
    STAGE_1_EVENT_ID,
    stage_1_sprints,
    stage_1_koms,
    SINGLE_POINTS,
    DOUBLE_POINTS,
    True,
    DOUBLE_POINTS
    )
    # print results to csv
    stage_1.print_all_results(1)

# ==========================================================#
# ================ Run script for stage 2 ==================#
# ==========================================================#
# easy on/off toggle for testing
if get_stage_2_results:
    # create new model
    stage_2 = StageModel(
    STAGE_2_EVENT_ID,
    stage_2_sprints,
    stage_2_koms,
    SINGLE_POINTS,
    DOUBLE_POINTS,
    True,
    DOUBLE_POINTS
    )
    stage_2.print_all_results(2)
