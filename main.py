import requests, os
from dotenv import load_dotenv
from database import engine
from models import Base, Games
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, timezone
from llm import gerar_query, formatar_resposta

load_dotenv()

#CONSTANTS
API_KEY = os.getenv("STEAM_API_KEY")
URL = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"

def resolve_vanity_url(vanity):
    """Resolves a vanity URL to a Steam ID"""
    #DICTONARY
    params = {
        "key": API_KEY,
        "vanityurl": vanity
    }
    
    #REQUEST
    response = requests.get("https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/", params=params)
    data = response.json()
    
    if data["response"]["success"] != 1:
        return None
    else:
        return data["response"]["steamid"]

def fetch_steam_data(steam_id):
    """Fetches data from Steam API"""
    #DICTONARY
    params = {
        "key": API_KEY,
        "steamid": steam_id,
        "include_appinfo" : True,
        "format" : "json",
        "include_played_free_games" : True
    }

    #REQUEST
    response = requests.get(URL, params=params)
    data = response.json()

    return data

def fill_database(data):
    """Creates the database and fills  with data from Steam API"""
    #CREATE TABLE
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    #CREATE SESSION
    session = Session(engine)

    #INSERT DATA
    for game in data["response"]["games"]:
        game_data = Games(
            appid = game["appid"],
            name = game["name"],
            img_icon_url = game["img_icon_url"],
            playtime_forever = game["playtime_forever"],
            playtime_windows_forever = game["playtime_windows_forever"],
            playtime_linux_forever = game["playtime_linux_forever"],
            playtime_deck_forever = game["playtime_deck_forever"],
            playtime_disconnected = game["playtime_disconnected"],
            rtime_last_played = datetime.fromtimestamp(game["rtime_last_played"], tz=timezone.utc)
        )

        session.add(game_data)
        
    session.commit()
    
    return session

def run_prompt(session, prompt):
    """Runs the prompt and returns the answer"""
    #GENERATE QUERY
    query = gerar_query(prompt)

    #EXECUTE QUERY
    result = session.execute(text(query))
    lines = result.fetchall()

    #FORMAT ANSWER
    answer = formatar_resposta(prompt, lines)

    return answer


# data = fetch_steam_data()
# session = fill_database(data)
# while True:
#     prompt = input("Digite aqui seu prompt. (Digite sair para sair)\n")
#     if prompt.lower() == "sair":
#         break
#     answer = run_prompt(session, prompt)
#     print(answer)
