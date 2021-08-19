from leaderboard import Leaderboard
from account import Account
from blizzardapi import BlizzardApi
from dacite import from_dict


class DiabloApi:
    def __init__(self, api: BlizzardApi, locale: str):
        self.api = api
        self.locale = locale

    def get_account(self, region: str, battletag: str) -> Account:
        battletag = battletag.replace("#", "%23")

        try:
            data = self.api.diablo3.community.get_api_account(
                region, self.locale, battletag
            )

            return from_dict(Account, data)
        except Exception as e:
            print(
                f"Failed to request account for battletag {battletag}."
            )
            return Account(battleTag=battletag.replace("%23", "#"))

    def get_current_season(self, region: str) -> int:
        return int(
            self.api.diablo3.game_data.get_season_index(region)["current_season"]
        )

    def get_season_leaderboard(
        self, region: str, season: int, leaderboard: str
    ) -> Leaderboard:
        data = self.api.diablo3.game_data.get_season_leaderboard(
            region, season, leaderboard
        )

        return from_dict(Leaderboard, data)
