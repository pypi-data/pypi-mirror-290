
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
from enum import Enum

class Module(Enum):
    CORE="core"
    ORACLE="oracle"
    PORTFOLIO="portfolio"
    RISK="risk"
    RESEARCH="research"
    TRADING="trading"
    SIMULATION="simulation"

    def __str__(self):
        return self.value

class Sector(Enum):
    FINCORE="fincore"
    GYMCORE="gymcore"
    HEALTHCORE="healthcore"
    ENVICORE="envicore"
    SPORTSCORE="sportscore"
    POLICORE="policore"
    CUSTOM="custom"

    def __str__(self):
        return self.value