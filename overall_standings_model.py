import csv
import json
from decimal import Decimal

from data_shapes import (

)


class OverallStandingsModel:
    stages_data = []
    stage_results = []

    def __init__(self, last_stage):
        self.last_stage = last_stage
        
