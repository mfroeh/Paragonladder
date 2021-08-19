from enum import Enum
from dataclasses import dataclass
from typing import Optional, List


class HeroClassString(Enum):
    barbarian = "barbarian"
    crusader = "crusader"
    dh = "dh"
    monk = "monk"
    necromancer = "necromancer"
    wd = "wd"
    wizard = "wizard"


@dataclass
class Ladder:
    href: Optional[str] = None


@dataclass
class Leaderboard:
    ladder: Optional[Ladder] = None
    teamsize: Optional[int] = None
    hardcore: Optional[bool] = None
    heroclassstring: Optional[HeroClassString] = None


@dataclass
class Links:
    linksself: Optional[Ladder] = None


@dataclass
class LeaderboardInfo:
    links: Optional[Links] = None
    leaderboard: Optional[List[Leaderboard]] = None
    seasonid: Optional[int] = None
    lastupdatetime: Optional[str] = None
    generatedby: Optional[str] = None
