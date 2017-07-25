import curses
from math import ceil

def main_loop(screen, update_screen_function, need_update_function=None):

    update_screen_function()
    curses.halfdelay(40)
    while True:
        #http://stackoverflow.com/questions/28328982/using-curses-how-do-i-update-the-screen-or-wait-for-a-key
        inputchar = screen.getch()
        if inputchar != curses.ERR:
            #exit()
            pass
        else:
            if need_update_function is None or need_update_function():
                screen.clear()
                update_screen_function()

def write_on_screen(screen, sentence, start_row, attribute=curses.A_NORMAL, max_rows=None, max_width=-1):
    height,width = screen.getmaxyx()
    if max_width != -1: width = min(max_width, width)

    words = sentence.split()
    y = 0
    x = 0
    for word in words:
        if x+len(word) >= width:
            if (max_rows is not None) and (y+1 >= max_rows):
                screen.addstr(y+start_row, min(x+1, width-4), '...', attribute)
                return y+1
            y += 1
            x = 0
        if y+start_row >= height: return y+1
        screen.addstr(y+start_row, x, word, attribute)
        x += len(word) + 1
    return y+1

def write_on_screen_right(screen, sentence, start_row, attribute=curses.A_NORMAL):
    height,width = screen.getmaxyx()
    x = width - len(sentence) - 1
    if len(sentence) >= width:
        return 0
    if start_row >= height:
        return 0
    screen.addstr(start_row, x, sentence, attribute)
    return 0

def dividing_line_on_screen(screen, row):
    height, width = screen.getmaxyx()
    if row >= height: return 1
    screen.addstr(row,0,"-"*(width-1))
    return 1

def vertical_line_on_screen(screen, col):
    height, width = screen.getmaxyx()
    for y in range(height):
        screen.addstr(y, col, "|")
    return 0

def table_on_screen(screen, labels, rows):
    height, width = screen.getmaxyx()
    col_count = len(labels)
    col_widths = [max(*[len(row[i])+1 for row in rows],len(labels[i]))
                                                for i in range(col_count)]
    leftovers = width - sum(col_widths) - 1
    #grow or shrink columns based on the amount of extra space on the screen
    if leftovers > 0:
        col_widths = [w+int(leftovers/col_count) for w in col_widths]
    if leftovers < 0:
        col_widths = [w+int(ceil(leftovers/col_count)) for w in col_widths]

    col_start_x = [sum(col_widths[:i]) for i in range(len(col_widths))]

    for x in col_start_x[1:]:
        vertical_line_on_screen(screen, x-1)

    y = 0
    y += table_row_on_screen(screen, col_widths, labels, y, curses.A_BOLD)
    y += dividing_line_on_screen(screen, y)
    for row in rows:
        if y >= height: return y
        y += table_row_on_screen(screen, col_widths, row, y)

def table_row_on_screen(screen, col_widths, row, y, attribute=curses.A_NORMAL):
    col_start_x = [sum(col_widths[:i]) for i in range(len(row))]
    for x, col_width, row_value in zip(col_start_x, col_widths, row):
        screen.addstr(y, x, row_value[:col_width-1], attribute)
    return 1

if __name__ == "__main__":
    pass
