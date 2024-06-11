"""Used for syncing game data into Gathering"""

import xml.etree.ElementTree as ET
import json
import time
import logging
import re
import os
import xmltodict
import requests
from dotenv import load_dotenv
from lookup import price_lookup

# Variables
load_dotenv()

# Constants
LOG_FORMAT = "%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s"

# Setup Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Console Handler
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(consoleHandler)

# Log Messages
logger.info('Script is running')

class GameInfo:
    """Retrieves information of BGG items and updates them on Gathering"""
    def __init__(self, object_id):
        self.object_id = object_id
        print(os.getenv('BGG_API_URL'))
        print(os.getenv('BGG_API_ENDPOINT_BOARDGAME'))
        print(str(self.object_id))
        api_url = os.getenv('BGG_API_URL') + os.getenv('BGG_API_ENDPOINT_BOARDGAME') +  "/" + str(self.object_id) + "?stats=1"
        logger.info("using: %s", api_url)
        self.response = requests.get(api_url, timeout=3) # Get information of game through BGG API
        self.dictionary = xmltodict.parse(self.response.content) # Parse the XML to Dict
        self.json_object_string = json.dumps(self.dictionary) # Convert to String
        self.json_object = json.loads(self.json_object_string) # Convert JSON to LIST
        logger.info(object_id)

    def title(self):
        """Retrieves the title of the object id"""
        title_object = self.json_object['boardgames']['boardgame']['name']
        title = None
        for obj in title_object:
            try:
                obj_len = len(obj.keys())
            except:
                title = self.json_object['boardgames']['boardgame']['name']['#text']
                obj_len = 0

            if obj_len > 2:
                title = obj['#text']

        return title

    def expansion(self):
        """Retrieves the expansion of the object id"""
        # If Expansion for Base-game in categories, then expansion update
        if 'boardgamecategory' in  self.json_object['boardgames']['boardgame']:
            category_object = self.json_object['boardgames']['boardgame']['boardgamecategory']
            for obj in category_object:
                try:
                    is_expansion = obj['#text'] == 'Expansion for Base-game'
                except:
                    is_expansion = False
                if is_expansion:
                    if 'boardgameexpansion' in  self.json_object['boardgames']['boardgame']:
                        exp_obj = self.json_object['boardgames']['boardgame']['boardgameexpansion']
                        if isinstance(exp_obj, list):
                            for item in exp_obj:
                                if '@objectid' in item:
                                    return int(item['@objectid'])
                        else:
                            return int(exp_obj['@objectid'])
                    else:
                        return 0
        return 0

    def category(self):
        """Retrieves the category of the object id"""
        category = ""
        if 'boardgamecategory' in  self.json_object['boardgames']['boardgame']:
            category_object = self.json_object['boardgames']['boardgame']['boardgamecategory']
            for obj in category_object:
                try:
                    category += obj['#text']+ ", "
                except:
                    category = self.json_object['boardgames']['boardgame']['boardgamecategory']['#text']
            return str(category.strip(', '))
        return " "

    def mechanic(self):
        """Retrieves the mechanic of the object id"""
        mechanic = ""
        if 'boardgamemechanic' in  self.json_object['boardgames']['boardgame']:
            mechanic_object = self.json_object['boardgames']['boardgame']['boardgamemechanic']
            for obj in mechanic_object:
                try:
                    mechanic += obj['#text']+ ", "
                except:
                    mechanic = self.json_object['boardgames']['boardgame']['boardgamemechanic']['#text']
            return str(mechanic.strip(', '))
        return " "

    def bgg_rating(self):
        """Retrieves the rank of the object id"""
        return round(int(float(self.json_object['boardgames']['boardgame']['statistics']['ratings']['average'])))

    def bgg_rank_voters(self):
        """Retrieves the ratings of the object id"""
        return int(float(self.json_object['boardgames']['boardgame']['statistics']['ratings']['usersrated']))

    def year_published(self):
        """Retrieves the year published of the object id"""
        if self.json_object['boardgames']['boardgame']['yearpublished'] is not None:
            return int(self.json_object['boardgames']['boardgame']['yearpublished'])
        return 0

    def minplayers(self):
        """Retrieves the minimum players of the object id"""
        if self.json_object['boardgames']['boardgame']['minplayers'] is not None:
            return int(self.json_object['boardgames']['boardgame']['minplayers'])
        return 0

    def maxplayers(self):
        """Retrieves the maximum players of the object id"""
        if self.json_object['boardgames']['boardgame']['maxplayers'] is not None:
            return int(self.json_object['boardgames']['boardgame']['maxplayers'])
        return 0

    def playtime(self):
        """Retrieves the total playtime of the object id"""
        if self.json_object['boardgames']['boardgame']['playingtime'] is not None:
            return int(self.json_object['boardgames']['boardgame']['playingtime'])
        return 0

    def age(self):
        """Retrieves the suitable age of the object id"""
        if self.json_object['boardgames']['boardgame']['age'] is not None:
            return int(self.json_object['boardgames']['boardgame']['age'])
        return 0

    def description(self):
        """Retrieves the description of the object id"""
        return self.json_object['boardgames']['boardgame']['description']

    def image(self):
        """Retrieves the image_ url of the object id"""
        if 'image' in self.json_object['boardgames']['boardgame']:
            image = self.json_object['boardgames']['boardgame']['image']
        else:
            image = " "
        return image

    def thumbnail(self):
        """Retrieves the thumbnail of the object id"""
        if 'thumbnail' in  self.json_object['boardgames']['boardgame']:
            thumbnail = self.json_object['boardgames']['boardgame']['thumbnail']
        else:
            thumbnail = " "
        return thumbnail

    def preferred_players(self):
        """Retrieves the calculated best choice of players for the object id"""
        url = os.getenv('BGG_API_URL')+os.getenv('BGG_API_ENDPOINT_BOARDGAME')+'/'+str(self.object_id)

        response = requests.get(url, timeout=3)
        root = ET.fromstring(response.content)

        best_numplayers = 0
        highest_value = 0
        for item in root.findall('./boardgame/poll[@name="suggested_numplayers"]/results'):
            numplayers = re.sub("[^0-9]", "", item.attrib['numplayers'])
            try:
                best = int(item.find('./result[@value="Best"]').attrib['numvotes'])
            except:
                best = 0

            if best > highest_value:
                highest_value = best
                best_numplayers = numplayers


        if best_numplayers == 0:
            best_numplayers = 0
            highest_value = 0
            for item in root.findall('./boardgame/poll[@name="suggested_numplayers"]/results'):
                numplayers = re.sub("[^0-9]", "", item.attrib['numplayers'])
                try:
                    best = int(item.find('./result[@value="Recommended"]').attrib['numvotes'])
                except:
                    best = 0
                if best > highest_value:
                    highest_value = best
                    best_numplayers = numplayers

        return int(best_numplayers)

    def is_valid(self):
        """Decides if the object id is valid or not"""
        try:
            if self.json_object['boardgames']['boardgame']['error']:
                return False
            return True
        except:
            return True

