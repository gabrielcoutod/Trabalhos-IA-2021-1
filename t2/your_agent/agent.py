# biblioteca para realizar copias profundas
import copy 


MAX_VAL =  100000
MIN_VAL = -100000
MAX_DEPTH = 3
INITIAL_DEPTH = 0
NO_MOVES = (-1,-1)

def make_move(the_board, color):
    v, move = valor_max(the_board, color, MIN_VAL, MAX_VAL, INITIAL_DEPTH)
    return move

def valor_max(the_board, color, alpha, beta, depth):
    if teste_corte(the_board, depth, color):
        return avalia_pos(the_board, color), NO_MOVES
    
    v = MIN_VAL
    move = NO_MOVES
    legal_moves = the_board.legal_moves(color)
    if len(legal_moves) == 0:
        legal_moves = [(-1,-1)]

    for new_move in legal_moves:
        s = copy.deepcopy(the_board)
        s.process_move(new_move, color)

        temp_v, temp_move = valor_min(s, the_board.opponent(color), alpha, beta, depth + 1)
        v, move = (temp_v, new_move) if temp_v > v else (v, move)

        alpha = max(alpha, v)
        if alpha >= beta:
            break
    return v, move

def valor_min(the_board, color, alpha, beta, depth):
    if teste_corte(the_board, depth, color):
        return avalia_pos(the_board, the_board.opponent(color)), NO_MOVES
    
    v = MAX_VAL
    move = NO_MOVES
    legal_moves = the_board.legal_moves(color)
    if len(legal_moves) == 0:
        legal_moves = [(-1,-1)]

    for new_move in legal_moves:
        s = copy.deepcopy(the_board)
        s.process_move(new_move, color)

        temp_v, temp_move = valor_max(s, the_board.opponent(color), alpha, beta, depth + 1)
        v, move = (temp_v, new_move) if temp_v < v else (v, move)

        beta = min(beta, v)
        if beta <= alpha:
            break
    return v, move

def teste_corte(the_board, depth, color):
    return the_board.is_terminal_state() or depth > MAX_DEPTH or (not the_board.has_legal_move(color) and depth == INITIAL_DEPTH)


def avalia_pos(the_board, color):
    '''Baseado na heuristica em https://kartikkukreja.wordpress.com/2013/03/30/heuristic-function-for-reversiothello/'''
    board_str = the_board.__str__()
    opponent_color = the_board.opponent(color)


    player_coins = board_str.count(color)
    enemy_coins = board_str.count(opponent_color)
    parity = 100 * (player_coins - enemy_coins) / (player_coins + enemy_coins)


    player_moves = len(the_board.legal_moves(color))
    enemy_moves = len(the_board.legal_moves(opponent_color))
    mobility = (100 * (player_moves - enemy_moves) / (player_moves + enemy_moves)) if player_moves + enemy_moves != 0 else 0


    player_corners = 0
    enemy_corners = 0
    corners = [0,7,56,63]
    for corner in corners:
        if board_str[corner] == color:
            player_corners += 1
        elif board_str[corner] == opponent_color:
            enemy_corners += 1

    corner = (100 * (player_corners - enemy_corners) / (player_corners + enemy_corners)) if player_corners + enemy_corners != 0 else 0


    parity_weight = 20
    mobility_weight = 30
    corner_weight = 50
    return (parity_weight * parity) + (mobility_weight * mobility) + (corner_weight * corner)

