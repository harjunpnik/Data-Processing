import os
import re
import bs4
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

def createGameDf():
    '''Creates game dataframe with "Game|Rating|#Reviews|Discount%|Price|Original_price|Release_year|Win|Lin|OSX|Time" columns '''
    games_df = pd.DataFrame(columns=['Game', 'Rating', 'Review_amount','Discount%', 'Price', 'Original_price', 'Release_year', 
                                 'Win', 'Lin','OSX','Time'])
    games_df = games_df.astype({'Game': 'object','Rating': 'int64','Review_amount': 'int64','Discount%': 'int64','Price': 'object',
                            'Original_price': 'object','Release_year': 'int64', 'Win': 'int64', 'Lin': 'int64',
                            'OSX': 'int64', 'Time': 'object'})
    return games_df

def fecthSite(page_nr):
    '''Fetches steam sale site. Takes in aparameter page_nr that defines what page it fetches'''
    base_steam_url = "https://store.steampowered.com/search/?specials=1&page="
    uClient = uReq( base_steam_url + str(page_nr))
    page_html = uClient.read()
    uClient.close()
    return page_html

def game_support(game,platform_class):
    '''game_support - Takes in game and searches for a span including the platform class'''
    platform_support = game.find("span", {"class": platform_class})
    platform_support = 1 if platform_support != None else 0
    return platform_support

def reviewScore(game):
    ''' Takes game as a parameter and returns a score from 1-9 depending on the review tooltip'''
    rating_text = game.find("div", {"class":"col search_reviewscore responsive_secondrow"}).span['data-tooltip-html']
    rating_text = re.search("(?<=)(.*?)(?=<)", rating_text).group(0)
    
    switcher = {
        'Overwhelmingly Positive': 9,
        'Very Positive':8,
        'Positive':7,
        'Mostly Positive':6,
        'Mixed':5,
        'Mostly Negative':4,
        'Negative':3,
        'Mostly Negative':2,
        'Overwhelmingly Negative':1
    }
    
    return switcher.get(rating_text, 0)

def gameDataFrame(game, fetch_timestamp):
    '''gameDataFrame - takes in game as parameter and timestamp data was fetched. Returns a data  '''
    # GAME NAME
    game_name = game.find("span", {"class":"title"}).getText()
    # RATING
    try:
        rating = reviewScore(game)
    except:
        rating = 0
    # REVIEW AMOUNT
    try:
        review_amount = game.find("div", {"class":"col search_reviewscore responsive_secondrow"}).span['data-tooltip-html']
        review_amount = re.search("(?<= )([0-9,]+)(?= )", review_amount).group(0)
        review_amount = review_amount.replace(",","")
    except:
        review_amount = 0
    # DISCOUNT
    try:
        discount = game.find("div", {"class":"col search_discount responsive_secondrow"}).span.getText()
        discount = re.search("(?<=-)(.*?)(?=%)", discount).group(0) # Remove - and % from text
    except:
        discount = 0
    # PRICE
    try:
        price = game.find("div", {"class":"col search_price discounted responsive_secondrow"}).getText()
        price = re.search("(?<=€)(.*?)(?=€)", price).group(0) # Takes only the price that is between two € chars
    except:
        price = 0
    # ORIGINAL PRICE
    try:
        og_price = game.find("div", {"class":"col search_price discounted responsive_secondrow"}).span.strike.getText()[:-1]
    except:
        og_price = 0
    # RELEASE YEAR
    release_year = game.find("div", {"class":"col search_released responsive_secondrow"}).getText()[-4:] # last 4 digits is year
    # WIN
    win_support = game_support(game, "platform_img win")
    # LIN
    lin_support = game_support(game, "platform_img linux")
    # OSX
    mac_support = game_support(game, "platform_img mac")
    # TIME
    time = fetch_timestamp
    
    data = {
        'Game': game_name, 
        'Rating': rating,
        'Review_amount': review_amount,
        'Discount%': discount,
        'Price': price, 
        'Original_price': og_price, 
        'Release_year': release_year, 
        'Win': win_support, 
        'Lin': lin_support,
        'OSX': mac_support,
        'Time': time
      }
    return data

# create empty dataframe
games_df = createGameDf()

# fetch data from 5 first pages
for x in range(1, 6):
    page_html = fecthSite(x)
    fetch_timestamp = str(datetime.now())
    page_soup = soup(page_html, 'html.parser')
    games = page_soup.findAll("a", {"class":"search_result_row"})
    for game in games:
        game_data = gameDataFrame(game, fetch_timestamp)
        games_df = games_df.append(game_data, ignore_index=True)

# Save to CSV file        
cwd = os.getcwd()
path = cwd + "\\SteamSale.csv"
if(os.path.exists(path)):
    # SAVE in same file
    old_csv = pd.read_csv(path)
    # CSV is release_year is read as float and  has ".0" after each number so that must be removed
    old_csv['Release_year'] = old_csv['Release_year'].map(lambda x: str(x).rstrip(".0"))
    # I don't want 
    old_csv['Release_year'] = old_csv['Release_year'].map(lambda x: str(x).rstrip(".0") if (str(x) != "nan") else str(x).replace("nan",""))
    concatenated_csv = pd.concat([old_csv,games_df])
    concatenated_csv.to_csv( path, index=False, header=True)
else:
    # CREATE new file
    export_csv = games_df.to_csv (path, index = None, header=True)