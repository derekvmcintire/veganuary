import pdb
from models.stage_model import StageModel
from models.overall_standings_model import OverallStandingsModel
from models.riders_model import RidersCollection
from models.prime_results_model import PrimeResultsCollection
# import stage 1 data
from zp_data.stage_1.stage_1_results import STAGE_1_RESULTS
# import stage 2 data
from zp_data.stage_2.stage_2_results import STAGE_2_RESULTS
from zp_data.stage_2.sprint_kom_data import STAGE_2_SPRINT_KOM_DATA


# Run script for stage 1
stage_1 = StageModel(
STAGE_1_RESULTS,
""
)
stage_1.print_stage_results('a', 1)
print('Exporting Cat A results for stage 1')
stage_1.print_stage_results('b', 1)
print('Exporting Cat B results for stage 1')
stage_1.print_stage_results('c', 1)
print('Exporting Cat C results for stage 1')
stage_1.print_stage_results('d', 1)
print('Exporting Cat D results for stage 1')

# Run script for stage 2
stage_2 = StageModel(
STAGE_2_RESULTS,
STAGE_2_SPRINT_KOM_DATA
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
