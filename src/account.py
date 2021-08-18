from dataclasses import dataclass
from typing import Mapping, Optional, List, Dict


@dataclass
class Blacksmith:
    slug: Optional[str] = None
    level: Optional[int] = None


@dataclass
class Death:
    killer: Optional[int] = None
    time: Optional[int] = None


@dataclass
class FallenHero:
    heroId: Optional[int] = None
    name: Optional[str] = None
    fallenHeroclass: Optional[str] = None
    level: Optional[int] = None
    elites: Optional[int] = None
    hardcore: Optional[bool] = None
    death: Optional[Death] = None
    gender: Optional[int] = None


@dataclass
class HeroKills:
    elites: Optional[int] = None


@dataclass
class Hero:
    id: Optional[int] = None
    name: Optional[str] = None
    heroclass: Optional[str] = None
    classSlug: Optional[str] = None
    gender: Optional[int] = None
    level: Optional[int] = None
    kills: Optional[HeroKills] = None
    paragonLevel: Optional[int] = None
    hardcore: Optional[bool] = None
    seasonal: Optional[bool] = None
    dead: Optional[bool] = None
    lastupdated: Optional[int] = None


@dataclass
class AccountKills:
    monsters: Optional[int] = None
    elites: Optional[int] = None
    hardcoreMonsters: Optional[int] = None


@dataclass
class Progression:
    act1: Optional[bool] = None
    act3: Optional[bool] = None
    act2: Optional[bool] = None
    act5: Optional[bool] = None
    act4: Optional[bool] = None


@dataclass
class SeasonalProfile:
    seasonId: Optional[int] = None
    paragonLevel: Optional[int] = None
    paragonLevelHardcore: Optional[int] = None
    kills: Optional[AccountKills] = None
    timePlayed: Optional[Mapping[str, float]] = None
    highestHardcoreLevel: Optional[int] = None


@dataclass
class Account:
    battleTag: Optional[str] = None
    paragonLevel: Optional[int] = None
    paragonLevelHardcore: Optional[int] = None
    paragonLevelSeason: Optional[int] = None
    paragonLevelSeasonHardcore: Optional[int] = None
    guildName: Optional[str] = None
    heroes: Optional[List[Hero]] = None
    lastHeroPlayed: Optional[int] = None
    lastUpdated: Optional[int] = None
    kills: Optional[AccountKills] = None
    highestHardcoreLevel: Optional[int] = None
    timePlayed: Optional[Mapping[str, float]] = None
    progression: Optional[Progression] = None
    fallenHeroes: Optional[List[FallenHero]] = None
    seasonalProfiles: Optional[Dict[str, SeasonalProfile]] = None
    blacksmith: Optional[Blacksmith] = None
    jeweler: Optional[Blacksmith] = None
    mystic: Optional[Blacksmith] = None
    blacksmithSeason: Optional[Blacksmith] = None
    jewelerSeason: Optional[Blacksmith] = None
    mysticSeason: Optional[Blacksmith] = None
    blacksmithHardcore: Optional[Blacksmith] = None
    jewelerHardcore: Optional[Blacksmith] = None
    mysticHardcore: Optional[Blacksmith] = None
    blacksmithSeasonHardcore: Optional[Blacksmith] = None
    jewelerSeasonHardcore: Optional[Blacksmith] = None
    mysticSeasonHardcore: Optional[Blacksmith] = None
