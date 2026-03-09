import curses
import time
import random

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    sh, sw = stdscr.getmaxyx()
    ship_x = sw // 2
    bullets = []
    enemies = [[i, j] for i in range(5) for j in range(10)]
    enemy_direction = 1
    score = 0

    while True:
        stdscr.clear()

        # Draw ship
        stdscr.addstr(sh-2, ship_x, "^")

        # Draw bullets
        for b in bullets:
            stdscr.addstr(b[0], b[1], "|")

        # Draw enemies
        for e in enemies:
            stdscr.addstr(e[0], e[1]*3, "V")  # spacing enemies

        stdscr.addstr(0, 2, f"Score: {score}")

        stdscr.refresh()

        # Input
        key = stdscr.getch()
        if key == curses.KEY_LEFT and ship_x > 0:
            ship_x -= 2
        elif key == curses.KEY_RIGHT and ship_x < sw-1:
            ship_x += 2
        elif key == ord(" "):
            bullets.append([sh-3, ship_x])

        # Move bullets
        new_bullets = []
        for b in bullets:
            b[0] -= 1
            if b[0] > 0:
                new_bullets.append(b)
        bullets = new_bullets

        # Move enemies
        move_down = False
        for e in enemies:
            e[1] += enemy_direction
            if e[1]*3 >= sw-1 or e[1]*3 <= 0:
                move_down = True
        if move_down:
            enemy_direction *= -1
            for e in enemies:
                e[0] += 1

        # Collision detection
        new_enemies = []
        for e in enemies:
            hit = False
            for b in bullets:
                if b[0] == e[0] and b[1] == e[1]*3:
                    score += 1
                    bullets.remove(b)
                    hit = True
                    break
            if not hit:
                new_enemies.append(e)
        enemies = new_enemies

        # Check game over
        for e in enemies:
            if e[0] >= sh-2:
                stdscr.nodelay(False)
                stdscr.addstr(sh//2, sw//2-5, "GAME OVER")
                stdscr.refresh()
                stdscr.getch()
                return

        if not enemies:
            stdscr.nodelay(False)
            stdscr.addstr(sh//2, sw//2-5, "YOU WIN!")
            stdscr.refresh()
            stdscr.getch()
            return

        time.sleep(0.05)

curses.wrapper(main)
