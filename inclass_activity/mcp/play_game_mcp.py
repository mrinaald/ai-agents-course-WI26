import json
import os
from mcp.server.fastmcp import FastMCP
from jericho_game import JerichoGame

mcp = FastMCP("play_game_mcp")

# Global game session — shared across tool calls
_game: JerichoGame | None = None


@mcp.tool()
def load_game(game_path: str) -> str:
    """Load the game file and return the opening text."""
    global _game

    if not os.path.isfile(game_path):
        return f"File not found: {game_path}"

    try:
        if _game is not None:
            _game.close()

        _game = JerichoGame(game_path)
        obs = _game.read()
        return json.dumps({"observation": obs, "score": _game.score, "moves": _game.moves}, indent=2)

    except Exception as e:
        return f"Failed to load game: {e}"


@mcp.tool()
def send_command(command: str) -> str:
    """Send a command to the game (e.g. 'look', 'go north', 'take lamp')."""
    if _game is None:
        return "No game loaded. Use 'load_game' first."

    # TODO: Send the command to the current game session. See `send` in JerichoGame.
    # TODO: Return a JSON string with observation, score, moves, and done flag
    pass


if __name__ == "__main__":
    mcp.run()
