# Write your code here
import random
random.seed(0)


def generator(te_genereren=28):
    dominoes = []

    while len(dominoes) != te_genereren:
        number1 = random.randint(0, 6)
        number2 = random.randint(0, 6)
        domino = [number1, number2]

        if domino not in dominoes and [number2, number1] not in dominoes:
            dominoes.append(domino)

    return dominoes

def split(dominoes):
    stock = dominoes[:14]
    rest = dominoes[14:]

    computer = rest[:7]
    player = rest[7:]

    return stock, computer, player


def duplitas(dominoes):
    duplicates = [domino for domino in dominoes if domino[0] == domino[1]]

    while len(duplicates) == 0:
        duplicates = [domino for domino in generator(28) if domino[0] == domino[1]]

    return max(duplicates)

def show_your_pieces(dominoes):
    string = "Your pieces:\n"

    for i, domino in enumerate(dominoes):
        if i+1 == 1:
            string += f"{i+1}:{domino}"
        else:
            string += f"\n{i+1}:{domino}"

    return string


def if_move_0(dominoes):
    choice = random.choice(stock)
    stock.remove(choice)
    dominoes.append(choice)

def speel_een_zet(naar_waar, mijn_dominoes):
    mijn_piece = mijn_dominoes[abs(naar_waar)-1]

    if naar_waar == 0:
        mijn_dominoes.append(if_move_0(mijn_dominoes))
    elif naar_waar < 0:
        if mijn_piece[0] == snake[0][0]:
            mijn_piece = mijn_piece[::-1]

        snake.insert(0, mijn_piece)
    else:
        if mijn_piece[-1] == snake[-1][-1]:
            mijn_piece = mijn_piece[::-1]

        snake.append(mijn_piece)

    mijn_dominoes.pop(abs(naar_waar)-1)


class StockIsEmpty(Exception):
    pass


def get_valid_move_player(player_dominoes):
    while True:
        try:
            move = int(input(f"{status}\n"))
            assert -len(player_dominoes) <= move <= len(player_dominoes)
        except (ValueError, AssertionError):
            print("Invalid input. Please try again.")
            continue

        min_eraf = abs(move)

        mijn_piece = player_dominoes[min_eraf-1]

        if move > 0 and snake[-1][-1] in mijn_piece:
            return move
        elif move == 0 and len(stock) != 0:
            return move
        elif move < 0 and snake[0][0] in mijn_piece:
            return move

        print("Illegal move. Please try again.")
        print('')

def can_i_place_at_left_side(domino):
    if snake[0][0] in domino:
        return True
    return False

def can_i_place_at_right_side(domino):
    if snake[-1][-1] in domino:
        return True
    return False


def test_can_i_place_at_right_side():
    global snake
    snake = [[3, 4], [4, 4], [4, 2]]

    assert can_i_place_at_right_side([2, 1]) is True
    assert can_i_place_at_right_side([1, 2]) is True
    assert can_i_place_at_right_side([3, 3]) is False

# test_can_i_place_at_right_side()

def get_valid_move_computer(computer_dominoes):
    print(status)
    input('')

    for index, mijn_piece in enumerate(computer_dominoes):
        index += 1

        if can_i_place_at_left_side(mijn_piece):
            return int(str(-index))
        elif can_i_place_at_right_side(mijn_piece):
            return index

    return 0

def test_get_valid_move_computer():
    global snake
    snake = [[3, 4], [4, 4], [4, 2]]

    assert get_valid_move_computer([[2, 1], [4, 3], [5, 5]]) == 1
    assert get_valid_move_computer([[1, 2], [4, 2], [1, 3]]) == 1
    assert get_valid_move_computer([[3, 3], [2, 3], [6, 3]]) == -1
    assert get_valid_move_computer([[6, 6]]) == 0

# test_get_valid_move_computer()

#---------------------------------------------------------------------------------------------------------

dominoes = generator()
stock, computer, player = split(dominoes)
player1 = duplitas(player)
computer1 = duplitas(computer)
snake = []
biggest_domino = max(player1, computer1)
snake.append(biggest_domino)

if biggest_domino == player1:
    wie_aan_de_beurt = "computer"
    status = "Status: Computer is about to make a move. Press Enter to continue..."
    player.remove(biggest_domino)
else:
    wie_aan_de_beurt = "player"
    status = "Status: It's your turn to make a move. Enter your command."
    computer.remove(biggest_domino)

while True:
    print("======================================================================")
    print(f"Stock size: {len(stock)}")
    print(f"Computer pieces: {len(computer)}\n")

    snake_to_print = None
    if len(snake) < 7:
        snake_to_print = snake
    else:
        snake_to_print = snake[:3]+['...']+snake[-3:]
    print("".join(str(s) for s in snake_to_print))
    print('')

    print(f"{show_your_pieces(player)}\n")


    if wie_aan_de_beurt == "player" and len(player) != 0:
        move = get_valid_move_player(player)

        speel_een_zet(naar_waar=move, mijn_dominoes=player)


        status = "Status: Computer is about to make a move. Press Enter to continue..."
        wie_aan_de_beurt = "computer"
    elif wie_aan_de_beurt == "computer" and len(computer) != 0:
        move = get_valid_move_computer(computer)

        if move == 0:
            if_move_0(computer)

            continue

        speel_een_zet(naar_waar=move, mijn_dominoes=computer)

        status = "Status: It's your turn to make a move. Enter your command."
        wie_aan_de_beurt = "player"
    else:
        break


if len(player) == 0:
    print("Status: The game is over. You won!")
elif len(computer) == 0:
    print("Status: The game is over. The computer won!")
else:
    print("Status: The game is over. It's a draw!")