from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Title:
    enUS: Optional[str] = None
    esMX: Optional[str] = None
    ptBR: Optional[str] = None
    deDE: Optional[str] = None
    enGB: Optional[str] = None
    esES: Optional[str] = None
    frFR: Optional[str] = None
    itIT: Optional[str] = None
    plPL: Optional[str] = None
    ptPT: Optional[str] = None
    ruRU: Optional[str] = None
    koKR: Optional[str] = None
    zhTW: Optional[str] = None
    zhCN: Optional[str] = None


@dataclass
class Column:
    id: Optional[str] = None
    hidden: Optional[bool] = None
    order: Optional[int] = None
    label: Optional[Title] = None
    type: Optional[str] = None


@dataclass
class Data:
    id: Optional[str] = None
    number: Optional[int] = None
    timestamp: Optional[int] = None
    string: Optional[str] = None


@dataclass
class Player:
    key: Optional[str] = None
    accountId: Optional[int] = None
    data: Optional[List[Data]] = None


@dataclass
class Row:
    player: Optional[List[Player]] = None
    order: Optional[int] = None
    data: Optional[List[Data]] = None


@dataclass
class Leaderboard:
    row: Optional[List[Row]] = None
    key: Optional[str] = None
    title: Optional[Title] = None
    column: Optional[List[Column]] = None
    last_update_time: Optional[str] = None
    generated_by: Optional[str] = None
    greater_rift: Optional[bool] = None
    greater_rift_team_size: Optional[int] = None
    season: Optional[int] = None