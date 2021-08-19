from typing import List
from account import Account
from constants import LeaderboardType
from diablo_api import DiabloApi
from time import sleep


class Collector:
    def __init__(self, season: int, region: str, api: DiabloApi):
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

    def collect_accounts(self, battletags: List[str]) -> List[Account]:
        """
        Collects the accounts for the given battletags by using the DiabloApi.
        """
        accounts = []
        for i, btag in enumerate(battletags):
            account = self.api.get_account(self.region, btag)
            accounts.add(account)

            print(f"Collected {i + 1}/{len(battletags)} accounts")
            if i > 0 and i % 20 == 0:
                sleep(0.35)

        return accounts
