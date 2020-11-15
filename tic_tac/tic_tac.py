
import random


player_move = {
    1: 8,
    2: 10,
    3: 12,
    4: 15,
    5: 17,
    6: 19,
    7: 22,
    8: 24,
    9: 26,
}


def tics():
    tics = []
    tics += [' ']
    tics += ['_']*5
    tics += [' ']
    tics += ['|', '_', '|', '_', '|', '_', '|']*3
    return tics


def tic_view(list):
    view_string = ''
    for col in range(1, 6):
        view = [list[i:i + 7] for i in range(7 * (col -1), (7 * col) -1, 7)]
        view_string += '%s%s' % ('\n\t', ''.join(view[0]))
    return view_string


def opponent(loc, mark, view):
    spots = [x for x in range(len(view)) if view[x] == '_']
    # spots[5:] is not ideal, but it works
    return random.choice(spots[5:])


def check_win(mark, oppo, view):
    player_spots = [x for x in range(len(view)) if view[x] == mark]
    opponent_spots = [x for x in range(len(view)) if view[x] == oppo]
    winning_spots = [
        [8, 10, 12],
        [15, 17, 19],
        [22, 24, 26],
        [8, 15, 22],
        [10, 17, 24],
        [12, 19, 26],
        [8, 17, 26],
        [12, 17, 22],
    ]
    win = []
    lose = []
    for conf in winning_spots:
        win.append(all(elem in player_spots for elem in conf))
        lose.append(all(elem in opponent_spots for elem in conf))
    return win, lose


def main():
    while True:
        tic_tac = tics()
        print("Choose X or O")
        mark = input()
        if mark not in ['x', 'X', 'o', 'O']:
            print("Invalid mark, please choose again")
            continue
        break
    mark = mark.upper()
    if mark in ['x', 'X']:
        oppo = 'O'
    else:
        oppo = 'X'
    while True:
        print(tic_view(tic_tac))
        print("Where should the mark go?")
        print("Choose from the numbers: 1, 2, 3, 4, 5, 6, 7, 8, 9")
        loc = int(input())
        if loc not in range(1, 10):
            print("Choose proper number")
            continue
        if tic_tac[player_move[loc]] != '_':
            print("Mark exists on this spot. Try again")
            continue

        tic_tac[player_move[loc]] = mark

        check_spots = [x for x in range(len(tic_tac)) if tic_tac[x] == '_']
        if not check_spots[5:]:
            print("Game over")
            break

        oppo_move = opponent(loc, oppo, tic_tac)
        tic_tac[oppo_move] = oppo

        win, lose = check_win(mark, oppo, tic_tac)
        if True in win:
            print(tic_view(tic_tac))
            print("You win!")
            break
        if True in lose:
            print(tic_view(tic_tac))
            print("You have lost")
            break


main()
