import pdb
from models.overall_standings_model import OverallStandingsModel
from models.stage_model import StageModel
from zp_request_library import ZPRequests
from data_shapes import (SINGLE_POINTS, DOUBLE_POINTS, PRIME_IDS, SPRINT_TYPE, KOM_TYPE)

STAGE_1_EVENT_ID = 1429958
STAGE_2_EVENT_ID = 1471415
STAGE_3_EVENT_ID = 1514103
STAGE_4_EVENT_ID = 1563324
stage_1_sprints = PRIME_IDS['1'][SPRINT_TYPE]
stage_1_koms = PRIME_IDS['1'][KOM_TYPE]
stage_2_sprints = PRIME_IDS['2'][SPRINT_TYPE]
stage_2_koms = PRIME_IDS['2'][KOM_TYPE]
stage_3_sprints = PRIME_IDS['3'][SPRINT_TYPE]
stage_3_koms = PRIME_IDS['3'][KOM_TYPE]
stage_4_sprints = PRIME_IDS['4'][SPRINT_TYPE]
stage_4_koms = PRIME_IDS['4'][KOM_TYPE]

# toggles
get_stage_1_results = False
get_stage_2_results = False
get_stage_3_results = False
get_stage_4_results = True
get_gc_results = True

# number of stages to use for gc
number_of_stages = 4


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


# ==========================================================#
# ================ Run script for stage 3 ==================#
# ==========================================================#
# easy on/off toggle for testing
if get_stage_3_results:
    # create new model
    stage_3 = StageModel(
        STAGE_3_EVENT_ID,
        stage_3_sprints,
        stage_3_koms,
        SINGLE_POINTS,
        DOUBLE_POINTS,
    )
    # print results to csv
    stage_3.print_all_results(3)


# ==========================================================#
# ================ Run script for stage 4 ==================#
# ==========================================================#
# easy on/off toggle for testing
if get_stage_4_results:
    # create new model
    stage_4 = StageModel(
        STAGE_4_EVENT_ID,
        stage_4_sprints,
        stage_4_koms,
        DOUBLE_POINTS,
        DOUBLE_POINTS,
        True,
        DOUBLE_POINTS
    )
    # print results to csv
    stage_1.print_all_results(1)


# ==========================================================#
# ======== Run script for general classification ===========#
# ==========================================================#
# easy on/off toggle for testing
if get_gc_results:
    gc_results = OverallStandingsModel(number_of_stages)
    gc_results.print_all_gc_results()
