# biblioteca para realizar copias profundas
import copy 

# variaveis para os valores maximos e minimos do algoritmo
MAX_VAL =  100000
MIN_VAL = -100000
# variaveis para a profundidade da avaliação
MAX_DEPTH = 3
INITIAL_DEPTH = 0
# variavel para representar um movimento nulo
NO_MOVES = (-1,-1)

def make_move(the_board, color):
    '''Retorna o melhor movimento usando o algoritmo minimax para o estado atual no jogo.'''
    v, move = valor_max(the_board, color, MIN_VAL, MAX_VAL, INITIAL_DEPTH)
    return move

def valor_max(the_board, color, alpha, beta, depth):
    '''Função para o jogador MAX.'''

    # testa se deve parar de analisar
    if teste_corte(the_board, depth, color):
        return avalia_pos(the_board, color), NO_MOVES
    
    # inicializa as variaveis do algoritmo
    v = MIN_VAL
    move = NO_MOVES
    legal_moves = the_board.legal_moves(color)

    # caso o jogador atual não tenha movimentos possiveis e existam jogadas disponiveis 
    # para o oponente adiciona um movimento vazio para entrar no loop e analisar
    if len(legal_moves) == 0:
        legal_moves = [(-1,-1)]

    # loop para verificar qual o melhor movimento no estado atual
    for new_move in legal_moves:
        # estado com o movimento atual
        s = copy.deepcopy(the_board)
        s.process_move(new_move, color)

        # verifica se deve atualizar o melhor movimento
        temp_v, temp_move = valor_min(s, the_board.opponent(color), alpha, beta, depth + 1)
        v, move = (temp_v, new_move) if temp_v > v else (v, move)

        alpha = max(alpha, v)
        # MIN que chamou conhece uma alternativa beta melhor que alpha
        if alpha >= beta:
            break
    return v, move

def valor_min(the_board, color, alpha, beta, depth):
    '''Função para o jogador MIN.'''

    # testa se deve parar de analisar
    if teste_corte(the_board, depth, color):
        return avalia_pos(the_board, the_board.opponent(color)), NO_MOVES
    
    # inicializa as variaveis do algoritmo
    v = MAX_VAL
    move = NO_MOVES
    legal_moves = the_board.legal_moves(color)

    # caso o jogador atual não tenha movimentos possiveis e existam jogadas disponiveis 
    # para o oponente adiciona um movimento vazio para entrar no loop e analisar
    if len(legal_moves) == 0:
        legal_moves = [(-1,-1)]

    # loop para verificar qual o melhor movimento no estado atual
    for new_move in legal_moves:
        # estado com o movimento atual
        s = copy.deepcopy(the_board)
        s.process_move(new_move, color)

        # verifica se deve atualizar o melhor movimento
        temp_v, temp_move = valor_max(s, the_board.opponent(color), alpha, beta, depth + 1)
        v, move = (temp_v, new_move) if temp_v < v else (v, move)

        beta = min(beta, v)
        # MAX que chamou conhece uma alternativa alpha melhor que beta
        if beta <= alpha:
            break
    return v, move

def teste_corte(the_board, depth, color):
    '''
    Verifica se o estado atual é terminal, a profundidade é maior que a maxima, ou se 
    não há movimentos legais para o jogador atual, e a analise está na profundidade inicial,
    indicando que não faria sentido continuar analisando os movimentos possiveis do outro jogador.
    '''
    return the_board.is_terminal_state() or depth > MAX_DEPTH or (not the_board.has_legal_move(color) and depth == INITIAL_DEPTH)


def avalia_pos(the_board, color):
    '''
    Avalia a posição atual do jogador.
    Função Baseada na heuristica em https://kartikkukreja.wordpress.com/2013/03/30/heuristic-function-for-reversiothello/
    '''
    board_str = the_board.__str__()
    opponent_color = the_board.opponent(color)

    # considera a quantidade de peças de cada jogador
    player_coins = board_str.count(color)
    enemy_coins = board_str.count(opponent_color)
    parity = 100 * (player_coins - enemy_coins) / (player_coins + enemy_coins)

    # considera a quantidade de movimentos de cada jogador
    player_moves = len(the_board.legal_moves(color))
    enemy_moves = len(the_board.legal_moves(opponent_color))
    mobility = (100 * (player_moves - enemy_moves) / (player_moves + enemy_moves)) if player_moves + enemy_moves != 0 else 0


    # considera a quantidade de cantos de cada jogador
    player_corners = 0
    enemy_corners = 0
    corners = [0,7,56,63]
    for corner in corners:
        if board_str[corner] == color:
            player_corners += 1
        elif board_str[corner] == opponent_color:
            enemy_corners += 1

    corner = (100 * (player_corners - enemy_corners) / (player_corners + enemy_corners)) if player_corners + enemy_corners != 0 else 0

    # da um peso para cada um dos valores
    parity_weight = 20
    mobility_weight = 30
    corner_weight = 50

    # retorna a avaliação
    return (parity_weight * parity) + (mobility_weight * mobility) + (corner_weight * corner)