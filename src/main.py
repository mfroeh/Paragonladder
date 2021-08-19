from analyzer import Analyzer
from collector import Collector
from constants import Locale, regions
from diablo_api import DiabloApi
from database import Database
from blizzardapi import BlizzardApi
import argparse
from pages import make_site

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

    db = Database(current_season, region)
    collector = Collector(current_season, region, api)
    analyzer = Analyzer(current_season, region)

    btags = collector.collect_battletags()
    db.insert_battletags(btags)

    battletags = db.get_battltags()
    accounts = collector.collect_accounts(battletags)
    infos = analyzer.analyze_accounts(accounts)

    db.update_account_infos(infos)

make_site()
