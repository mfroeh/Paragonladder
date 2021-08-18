from extractor import Extractor
from diablo_api import DiabloApi, Locale, Region
from database import Database
from blizzardapi import BlizzardApi
import datetime as dt
import argparse
from pages import make_site
from constants import regions

parser = argparse.ArgumentParser()
parser.add_argument("--client_id")
parser.add_argument("--client_secret")

args = vars(parser.parse_args())
if not args["client_id"] or not args["client_secret"]:
    print("No client id or secret given.")
    quit()


client_id = args["client_id"]
client_secret = args["client_secret"]

api = DiabloApi(BlizzardApi(client_id, client_secret), Locale.EN_US)

for region in regions:
    current_season = api.get_current_season(region)

    e = Extractor(current_season, region, api)
    db = Database(current_season, region)

    # btags = e.collect_battletags()
    # db.insert_battletags(btags)

    # battletags = db.get_battltags()
    # paragon_infos = e.collect_account_infos(battletags)
    # db.update_account_infos(paragon_infos)

make_site()
