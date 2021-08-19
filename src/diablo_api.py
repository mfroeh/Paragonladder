from leaderboard import Leaderboard
from account import Account
from enum import Enum
from blizzardapi import BlizzardApi
from dacite import from_dict


class LeaderboardType(Enum):
    FOUR_PLAYER = "rift-team-4"
    THREE_PLAYER = "rift-team-3"
    TWO_PLAYER = "rift-team-2"


class Locale(Enum):
    EN_US = "en_US"


class Region(Enum):
    EU = "eu"
    US = "us"
    KR_TW = "kr"
    CN = "cn"


class DiabloApi:
    def __init__(self, api: BlizzardApi, locale: Locale):
        self.api = api
        self.locale = locale.value

    def get_account(self, region: Region, battletag: str) -> Account:
        battletag = battletag.replace("#", "%23")
        try:
            data = self.api.diablo3.community.get_api_account(
                region.value, self.locale, battletag
            )

            return from_dict(Account, data)
        except Exception as e:
            print(f"Failed request account data for battletag {battletag}")
            return Account()

    def get_current_season(self, region: Region) -> int:
        return int(
            self.api.diablo3.game_data.get_season_index(region.value)["current_season"]
        )

    def get_season_leaderboard(
        self, region: Region, season: int, leaderboard: LeaderboardType
    ) -> Leaderboard:
        data = self.api.diablo3.game_data.get_season_leaderboard(
            region.value, season, leaderboard.value
        )

        return from_dict(Leaderboard, data)
