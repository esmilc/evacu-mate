#!/usr/bin/env python3
"""
Batch-geocode shelters from simulation/florida_shelters.json using Google Geocoding API.

Writes simulation/florida_shelters_geocoded.json as an array of shelters with added
`lat` and `lng` fields. The script is resumable: it will preserve already-geocoded
entries in the output file and continue from where it left off.

Usage:
  set GOOGLE_MAPS_API_KEY=YOUR_KEY
  python scripts/geocode_shelters.py

Notes:
- This script performs network calls and may incur Google billing. Use responsibly.
- It includes simple rate-limiting and exponential backoff.
"""
import os
import time
import json
import requests
import argparse
from typing import Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, '..'))
SIM_IN = os.path.join(REPO_ROOT, 'simulation', 'florida_shelters.json')
SIM_OUT = os.path.join(REPO_ROOT, 'simulation', 'florida_shelters_geocoded.json')

API_KEY = os.getenv('GOOGLE_MAPS_API_KEY') or os.getenv('GOOGLE_MAPS_API')
GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

def geocode_address(address: str) -> Tuple[float, float]:
    params = {'address': address, 'key': API_KEY}
    resp = requests.get(GEOCODE_URL, params=params, timeout=10)
    resp.raise_for_status()
    j = resp.json()
    status = j.get('status')
    if status != 'OK' or not j.get('results'):
        raise RuntimeError(f'Geocode failed: {status} for {address}')
    loc = j['results'][0]['geometry']['location']
    return float(loc['lat']), float(loc['lng'])

def load_input() -> dict:
    with open(SIM_IN, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_progress() -> list:
    if os.path.exists(SIM_OUT):
        with open(SIM_OUT, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_progress(out_list: list):
    with open(SIM_OUT, 'w', encoding='utf-8') as f:
        json.dump(out_list, f, indent=2)

def flatten_input(data: dict) -> list:
    flattened = []
    for county, entries in data.items():
        for e in entries:
            name = e.get('name') or e.get('facility') or 'Unnamed'
            street = e.get('street_address') or e.get('address') or ''
            address = f"{street}, {county}, FL" if street else f"{county}, FL"
            flattened.append({**e, 'county': county, 'address': address})
    return flattened

def main():
    parser = argparse.ArgumentParser(description='Batch-geocode simulation shelters')
    parser.add_argument('--limit', type=int, default=0, help='Limit number of geocode requests (0 = all)')
    parser.add_argument('--dry-run', action='store_true', help='Dry run: do not call external API')
    args = parser.parse_args()

    if not API_KEY:
        print('Missing GOOGLE_MAPS_API_KEY in env. Export it and retry.')
        return 2

    data = load_input()
    items = flatten_input(data)
    if args.limit and args.limit > 0:
        items = items[: args.limit]

    progress = load_progress()

    # Build an index for already-processed addresses (by name+address)
    processed = {(p.get('name'), p.get('address')): p for p in progress}

    out = list(progress)  # start from existing
    total = len(items)
    for i, item in enumerate(items):
        key = (item.get('name'), item.get('address'))
        if key in processed:
            print(f'[{i+1}/{total}] Skipping already-processed: {item.get("name")}')
            continue

        print(f'[{i+1}/{total}] Geocoding: {item.get("name")} - {item.get("address")}')
        if args.dry_run:
            print('  dry-run: skipping API call')
            out.append(item)
            save_progress(out)
            continue

        # retry/backoff
        backoff = 1.0
        while True:
            try:
                lat, lng = geocode_address(item['address'])
                item['lat'] = lat
                item['lng'] = lng
                out.append(item)
                # persist every successful geocode to allow resume
                save_progress(out)
                print(f'  OK -> {lat},{lng}')
                break
            except Exception as e:
                print(f'  Geocode error: {e}. Backoff {backoff}s')
                time.sleep(backoff)
                backoff = min(backoff * 2, 30.0)

        # polite cooldown to avoid hitting rate limits; adjust as needed
        time.sleep(0.12)

    print('Geocoding complete. Output written to', SIM_OUT)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
