import curses
import os
import random
import time

# ------------------------------------------------------------
# Platform-independent input handling
# ------------------------------------------------------------

def make_input_handler(stdscr):
    """
    Returns a function that polls the keyboard and returns:
    (last_horizontal_key, current_key)
    """

    # State: currently pressed keys, last horizontal direction
    state = {
        "pressed": set(),
        "last_dir": -1,
    }

    if os.name == "nt":
        import msvcrt
        import ctypes

        GetAsyncKeyState = ctypes.windll.user32.GetAsyncKeyState

        KEYMAP = {
            b'K': curses.KEY_LEFT,
            b'M': curses.KEY_RIGHT,
            b'H': curses.KEY_UP,
            b'P': curses.KEY_DOWN,
            b' ': ord(' '),
            b'c': ord('c'),
        }

        def poll():
            pressed = set()

            # async arrows
            if GetAsyncKeyState(0x25) & 0x8000:
                pressed.add(curses.KEY_LEFT)
            if GetAsyncKeyState(0x27) & 0x8000:
                pressed.add(curses.KEY_RIGHT)
            if GetAsyncKeyState(0x26) & 0x8000:
                pressed.add(curses.KEY_UP)
            if GetAsyncKeyState(0x28) & 0x8000:
                pressed.add(curses.KEY_DOWN)

            # buffered input
            while msvcrt.kbhit():
                ch = msvcrt.getch()
                if ch in (b'\xe0', b'\x00'):
                    ch = msvcrt.getch()
                pressed.add(KEYMAP.get(ch, -1))

            return pressed

    else:
        try:
            from Xlib.display import Display
            d = Display()

            def poll():
                pressed = set()
                keymap = d.query_keymap()
                for sym, key in zip(
                    [curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_UP,
                     curses.KEY_DOWN, ord(' '), ord('c')],
                    [0xff51, 0xff53, 0xff52, 0xff54, 0x20, 0x63]
                ):
                    code = d.keysym_to_keycode(key)
                    if keymap[code >> 3] & (1 << (code & 7)):
                        pressed.add(sym)
                while True:
                    ch = stdscr.getch()
                    if ch == -1:
                        break
                    pressed.add(ch)
                return pressed

        except ImportError:
            def poll():
                pressed = set()
                while True:
                    ch = stdscr.getch()
                    if ch == -1:
                        break
                    pressed.add(ch)
                return pressed

    def handler(stdscr):
        current = poll()

        last_dir = state["last_dir"]

        # horizontal direction logic
        if curses.KEY_LEFT in current and last_dir != curses.KEY_LEFT:
            last_dir = curses.KEY_LEFT
        elif curses.KEY_RIGHT in current and last_dir != curses.KEY_RIGHT:
            last_dir = curses.KEY_RIGHT
        elif last_dir not in current:
            last_dir = -1

        state["pressed"] = current
        state["last_dir"] = last_dir

        # choose a "main" key
        key = -1
        for k in (curses.KEY_UP, ord(' '), ord('c')):
            if k in current:
                key = k
                break
        if key == -1 and curses.KEY_DOWN in current:
            key = curses.KEY_DOWN

        return last_dir, key

    return handler

# ------------------------------------------------------------
# Game logic
# ------------------------------------------------------------

