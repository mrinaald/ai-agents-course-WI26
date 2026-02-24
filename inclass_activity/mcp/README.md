# Build an MCP Server

## Overview

In this assignment, you will build a simple **MCP (Model Context Protocol) server** that exposes tools an LLM can call.
The tool scrapes the games from [IFDB (the Interactive Fiction Database)](https://ifdb.org) and returns its title, author, and download links for its `.gblorb` game file.

## Prerequisites

We will test your local MCP server with either 1) Claude Desktop or 2) Cursor.
Before class, make sure you have one of the following installed:
- [Claude Desktop](https://claude.ai/download) (free account required)
- [Cursor](https://www.cursor.com)

Also install the required Python packages:

```bash
# Python 3.10 or higher
pip install httpx beautifulsoup4 jericho
```

## What You'll Build

A working MCP server on your laptop.

We will make three tools: `get_top_rated_game`, `get_most_rated_game`, and `get_game_by_title`.

### Tool 1: `get_top_rated_game`
Returns the highest-rated game on IFDB.

```json
{
  "title": "Counterfeit Monkey",
  "author": "Emily Short",
  "average_rating": 4.826,
  "num_ratings": 282,
  "gblorb_urls": [
    "https://github.com/i7/counterfeit-monkey/releases/download/r11.1/CounterfeitMonkey-11.gblorb",
    "https://ifarchive.org/if-archive/games/glulx/CounterfeitMonkey.gblorb",
    ...,
  ]
}
```

### Tool 2: `get_most_rated_game`
Returns the game with the **highest number of ratings** — i.e. the most reviewed game on IFDB.

```json
{
  "title": "Photopia",
  "author": "Adam Cadre",
  "average_rating": 4.262435677,
  "num_ratings": 583,
  "gblorb_urls": [
    ...,
  ]
}
```

### Tool 3: `get_game_by_title`
Searches IFDB by title and returns the best-matching game with its download links.

```json
{
  "title": "Anchorhead",
  "author": "Michael Gentry",
  "average_rating": 4.638954869,
  "num_ratings": 421,
  "download_urls": [
    "https://ifarchive.org/if-archive/games/zcode/anchor.z8",
    "https://ifarchive.org/if-archive/games/glulx/AnchorheadDemo.gblorb"
  ]
}
```

## TO DO 1: Implement MCP tools

Complete three MCP tool functions in `ifdb_mcp.py`.

Tip: Rather than scraping HTML, use IFDB's official JSON API:

```python
response = httpx.get(
    "https://ifdb.org/search",
    # `searchfor` is a query filter (`#ratings:1-`:  all games with at least 1 rating)
    params={"json": "1", "game": "1", "searchfor": "#ratings:1-"}, 
    follow_redirects=True
)
data = response.json()
```

The API returns a JSON object with a `"games"` list.
Each game has fields including `tuid`, `title`, `author`, `averageRating`, `numRatings`, and `starSort`.


## Test Your Server

After completing TO DOs in `ifdb_mcp.py`, test the scraping logic on its own:

```bash
python test_ifdb.py
```

Now, let's wire up your MCP server with an agent.


### Option 1: Claude Desktop (free account required)

If you have Claude Desktop installed, you can connect your server to it by editing the MCP config file. 

**Settings → Developer → Edit Config**

Add the following (replace the path with your local python/file path):

```json
{
  "mcpServers": {
    "ifdb-tool": {
      "command": "/your/python/path",
      "args": ["/absolute/path/to/ifdb_mcp.py"]
    }
  }
}
```

> **Q. How to find the Python path:** run this in a terminal and copy the output to the `command` field: `python -c "import sys; print(sys.executable)"`

Then, restart Claude Desktop and check your tool is successfully registered at **Settings → Developer → Edit Config**. It should show a blue `running` tag next to the tool name.

Try asking on chat: *"What's the top game on IFDB and where can I download it?"*


### Option 2: Cursor

---

**Step 1:** Add your server to Cursor's MCP config

Go to **Settings → Cursor Settings → Tools & MCP → Add a Custom MCP server**.

Paste this into `mcp.json` (replace the path with your local python/file path):

```json
{
  "mcpServers": {
    "ifdb-tool": {
      "command": "/your/python/path",
      "args": ["/absolute/path/to/ifdb_mcp.py"]
    }
  }
}
```

> **Q. How to find the Python path:** run this in a terminal and copy the output to the `command` field: `python -c "import sys; print(sys.executable)"`

Save the file and confirm your server shows up with a green dot and lists `get_top_rated_game`, `get_most_rated_game` and `get_game_by_title` as available tools.

---

**Step 2:** Call the tools

Switch Cursor's chat mode to **Agent** — MCP tools are only available in Agent mode, not regular chat.

Try asking: *"What's the top game on IFDB and where can I download it?"*
(Cursor will ask for your approval before running the tool.)

## TO DO 2: Test `get_most_rated_game` tool

Come up with a question to make the agent call `get_most_rated_game`. Save a screenshot of the agent's response.

## TO DO 3: Play Game

Now let's play the game *Anchorhead* with the agent! 

Try asking: *"Find the game Anchorhead on IFDB and tell me where to download it."* This will let the agent call the `get_game_by_title` function and will show the donwload links. 

Download `anchor.z8` file using the link from the response (or just let your agent download the file instead). We will implement a simple tool that plays the game using the local `anchor.z8` file.

A second MCP server, `play_game_mcp.py`, exposes two tools for playing a Z-machine game via Jericho:

- `load_game(game_path)` — already implemented for you
- `send_command(command)` — **TO DO**

**Step 1:** Open `play_game_mcp.py` and implement `send_command`. Follow the TODO comments inside.

Test your code before registering the server:
```bash
python test_play_game.py /your/path/to/anchor.z8
```


**Step 2:** Register `play_game_mcp.py` as a second MCP server alongside `ifdb-tool`:

```json
{
  "mcpServers": {
    "ifdb-tool": {
      "command": "/your/python/path",
      "args": ["/absolute/path/to/ifdb_mcp.py"]
    },
    "play-game-tool": {
      "command": "/your/python/path",
      "args": ["/absolute/path/to/play_game_mcp.py"]
    }
  }
}
```

**Step 3:** Ask the agent to play the game:

> *"Load the Anchorhead game from `/your/path/to/anchor.z8` and play"*

Try a few moves of `Anchorhead` and screenshot the responses.

## Submission

Submit 1) `ifdb_mcp.py` and 2) `play_game_mcp.py`, plus three screenshots to Gradescope:

3) Agent's response when asking *"What's the top-rated interactive fiction game on IFDB?"*
4) Make the agent use `get_most_rated_game` tool, and screenshot the response.
5) Agent playing a few moves of Anchorhead.


## Resources

- [MCP Build a Server Guide](https://modelcontextprotocol.io/docs/develop/build-server)
- [FastMCP Docs](https://github.com/jlowin/fastmcp)
