import re
import jericho


def _clean(text: str) -> str:
    """Collapse excessive blank lines and trim whitespace."""
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


class JerichoGame:
    """Wraps a jericho.FrotzEnv session for interactive fiction play.

    Usage:
        game = JerichoGame("/path/to/game.z8")
        intro = game.read()           # opening text
        obs   = game.send("look")     # send a command, get response text
        game.close()                  # shut down the environment

    After each send(), updated state is available as:
        game.score   — current score
        game.moves   — move count
        game.done    — True if the game has ended
    """

    def __init__(self, path: str):
        self._env = jericho.FrotzEnv(path)
        obs, info = self._env.reset()
        self._opening = _clean(obs)
        self.score: int = info.get("score", 0)
        self.moves: int = info.get("moves", 0)
        self.done: bool = False

    def read(self) -> str:
        """Return the game's opening text (call once after __init__)."""
        return self._opening

    def send(self, command: str) -> str:
        """Send a command and return the game's response."""
        obs, _reward, self.done, info = self._env.step(command)
        self.score = info.get("score", 0)
        self.moves = info.get("moves", 0)
        return _clean(obs)

    def close(self):
        """Shut down the Frotz environment."""
        try:
            self._env.close()
        except Exception:
            pass
