from dataclasses import dataclass
from typing import List, Mapping
from diablo_api import DiabloApi, LeaderboardType, Region
from time import sleep


@dataclass
class AccountInfo:
    battletag: str
    paragon_season: int
    paragon_nonseason: int
    # playtime: float
    playtime_distribution: Mapping[str, float]
    last_update: int


class Extractor:
    def __init__(self, season: int, region: Region, api: DiabloApi):
        self.season = season
        self.api = api
        self.region = region

    def collect_battletags(self) -> List[str]:
        """
        Collects a list of battletags from the "rift-team-4" leaderboard by using the DiabloApi.
        """
        leaderboard = self.api.get_season_leaderboard(
            self.region, self.season, LeaderboardType.FOUR_PLAYER
        )

        battletags = []
        i = 0
        for row in leaderboard.row:
            for player in row.player:
                battletag = next(
                    d.string for d in player.data if d.id == "HeroBattleTag"
                )
                if battletag not in battletags:
                    battletags.append(battletag)
                    i += 1

        print(f"Found {i} unique battletags")

        return battletags

    def collect_account_infos(self, battletags: List[str]) -> List[AccountInfo]:
        """
        Collects the account info for the given battletags by using the DiabloApi.
        """
        infos = []
        for i, btag in enumerate(battletags):
            account = self.api.get_account(self.region, btag)
            if not account.paragonLevelSeason:
                print(f"Paragon for battletag {btag} was 0. Skipping it.")
                continue

            playtime_distrubution = next(
                x
                for x in account.seasonalProfiles.values()
                if x.seasonId == self.season
            ).timePlayed

            infos.append(
                AccountInfo(
                    battletag=account.battleTag,
                    paragon_season=account.paragonLevelSeason,
                    paragon_nonseason=account.paragonLevel,
                    playtime_distribution=playtime_distrubution,
                    last_update=account.lastUpdated,
                )
            )

            print(f"Processed {i + 1}/{len(battletags)}")
            if i > 0 and i % 20 == 0:
                sleep(0.35)

        return infos
