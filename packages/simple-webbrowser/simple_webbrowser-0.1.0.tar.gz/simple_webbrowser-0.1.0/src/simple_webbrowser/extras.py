Search = None

def initialize(__maker):
    global Search
    
    Search = __maker

def DoomWorld(query: str):
    Search("https://www.doomworld.com/search/?q=", query, "%20")

def DeepL(query: str, _lang: str = "en"):
    Search(f"https://www.deepl.com/translator#{_lang}/", query, "%20")

def Twitch(query: str):
    Search("https://www.twitch.tv/search?term=", query, "%20")
