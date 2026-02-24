from mcp.server.fastmcp import FastMCP
import httpx
from bs4 import BeautifulSoup
import json

mcp = FastMCP("ifdb-tool")

BASE_URL = "https://ifdb.org"


def get_gblorb_links(game_id: str) -> list[str]:
    """Helper: fetch the game page and return all .gblorb download URLs."""
    page = httpx.get(f"{BASE_URL}/viewgame?id={game_id}", follow_redirects=True)
    soup = BeautifulSoup(page.text, "html.parser")
    return [
        a["href"] for a in soup.find_all("a", href=True)
        if a["href"].endswith(".gblorb")
    ]


PLAYABLE_EXTENSIONS = (".z5", ".z8", ".zblorb", ".gblorb", ".ulx")

def get_download_links(game_id: str) -> list[str]:
    """Helper: fetch the game page and return all playable download URLs (deduplicated)."""
    page = httpx.get(f"{BASE_URL}/viewgame?id={game_id}", follow_redirects=True)
    soup = BeautifulSoup(page.text, "html.parser")
    seen = set()
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.endswith(PLAYABLE_EXTENSIONS) and "iplayif.com" not in href and href not in seen:
            seen.add(href)
            links.append(href)
    return links


@mcp.tool()
def get_top_rated_game() -> str:
    """Get the top-rated game on IFDB, including its gblorb download links."""

    # TODO: Call the IFDB JSON API and read data["games"]
    # TODO: Sort the game list by game["starSort"] (descending) and pick the first game.
    # TODO: Call get_gblorb_links() with the game's tuid
    # TODO: Return a JSON string (use json.dumps) with title, author, average_rating, num_ratings, gblorb_urls:
    #     {
    #       "title": <string>,            # from game["title"]
    #       "author": <string>,           # from game["author"]
    #       "average_rating": <float>,    # from game["averageRating"]
    #       "num_ratings": <int>,         # from game["numRatings"]
    #       "gblorb_urls": [<string>, ...]# list of download URLs
    #     }

    pass


@mcp.tool()
def get_most_rated_game() -> str:
    """Get the most-rated game on IFDB (highest number of ratings), including its gblorb download links."""

    # TODO: Call the IFDB JSON API and read data["games"]
    # TODO: Sort the game list by game["numRatings"] (descending) and pick the first game.
    # TODO: Call get_gblorb_links() with the game's tuid
    # TODO: Return a JSON string (use json.dumps) with title, author, average_rating, num_ratings, gblorb_urls:
    #     {
    #       "title": <string>,            # from game["title"]
    #       "author": <string>,           # from game["author"]
    #       "average_rating": <float>,    # from game["averageRating"]
    #       "num_ratings": <int>,         # from game["numRatings"]
    #       "gblorb_urls": [<string>, ...]# list of download URLs
    #     }
    pass


@mcp.tool()
def get_game_by_title(title: str) -> str:
    """Search IFDB by title and return the best-matching game with its download links."""

    # TODO: Call the IFDB JSON API with params={"json": "1", "game": "1", "searchfor": title}.
    # TODO: Take the first game in data["games"] (results are already sorted by relevance).
    # TODO: Call `get_download_links()` with the game's tuid
    # TODO: Return a JSON string (use json.dumps) with title, author, average_rating, num_ratings, download_urls:
    #     {
    #       "title": <string>,             # from game["title"]
    #       "author": <string>,            # from game["author"]
    #       "average_rating": <float>,     # from game["averageRating"]
    #       "num_ratings": <int>,          # from game["numRatings"]
    #       "download_urls": [<string>, ...] # list of download URLs
    #     }
    pass


if __name__ == "__main__":
    mcp.run(transport="stdio")
