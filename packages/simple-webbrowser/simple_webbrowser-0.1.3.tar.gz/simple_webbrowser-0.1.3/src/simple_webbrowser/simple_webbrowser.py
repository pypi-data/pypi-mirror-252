import webbrowser
from core import *

# [i] simple_webbrowser.py by MF366
# [*] Based on built-in module: webbrowser

def get(_using : str | None = None) -> webbrowser.BaseBrowser:
    return webbrowser.get(_using)
    
def Google(query: str):
    Website(BuildSearchURL('https://www.google.com/search?q=', query, "+"))

def Brave(query: str):
    Website(BuildSearchURL('https://search.brave.com/search?q=', query, "+"))
                
def Bing(query: str):
    Website(BuildSearchURL('https://www.bing.com/search?q=', query, "+"))
                
def Yahoo(query: str):
    Website(BuildSearchURL("https://search.yahoo.com/search?p=", query, "+"))
                
def DuckDuckGo(query: str):
    Website(BuildSearchURL("https://duckduckgo.com/?q=", query, "+"))
                
def YouTube(query: str):
    Website(BuildSearchURL("https://www.youtube.com/results?search_query=", query, "+"))
                
def Ecosia(query: str):
    Website(BuildSearchURL("https://www.ecosia.org/search?method=index&q=", query, "%20"))
        
def StackOverflow(query: str):
    Website(BuildSearchURL("https://stackoverflow.com/search?q=", query, "+"))
                
def SoundCloud(query: str):
    Website(BuildSearchURL("https://soundcloud.com/search?q=", query, "%20"))
                
def Archive(query: str):
    Website(BuildSearchURL("https://archive.org/search?query=", query, "+"))
                
def Qwant(query: str):
    Website(BuildSearchURL("https://www.qwant.com/?q=", query, "+"))
                
def SpotifyOnline(query: str):
    Website(BuildSearchURL("https://open.spotify.com/search/", query, "%20"))
    
def GitLab(query: str):
    Website(BuildSearchURL("https://gitlab.com/search?search=", query, "%20"))
    
def GitHub(query: str):
    Website(BuildSearchURL("https://github.com/search?q=", query, "+"))
