import csv
import copy
from dataclasses import dataclass

from data_shapes import (
    RIDERS_SHAPE,
)


@dataclass
class RiderModel:
    id: int = 0
    name: str = ""
    team: str = ""
    category: str = ""
    subteam: str = ""
    zp_name: str = ""
    zwid: int = 0
    gender: int = 0


class RidersCollection:
    def __init__(self):
        self.registered_riders = copy.deepcopy(RIDERS_SHAPE)

    def load_rider_list(self):
        # Loads the list of riders from the csv file in this directory
        rider_list_file = open('./veganuary_data/rider_list_with_gender.csv', 'r')
        rider_list = csv.reader(rider_list_file)
        for row in rider_list:
            rider = RiderModel()
            rider.id = row[0]
            rider.name = row[1]
            rider.team = row[2]
            rider.subteam = row[3]
            rider.category = row[4]
            rider.zp_name = row[5]
            rider.zwid = row[6]
            rider.gender = row[7]
            if rider.category == "A":
                self.registered_riders["a"].append(rider)
            elif rider.category == "B":
                self.registered_riders["b"].append(rider)
            elif rider.category == "C":
                self.registered_riders["c"].append(rider)
            elif rider.category == "D":
                self.registered_riders["d"].append(rider)



# create rider data class
# create riders model
# populate riders model with rider data
