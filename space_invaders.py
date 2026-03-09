import curses
import time

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

    # Shields
    shields = [[sh-5, x] for x in range(5, sw-5, 10)]

    while True:
        stdscr.clear()

        # Draw ship
        stdscr.addstr(sh-2, ship_x, "^")

        # Draw bullets
        for b in bullets:
            if 0 <= b[0] < sh and 0 <= b[1] < sw:
                stdscr.addstr(b[0], b[1], "|")

        # Draw enemies
        for e in enemies:
            ex = min(e[1]*3, sw-2)
            ey = e[0]
            stdscr.addstr(ey, ex, "V")

        # Draw shields
        for s in shields:
            stdscr.addstr(s[0], s[1], "#")

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
            # Check collision with shields
            hit_shield = None
            for s in shields:
                if b[0] == s[0] and b[1] == s[1]:
                    hit_shield = s
                    break
            if hit_shield:
                shields.remove(hit_shield)
                continue
            # Check collision with enemies
            hit_enemy = None
            for e in enemies:
                ex = min(e[1]*3, sw-2)
                if b[0] == e[0] and b[1] == ex:
                    hit_enemy = e
                    break
            if hit_enemy:
                enemies.remove(hit_enemy)
                score += 1
                continue
            if b[0] > 0:
                new_bullets.append(b)
        bullets = new_bullets

        # Move enemies
        move_down = False
        for e in enemies:
            e[1] += enemy_direction
            if e[1]*3 >= sw-2 or e[1]*3 <= 0:
                move_down = True
        if move_down:
            enemy_direction *= -1
            for e in enemies:
                e[0] += 1

        # Check game over
        for e in enemies:
            if e[0] >= sh-2:
                stdscr.nodelay(False)
                stdscr.addstr(sh//2, max(0, sw//2-5), "GAME OVER")
                stdscr.refresh()
                stdscr.getch()
                return

        if not enemies:
            stdscr.nodelay(False)
            stdscr.addstr(sh//2, max(0, sw//2-5), "YOU WIN!")
            stdscr.refresh()
            stdscr.getch()
            return

        time.sleep(0.05)

curses.wrapper(main)
