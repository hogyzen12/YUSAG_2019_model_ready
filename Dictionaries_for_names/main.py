#!/usr/bin/env python3

# mods
import sys
import asyncio
import csv
import pandas as pd
from pyppeteer import launch
from collections import OrderedDict
from bs4 import BeautifulSoup, SoupStrainer

async def get_browser():
    return await launch({"headless": True})

async def get_page(browser, url):
    page = await browser.newPage()
    await page.goto(url)
    source = await page.content()

    # Send back bs4 object
    return BeautifulSoup(source, 'lxml')

async def soup(source):
    p = "laceholder"
    return p

async def main():

    url = sys.argv[1]
    results = []
    header = ['Home','Away','H_Total','A_Total','H_Q1','H_Q2','H_Q3','H_Q4',
              'A_Q1','A_Q2','A_Q3','A_Q4']
    chrome = await get_browser()
    chrome_request = await get_page(chrome, url)

    scoreboards = chrome_request.find_all("div", {"class": "scoreboard-wrapper"})

    for board in scoreboards:

        # Status check
        check = board.select_one(".date-time").get_text(strip=True)

        if (check == 'Postponed'):
            continue

        # Fetch everything in element 'away'
        away_all = board.select_one(".away")

        # Pull the name out of the soup
        # sb-team-abbrev 
        # sb-team-short
        away_name = away_all.select_one(".sb-team-abbrev").get_text(strip=True)
        away_total = away_all.select_one(".total").get_text(strip=True)
        away_quarts = away_all.find_all("td", {"class": "score"})
        away_q_clean = []

        for quart in away_quarts:
            away_q_clean.append(quart.get_text(strip=True))

        # Rinse repeat
        home_all = board.select_one(".home")
        home_name = home_all.select_one(".sb-team-abbrev").get_text(strip=True)
        home_total = home_all.select_one(".total").get_text(strip=True)
        home_quarts = home_all.find_all("td", {"class": "score"})
        home_q_clean = []

        for quart in home_quarts:
            home_q_clean.append(quart.get_text(strip=True))

        set_list = [
            home_name,
            away_name,
            home_total,
            away_total,
            home_q_clean[0],
            home_q_clean[1],
            home_q_clean[2],
            home_q_clean[3],
            away_q_clean[0],
            away_q_clean[1],
            away_q_clean[2],
            away_q_clean[3]
        ]

        results.append(set_list)

    await chrome.close()

    df_csv = pd.DataFrame(results, columns=header).to_csv("scrapy_espn.csv")

    return

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

