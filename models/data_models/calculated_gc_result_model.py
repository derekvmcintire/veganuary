from dataclasses import dataclass
from decimal import *

class CalculatedGCResult:
    race_time: Decimal = 0
    display_race_time: str = ""
    registered_name: str = ""
    zwid: int = 0
    team: str = ""
    category: str = ""
    gender: int = 0
    zp_name: str = ""
    subteam: str = ""
