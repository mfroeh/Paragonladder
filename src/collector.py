from typing import ItemsView, List, Tuple
from account import Account
from constants import LeaderboardType
from diablo_api import DiabloApi
from time import sleep


class Collector:
    def __init__(self, season: int, region: str, api: DiabloApi):
        self.season = season
        self.api = api
        self.region = region

    def collect_battletags(self) -> List[ItemsView[str, int]]:
        """
        Collects a list of battletag, paragon pairs from all softcore leaderboards by using the DiabloApi.
        """
        battletags = {}  # Battletag : Paragon pairs
        for l in self.api.get_season_leaderboard_info(self.region, self.season):
            leaderboard = self.api.get_season_leaderboard(self.region, self.season, l)
            for row in leaderboard.row:
                for player in row.player:
                    battletag = next(
                        d.string for d in player.data if d.id == "HeroBattleTag"
                    )
                    paragon = next(
                        int(d.number) for d in player.data if d.id == "ParagonLevel"
                    )

                    if not battletag in battletags or paragon > battletags[battletag]:
                        battletags[battletag] = paragon

        return sorted(battletags.items(), key=lambda p: p[1], reverse=True)

    def collect_accounts(self, battletags: List[str]) -> List[Account]:
        """
        Collects the accounts for the given battletags by using the DiabloApi.
        """
        accounts = []
        for i, btag in enumerate(battletags):
            account = self.api.get_account(self.region, btag)
            if account and account.battleTag:
                accounts.append(account)

            if i > 0 and i % 20 == 0:
                sleep(0.35)

        print(f"Collected {len(battletags)} accounts")

        return accounts
