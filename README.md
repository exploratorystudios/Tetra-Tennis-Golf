# Tetra Tennis Golf 🎾🧩⛳

> *Tetris. But smaller. But also somehow bigger.*

---

ok so picture this: someone looked at Tetris — a game that already exists, works fine, brings joy to millions — and said "what if it was one function. what if the whole thing was one lambda. what if `__import__` showed up six times and that felt *normal*." that someone was me. this is that thing.

i'm not gonna pretend this is readable. it's not. it's a cognitive sketch of Tetris made manifest in Python, and it looks like someone asked a court jester to transcribe a falling-blocks game using only vibes and list comprehensions.

---

## What Even Is This

It's Tetris. Full Tetris. In your terminal. With:

- **Hold** (`C` key) — because constraints breed creativity and i genuinely needed hold
- **Hard drop** (Space) — slam those pieces down like you have somewhere to be
- **Ghost piece** — so you can see where your mistakes are about to land
- **Rotation** — yes, real rotation, in a code golf entry, i'm as surprised as you are
- **Score** — it goes up. you feel good. briefly.
- **Next piece preview** — NEXT, displayed in glorious curses color
- **Cross-platform input** — works on Windows (`msvcrt`), Linux with Xlib, and falls back to raw curses getch if you're in a vim-brained no-display environment

the whole thing runs in one function called `g`. there's a reason it's called `g`. it's short. everything here is short. that's the point.

---

## How To Run It

```bash
python tetra_tennis_golf.py
```

you'll need a terminal big enough to hold a 10-wide board. if your terminal is tiny, that's a you problem and also a physics problem.

**On Linux**, install `xlib` for proper key detection:
```bash
pip install xlib
```

without it you get curses fallback input which is fine, just a little vibe-based.

**On Windows**, it uses `msvcrt` and `ctypes`. it just works. windows moment.

---

## Controls

| Key | Action |
|-----|--------|
| ← → | Move |
| ↑ | Rotate |
| ↓ | Soft drop |
| Space | Hard drop |
| C | Hold piece |

---

## Architecture (lol)

ok so the whole game is structured like this:

```
one function
  → one lambda for input handling
      → three different input backends depending on your OS and what libs are installed
  → one lambda for collision detection
  → one giant `next(...)` expression that handles movement, hold, hard drop, and piece spawning simultaneously
  → one unholy `or`-chain that draws the entire board in a single expression
  → curses wrapper
```

the board stores two rows per visual row because the rendering uses `▄` `▀` `█` unicode half-block characters to pack twice the resolution into terminal cells. is this necessary. no. does it look extremely good. yes.

i find meaning in constraints. this codebase *is* constraints. it's constraints all the way down.

---

## Why "Tetra Tennis Golf"

"Tetris" is trademarked. "Code Golf" describes what this is. "Tennis" is there because it has the right vibe and i needed something between Tetra and Golf. also if you stare at the lambda on line 1 long enough it starts to look like a tennis racket. that's not true. but now you'll look.

---

## Known Issues

- If your terminal is too small it just crashes. this is intentional in the sense that i didn't fix it.
- The scoring system is `lines_cleared_total` not the standard Tetris scoring. it's fine. you're not speedrunning this.
- There's no pause. life has no pause button either.

---

## Requirements

- Python 3.8+
- A terminal with color support
- `windows-curses` if you're on Windows (`pip install windows-curses`)
- `xlib` if you're on Linux and want arrow keys to work properly
- The emotional bandwidth to look at a 60-line single-function Tetris and feel something

---

*false life. made manifest. in curses.*
