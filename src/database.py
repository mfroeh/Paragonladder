from dataclasses import asdict
from typing import List, NoReturn
from tinydb import TinyDB, Query
from analyzer import AccountInfo
from pathlib import Path


class Database:
    def __init__(self, season: int, region: str):
        self.season = season
        self.region = region

        Path(f"../database/{season}").mkdir(parents=True, exist_ok=True)
        self.db = TinyDB(f"../database/{season}/{region}.json")

    def update_tracked(self, infos: List[AccountInfo]) -> NoReturn:
        for info in infos:
            if not self.db.contains(Query().battletag == info.battletag):
                self.db.insert(asdict(info))
            else:
                self.db.update(asdict(info), Query().battletag == info.battletag)

    def remove_tracked_account(self, battletag: str) -> NoReturn:
        self.db.remove(Query().battletag == battletag)

    def get_tracked(self) -> List[AccountInfo]:
        """
        Returns the account info of all currently tracked accounts.
        """
        return sorted(
            [AccountInfo(**d) for d in self.db.all()],
            key=lambda x: x.paragon_season,
        )

    def get_tracked_battltags(self) -> List[str]:
        """
        Returns the battle tags of the currently tracked accounts.
        """
        return [x["battletag"] for x in self.db.all()]