def update_games(api_url):
    """Updates the games on the remote side"""
    headers = {"Content-Type": "application/json"}

    # Fetch games to update
    games_obj_in_db = requests.get(api_url, timeout=3)
    games = games_obj_in_db.json()

    logger.info('games waiting for update: %s', str(len(games)))
    game_count = 1
    # Loop the objects in JSON
    for obj in games:
        game = GameInfo(obj['object_id'])
        object_id = obj['object_id']
        logger.info('# %s/%s',str(game_count),str(len(games)))

        if game.is_valid():

            # Prepare JSON Payload
            game_json = {
                    "bgg_rank_voters": game.bgg_rank_voters(),
                    "bgg_rating": game.bgg_rating(),
                    "category": game.category(),
                    "mechanic": game.mechanic(),
                    "title": game.title(),
                    "expansion_to": game.expansion(),
                    "year_published": game.year_published(),
                    "minplayers": game.minplayers(),
                    "maxplayers": game.maxplayers(),
                    "preferred_players": game.preferred_players(),
                    "playtime": game.playtime(),
                    "age": game.age(),
                    "estimated_price": price_lookup.game_title(game.title()),
                    "description": game.description(),
                    "thumbnail_url": game.thumbnail(),
                    "image_url": game.image()
                    }

            #Send information to API

            try:
                url = os.getenv('GATHERING_API_URL')+"/"+object_id
                response = requests.put(url,data=json.dumps(game_json), headers=headers,timeout=5)
                if response.status_code == 200:
                    logger.info(game.title() ,' successfully updated')
                else:
                    logger.error(game.title() ,' failed to update. status_code: ',str(response.status_code))
            except requests.exceptions.HTTPError as errh:
                logger.error(errh)
            except requests.exceptions.ConnectionError as errc:
                logger.error(errc)
            except requests.exceptions.Timeout as errt:
                logger.error(errt)
            except requests.exceptions.RequestException as err:
                logger.error(err)

            time.sleep(2) # Wait in order to not overuse the API

        else:
            logger.info('No data from current game - Skipping')

        game_count += 1

    if len(str(games)) > 2:
        logger.info('Successfully updated games')
    else:
        logger.info('No games to update')

if __name__ == "__main__":
    while True:
        update_games(os.getenv('GATHERING_API_URL_NODATA'))
        time.sleep(120)
        logger.info('wait done - check again')
