from core import *

def DoomWorld(query: str):
    Website(BuildSearchURL("https://www.doomworld.com/search/?q=", query, "%20"))

def DeepL(query: str, _lang: str = "en"):
    Website(BuildSearchURL(f"https://www.deepl.com/translator#{_lang}/", query, "%20"))

def Twitch(query: str):
    Website(BuildSearchURL("https://www.twitch.tv/search?term=", query, "%20"))
