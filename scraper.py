import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import string
import re
import datetime
import sqlite3
import time


e_name = []
f1 = []
f2 = []




def scrape_data():

        data = requests.get("http://ufcstats.com/statistics/events/upcoming")
        soup = BeautifulSoup(data.text, 'html.parser')
        table = soup.find('table', {"class": "b-statistics__table-events"})
        links = table.find_all('a', href=True)

        for link in links:
            all_links.append(link.get('href'))

        for link in all_links:
            print(f"Now currently scraping link: {link}")

            data = requests.get(link)
            soup = BeautifulSoup(data.text, 'html.parser')
            time.sleep(1)

            h2 = soup.find("h2")
            e_name.append(h2.text.strip())

            rows = soup.find_all('table', {"class": "b-fight-details__table b-fight-details__table_style_margin-top b-fight-details__table_type_event-details js-fight-table"})

            for row in rows:


                    fighters = row.find_all('a', {"href": re.compile("http://ufcstats.com/fighter-details")})

                    try:
                        f1.append(fighters[0].text.strip())
                        f2.append(fighters[1].text.strip())
                    except IndexError:
                        f1.append("null")
                        f2.append("null")
                    continue


        return None

#preprocessing
# remove rows where DOB is null
# impute stance as orthodox for missing stances
def create_df():
    #create empty dataframe
    df = pd.DataFrame()

    df["Event"] = e_name
    df["Fighter1"] = f1
    df["Fighter2"] = f2

    return df

scrape_data()
df = create_df()
print("Scraping completed")

conn = sqlite3.connect('data.sqlite')
df.to_sql('data', conn, if_exists='replace')
print('Db successfully constructed and saved')
conn.close()
