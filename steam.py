import requests
from dotenv import load_dotenv
import json
import os
from roman_num import parse_roman
from string import ascii_letters

class Wishlist:
    def __init__(self,w_list) :
        self.w_list = w_list
        self.key_list = list(w_list.keys())
        self.length = len(self.key_list)
        self.games = []
        for i in range(self.length):
            title = w_list[self.key_list[i]]['name']
            capsule = w_list[self.key_list[i]]['capsule']
            try:
                steam_price  = float(w_list[self.key_list[i]]['subs'][0]['price'])/100
            except IndexError:
                steam_price = None
            new_game = Game(title,steam_price,capsule)
            self.games.append(new_game)
    def __str__(self):
        output = ''
        for i in range(self.length):
            output += str(self.games[i]) + '\n'
        return output
        
class Game:
    def __init__(self,title='',steam_price='',capsule=''):
        self.title = title
        self.itad_title = self.itad_parse()
        self.steam_price = steam_price
        self.capsule=capsule
        self.epic_price = None
        self.epic_url = None
        self.gog_price = None
        self.gog_url = None
        self.origin_price = None
        self.origin_url = None
        self.humble_price = None
        self.humble_url = None
        
    def __str__(self) -> str:
        output = ''
        output += self.title
        output += '\n'
        output += f'Steam: {self.steam_price} '
        output += f'Epic: {self.epic_price} '
        output += f'GOG: {self.gog_price}'
        return output

    def __repr__(self) -> str:
        return f'{self.title} {self.steam_price}'

    def itad_parse(self):
        # self.itad_title must remove all non-ascii characters and convert all nums to roman numerals, as well as remove 'the'
        itad_title = ''
        for i in list(self.title):
            if i.isdigit() and i != '0':
                itad_title += str(parse_roman(int(i)))
            elif i not in ascii_letters:
                continue
            else:
                itad_title += i
        itad_title = itad_title.lower().replace('the','')
        return itad_title
    
    def epic(self,e_price):
        self.epic_price = e_price
    
    def gog(self,gog_price):
        self.gog_price = gog_price

def main():
    welcome()
    warning()
    username = input("Enter username to retrieve wishlist: ")
    steamID = get_steamid(username)
    wishlist_games = get_wishlist(steamID)
    wishlist = Wishlist(wishlist_games)
    wishlist = itad(wishlist)
    print(wishlist)
    exit()

def get_steamid(username='OliveOil4Lube'):
    load_dotenv()
    STEAM_KEY = os.getenv('STEAM_KEY')
    url = 'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/'
    payload = {
        'key' : STEAM_KEY,
        'vanityurl' : username
    }
    r = requests.get(url,params=payload)
    user = json.loads(r.text)
    return user['response']['steamid']

def get_wishlist(steamID='76561198918721504'):
    url = 'https://store.steampowered.com/wishlist/profiles/' + steamID + '/wishlistdata/'
    r = requests.get(url)
    g = json.loads(r.text)
    return g

def itad(wishlist):
    url = 'https://api.isthereanydeal.com/v01/game/prices/'
    load_dotenv()
    ITAD_KEY = os.getenv('ITAD_KEY')
    # i iterates through every title
    for i in range(wishlist.length):
        payload = {
            'key' : ITAD_KEY,
            'plains' : str(wishlist.games[i].itad_title),
            'country' : 'USA',
            # 'shops' : 'epic,gog'
        }
        r = requests.get(url,params=payload)
        game =json.loads(r.text)
        length = len(game['data'][wishlist.games[i].itad_title]['list'])
        if length != 0:
            # j iterates through every store that is found for the title
            for j in range(length):
                shop_id = game['data'][wishlist.games[i].itad_title]['list'][j]['shop']['id']
                price = game['data'][wishlist.games[i].itad_title]['list'][j]['price_new']
                if shop_id == 'epic':
                    wishlist.games[i].epic_url = game['data'][wishlist.games[i].itad_title]['list'][j]['url']
                    if price == 0:
                        wishlist.games[i].epic('Free')
                    else:
                        wishlist.games[i].epic(price)
                if shop_id == 'gog':
                    wishlist.games[i].gog_url = game['data'][wishlist.games[i].itad_title]['list'][j]['url']
                    wishlist.games[i].gog(price)
                if shop_id == 'origin':
                    wishlist.games[i].origin_url = game['data'][wishlist.games[i].itad_title]['list'][j]['url']
                    wishlist.games[i].origin_price = price
                    pass
                if shop_id == 'humblestore':
                    wishlist.games[i].humble_url = game['data'][wishlist.games[i].itad_title]['list'][j]['url']
                    wishlist.games[i].humble_price = price

    return wishlist

def welcome():
    print("Welcome! This is an application that uses your steam wishlist to find prices for games on your wishlist on competing platforms.")
    print("Uses IsThereAnyDeal.com. Consider purchasing through their affiliate links to support.\n")

def warning():
    print('Custom URL must be set under edit profile to work. \nGo to https://www.steamcommunity.com/id/USERNAMEGOESHERE/edit/info and change custom URL to use.')

if __name__=='__main__':
    main()