"""
Manual test for play_game_mcp tools.
Run: python test_play_game.py /path/to/anchor.z8
"""
import sys
sys.path.insert(0, ".")

if len(sys.argv) < 2:
    print("Usage: python test_play_game.py /path/to/anchor.z8")
    sys.exit(1)

GAME = sys.argv[1]

import play_game_mcp as g

def section(title):
    print(f"\n{'='*50}")
    print(f"  {title}")
    print('='*50)

# --- Error cases ---
section("send_command with no game loaded")
result = g.send_command("look")
print(result)
assert result == "No game loaded. Use 'load_game' first.", f"Unexpected: {result}"
print("PASS")

section("load_game with bad path")
result = g.load_game("/nonexistent/path.z8")
print(result)
assert "File not found" in result, f"Unexpected: {result}"
print("PASS")

section("load_game (Anchorhead)")
result = g.load_game(GAME)
print(result)
assert "observation" in result, f"Missing 'observation': {result}"
assert "ANCHORHEAD" in result.upper(), f"Unexpected intro: {result}"
assert "score" in result
assert "moves" in result
print("PASS")

section("send_command: look")
result = g.send_command("look")
print(result)
assert "observation" in result
assert "score" in result
assert "moves" in result
assert "done" in result
print("PASS")

section("send_command: go north")
result = g.send_command("go north")
print(result)
assert "observation" in result
print("PASS")

if g._game:
    g._game.close()

print("\n\nAll tests passed.")