def game(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.start_color()
    curses.use_default_colors()

    # colors
    for i, c in enumerate([51, 27, 208, 226, 46, 196, 201]):
        curses.init_pair(i + 1, c, -1)

    H = 40
    W = 10
    board_x = stdscr.getmaxyx()[1] // 2 - 10

    board = [[0] * W for _ in range(H + 2)]

    PIECES = [
        [15, 4369],                    # I
        [113, 275, 71, 802],            # T
        [116, 785, 23, 547],            # Z
        [51],                           # O
        [54, 561],                     # S
        [39, 562, 114, 305],            # J
        [99, 306],                     # L
    ]

    def cells(mask):
        for r in range(4):
            for c in range(4):
                if mask >> (r * 4 + c) & 1:
                    yield r, c

    def collides(mask, x, y):
        for r, c in cells(mask):
            for dy in (0, 1):
                ny = y + r * 2 + dy
                nx = x + c
                if ny >= H or nx < 0 or nx >= W:
                    return True
                if board[ny][nx]:
                    return True
        return False

    input_handler = make_input_handler(stdscr)

    piece_index = random.randint(0, 6)
    next_piece = random.randint(0, 6)
    hold_piece = -1

    rotation = 0
    x, y = 3, 0
    score = 0
    tick = 0
    used_hold = False

    mask = PIECES[piece_index][rotation]

    while True:
        last_dir, key = input_handler(stdscr)

        y_aligned = y & ~1

        # horizontal move
        if last_dir == curses.KEY_LEFT and not collides(mask, x - 1, y_aligned):
            x -= 1
        elif last_dir == curses.KEY_RIGHT and not collides(mask, x + 1, y_aligned):
            x += 1

        # rotate
        if key == curses.KEY_UP:
            new_rot = (rotation + 1) % len(PIECES[piece_index])
            new_mask = PIECES[piece_index][new_rot]
            if not collides(new_mask, x, y_aligned):
                rotation = new_rot
                mask = new_mask

        # hold
        if key == ord('c') and not used_hold:
            used_hold = True
            if hold_piece == -1:
                hold_piece = piece_index
                piece_index = next_piece
                next_piece = random.randint(0, 6)
            else:
                hold_piece, piece_index = piece_index, hold_piece
            rotation = 0
            mask = PIECES[piece_index][0]
            x, y = 3, 0

        # gravity
        speed = max(1, 10 - score // 10)
        if key in (curses.KEY_DOWN, ord(' ')) or tick % speed == 0:
            if collides(mask, x, y_aligned + 2):
                # lock piece
                for r, c in cells(mask):
                    for dy in (0, 1):
                        ny = y_aligned + r * 2 + dy
                        nx = x + c
                        if 0 <= ny < H:
                            board[ny][nx] = piece_index + 1

                # clear lines
                cleared = 0
                new_board = []
                for row in range(0, H, 2):
                    if all(board[row]) and all(board[row + 1]):
                        cleared += 1
                    else:
                        new_board.append(board[row])
                        new_board.append(board[row + 1])

                for _ in range(cleared * 2):
                    new_board.insert(0, [0] * W)

                board[:] = new_board[:H]
                score += cleared

                # spawn next
                piece_index = next_piece
                next_piece = random.randint(0, 6)
                rotation = 0
                mask = PIECES[piece_index][0]
                x, y = 3, 0
                used_hold = False

                if collides(mask, x, 0):
                    stdscr.addstr(10, board_x + 6, "GAME OVER")
                    stdscr.refresh()
                    time.sleep(2)
                    return
            else:
                y += 2 if key == curses.KEY_DOWN else 1

        # render
        stdscr.erase()

        stdscr.addstr(0, board_x, "╔" + "═" * (W * 2) + "╗", curses.A_REVERSE)
        stdscr.addstr(H // 2 + 1, board_x, "╚" + "═" * (W * 2) + "╝", curses.A_REVERSE)
        stdscr.addstr(0, board_x + 1, f"Score:{score}", curses.A_REVERSE)

        # draw board and piece
        ghost_y = next(i for i in range(y_aligned, H, 2) if collides(mask, x, i + 2))

        ghost_cells = {
            (ghost_y + r * 2 + dy, x + c)
            for r, c in cells(mask)
            for dy in (0, 1)
        }

        live_cells = {
            (y + r * 2 + dy, x + c)
            for r, c in cells(mask)
            for dy in (0, 1)
        }

        for r in range(H // 2):
            stdscr.addstr(r + 1, board_x, "║", curses.A_REVERSE)
            stdscr.addstr(r + 1, board_x + W * 2 + 1, "║", curses.A_REVERSE)

            for c in range(W):
                top = (r * 2, c)
                bot = (r * 2 + 1, c)

                if top in live_cells or bot in live_cells:
                    color = curses.color_pair(piece_index + 1)
                    ch = "██"
                elif top in ghost_cells or bot in ghost_cells:
                    color = curses.color_pair(piece_index + 1)
                    ch = "▒▒"
                elif board[top[0]][c] or board[bot[0]][c]:
                    color = curses.color_pair(board[top[0]][c] or board[bot[0]][c])
                    ch = "██"
                else:
                    color = 0
                    ch = "  "

                stdscr.addstr(r + 1, board_x + c * 2 + 1, ch, color)

        stdscr.refresh()
        tick += 1
        curses.napms(99)

# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------

curses.wrapper(game)
