from analyzer import Analyzer
from collector import Collector
from constants import Locale, Region, regions
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
    if not current_season:
        print(f"Failed to get current season for {region}. Skipping it.")
        continue

    db = Database(current_season, region)
    collector = Collector(current_season, region, api)
    analyzer = Analyzer(current_season, region)

    # Get the battletags of the currently tracked accounts
    battletags = db.get_tracked_battltags()
    accounts = collector.collect_accounts(battletags)
    infos = analyzer.analyze_accounts(accounts)
    db.update_tracked(infos)

    # Collect battletags from all leaderboards
    btags = collector.collect_battletags()
    print(f"Collected a total of {len(btags)} unique battletags for {region}.")

    # Determine which new accounts to track
    tracked = {a.battletag: a.paragon_season for a in db.get_tracked()}
    new_to_track = []
    for btag, p in btags:
        if p > tracked.values()[0] and btag not in tracked.keys():
            new_to_track.append(btag)
            tracked[btag] = p

            # Remove trumped battletag
            trumped_btag = tracked.keys()[0]
            del tracked[trumped_btag]
            db.remove_tracked_account(trumped_btag)

            tracked = dict(sorted(tracked.items(), key=lambda item: item[1]))

    # Collect account info and insert the new accounts as tracked
    accounts = collector.collect_accounts(new_to_track)
    infos = analyzer.analyze_accounts(accounts)
    db.update_tracked(infos)

make_site()
