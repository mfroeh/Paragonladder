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

    def update_account_infos(self, infos: List[AccountInfo]) -> NoReturn:
        for info in infos:
            self.db.update(asdict(info), Query().battletag == info.battletag)

    def insert_battletags(self, battletags: List[str]) -> NoReturn:
        i = 0
        for btag in battletags:
            if not self.db.search(Query().battletag == btag):
                self.db.insert(asdict(AccountInfo(btag)))
                i += 1

        print(f"Inserted {i} new battletags")

    def get_account_infos(self) -> List[AccountInfo]:
        """
        Returns all account infos that have a paragon level in the season.
        """
        return [AccountInfo(**d) for d in self.db.all() if d["paragon_season"]]

    def get_battltags(self) -> List[str]:
        return [x["battletag"] for x in self.db.all()]
