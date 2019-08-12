import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import string
import re
import datetime
import sqlite3
import time

all_links = []
e_name = []
f1 = []
f2 = []




def scrape_data():

        for alpha in alphabets:
        links.append("http://www.fightmetric.com/statistics/fighters?char=" + alpha + "&page=all")

        # now that we have a list of links we need to iterate it with BeautifulSoup
        for link in links:
        print(f"Currently on this link: {link}")

        data = requests.get(link)
        soup = BeautifulSoup(data.text, 'html.parser')
        names = soup.find_all('a', href=True)
       
        # list to store url page of fighters
        fighters = []

        for name in names:
            fighters.append(name['href'])

        fighters = sorted(set(fighters))

        for fighter in fighters:
       

            h2 = soup.find("h2")
            e_name.append(h2.text.strip())

                
                    data = requests.get(fighter)
                    soup = BeautifulSoup(data.text, 'html.parser')

                    fighters = fighter.find_all('a', {"href": re.compile("http://ufcstats.com/fighter-details")})

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
