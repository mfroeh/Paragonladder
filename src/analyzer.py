import json
from typing import List, Mapping
from dataclasses import dataclass
from account import Account
from constants import Region


@dataclass
class AccountInfo:
    battletag: str
    paragon_season: int = 0
    paragon_nonseason: int = 0
    playtime: float = 0.0
    playtime_distribution: Mapping[str, float] = None
    most_played_class: str = None
    xp_gained: int = 0
    last_update: int = 0


class Analyzer:
    def __init__(self, season: int, region: Region):
        self.season = season
        self.region = region

    def analyze_accounts(self, accounts: List[Account]) -> List[AccountInfo]:
        return [self.analyze_account(account) for account in accounts]

    def analyze_account(self, account: Account) -> AccountInfo:
        """
        Analyzes a given account.
        """
        playtime_distrubution = next(
            x for x in account.seasonalProfiles.values() if x.seasonId == self.season
        ).timePlayed

        playtime = sum(playtime_distrubution.values())
        most_played = max(playtime_distrubution, key=playtime_distrubution.get)
        total_xp_gained = xp_from_paragon_level(account.paragonLevelSeason)

        return AccountInfo(
            battletag=account.battleTag,
            paragon_season=account.paragonLevelSeason,
            paragon_nonseason=account.paragonLevel,
            last_update=account.lastUpdated,
            playtime=playtime,
            playtime_distribution=playtime_distrubution,
            most_played_class=most_played,
            xp_gained=total_xp_gained,
        )


# Taken from https://github.com/dclamage/dclamage.github.io/blob/master/paragon1.4.js
paragons = json.load(open("../paragontotals.json", "r"))

c1 = 166105421028000
c2 = 201211626000
c3 = 229704000
c4 = 102000
half = 0.5
six = 6


def xp_from_paragon_level(level: int) -> int:
    if level <= 0:
        return paragons[0]
    elif level < 2252:
        return paragons[level]
    else:
        x = level - 2252
        xp1 = level - 2251
        xp2 = level - 2250

        return int(c1 + c2 * x + c3 * x * xp1 * 0.5 + x * xp1 * xp2 / six * c4)
