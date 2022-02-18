import random


def domino_stock():
    Dominos = list()
    for upper_pips in range(7):
        for lower_pips in range(7):
            # check if the domino is in the list: (a, b) and (b, a) both order.
            if ([lower_pips, upper_pips] not in Dominos
                and [upper_pips, lower_pips] not in Dominos):
                Dominos.append([upper_pips, lower_pips])
    return Dominos

def distribute_pieces(Dominos):
    # Distribute 7 domino each to two player
    player1 = random.sample(Dominos, 7)
    Dominos = [domino for domino in Dominos if domino not in player1]

    player2 = random.sample(Dominos, 7)
    Dominos = [domino for domino in Dominos if domino not in player2]
    return player1, player2, Dominos


def doublets_domino(computer_pieces, player_pieces):
    # loop through all the piece in each piece list check if the element have count of 2 for doubles.
    computer_doublets = [computer_piece for dots in range(7) for computer_piece in computer_pieces
                         if computer_piece == [dots, dots]]

    player_doublets = [player_piece for dots in range(7) for player_piece in player_pieces
                       if player_piece == [dots, dots]]

    return computer_doublets, player_doublets


def who_move_first(computer_stack, player_stack, dominos):
    computer_doubles, player_doubles = doublets_domino(computer_stack, player_stack)

    # loop until double list is not empty
    while (computer_doubles is None
           and player_doubles is None):
        # redistribute the pieces
        computer_stack, player_stack, dominos = distribute_pieces(dominos)
        computer_doubles, player_doubles = doublets_domino(computer_stack, player_stack)

    if computer_doubles is None:
        status = 'computer'      # check if computer_doubles list is empty
        # assign the status to computer and set domin_move to players
        domino_move = max(player_doubles)
    elif player_doubles is None:
        status = 'player'
        domino_move = max(computer_doubles)
    else:
        computer_move = max(computer_doubles)
        player_move = max(player_doubles)

        if player_move > computer_move:
            status = 'computer'
            domino_move = player_move
        else:
            status = 'player'
            domino_move = computer_move

    return status, domino_move, computer_stack, player_stack, dominos


def player_move(player_domino):
    while True:
        try:
            place = int(input())
            if place > 0 and place <= len(player_domino):
                break
            else:
                print('invalid input. Please try again')
        except ValueError:
            print('invalid input. Please try again')
    return place - 1  # as list start at '0'.


def update_board(move, player_hand, dominos, domino_snake):
    if move < 0:
        domino_snake.insert(0, player_hand[move-1])
    elif move > 0:
        domino_snake.append(player_hand[move-1])
    else:
        if dominos is not None:
            extra_piece = dominos[random.randint(0, len(dominos))]
            player_hand.append(extra_piece)
            dominos.remove(extra_piece)
        else:
            print('Stock is empty!.')


def start_game():
    Domino_snake = list()
    Dominos = domino_stock()

    computer_pieces, player_pieces, Dominos = distribute_pieces(Dominos)
    turn, piece_move, computer_pieces, player_pieces, Dominos = who_move_first(computer_pieces, player_pieces, Dominos)

    if turn == 'player':
        Domino_snake.append(piece_move)
        computer_pieces.remove(piece_move)
    else:
        Domino_snake.append(piece_move)
        player_pieces.remove(piece_move)

    while True:
        # interface
        print('=' * 70)
        print(f'Stock size: {len(Dominos)}')
        print(f'Computer pieces: {len(computer_pieces)}')

        for domino_piece in Domino_snake:
            print(domino_piece, end='')

        print()
        print('Your pieces: ')
        for index, piece in enumerate(player_pieces, start=1):
            print(f'{index}:{piece}')
        print()

        if turn == 'computer':
            print(f'Status: Computer is about to make a move. Press Enter to continue...')

        else:
            print("Status: It's your turn to make a move. Enter your command.")
            move = player_move(player_pieces)
            update_board(move, player_pieces, Dominos, Domino_snake)


start_game()
