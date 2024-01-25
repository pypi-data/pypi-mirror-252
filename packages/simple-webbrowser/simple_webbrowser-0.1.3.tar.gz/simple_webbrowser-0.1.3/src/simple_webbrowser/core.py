import webbrowser
from typing import Literal, Callable, Any

def Website(url: str, new: Literal[0, 1, 2] = 0, autoraise: bool = True, browser: webbrowser.BaseBrowser | Callable | Any = webbrowser) -> bool:        
    return browser.open(url, new, autoraise)

def BuildSearchURL(common: str, query: str, spacebar_rule: Literal["%20", "+"]) -> str:
    """
    BuildSearchURL allows you to set rules to search on any website

    Args:
        common (str): the part of the URL that never changes
        query (str): the search query
        spacebar_rule (either '%20' or '+'): the way the search engine handles SPACEBAR buy replacing it by something else (the value of this argument)
    """
    return f"{common}{query.replace(' ', spacebar_rule)}"