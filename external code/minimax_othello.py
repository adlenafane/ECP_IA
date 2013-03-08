# minimax:

def minimax_value(game, maxply, eval_fn = None):
    """Find the utility value of the game w.r.t. the current player."""
  
    # if we have reached the maximum depth, the utility is approximated
    # with the evaluation function
    if maxply == 0 or game.terminal_test():
        if eval_fn:
            return eval_fn(game)
        else:
            return game.score()

    best = None

    # try each move
    for move in game.generate_moves():
        g = game.copy()
        g.play_move(move)
        # evaluate the position and choose the best move
        # NOTE: the minimax function computes the value for the current
        # player which is the opponent so we need to invert the value
        val = -1 * minimax_value(g, maxply-1, eval_fn)
        if best is None or val > best:
            best = val

    return best

def minimax(game, maxply, eval_fn = None):
    """Find the best move in the game, looking ahead maxply moves.

    Returns a tuple (estimated value, operator)
    The game must support the following functions:
    
    copy() to make a deep copy of the game
    eval() a naive utility fn for non-terminal positions,
           but precise for terminal positions
    terminal_test() to determine whether the game is over
    operators() to return a list of operators on the current game state
    apply() to modify the game state by applying an operator

    maxply  the number of moves of lookahead 0=> no lookahead

    eval_fn instead of using the default game.eval(),
            to be used only for non-terminal positions
    """

    best = None

    # try each move
    for move in game.generate_moves():
        g = game.copy()
        g.play_move(move)
        # evaluate the position and choose the best move
        # NOTE: the minimax function computes the value for the current
        # player which is the opponent so we need to invert the value
        val = -1 * minimax_value(g, maxply, eval_fn)
        # update the best operator so far
        if best is None or val > best[0]:
            best = (val, move)

    return best

def alphabeta_value(game, maxply, alpha, beta, eval_fn = None):
    """Find the utility value of the game w.r.t. the current player.

    alpha = None => -inf
    beta = None => +inf
    """

    # if we have reached the maximum depth, the utility is approximated
    # with the evaluation function
    if maxply == 0 or game.terminal_test():
        if eval_fn:
            return eval_fn(game)
        else:
            return game.score()

    # try each move
    for move in game.generate_moves():
        g = game.copy()
        g.play_move(move)
        # evaluate the position and choose the best move
        # NOTE: the minimax function computes the value for the current
        # player which is the opponent so we need to invert the value
        # invert alpha beta values and meaning, think of the following
        #     alpha <=  my score <=  beta
        # => -alpha >= -my score >= -beta
        # => -alpha >= opp score >=  beta
        # => -beta  <= opp score <= -alpha
        if beta is not None:
            opp_alpha = -1 * beta
        else:
            opp_alpha = None
        if alpha is not None:
            opp_beta = -1 * alpha
        else:
            opp_beta = None
        val = -1 * alphabeta_value(g, maxply-1, opp_alpha, opp_beta, eval_fn)
        # update alpha (current player's low bound)
        if alpha is None or val > alpha:
            alpha = val
        # prune using the alpha-beta condition
        if (alpha is not None) and (beta is not None) and alpha >= beta:
            # I suppose we could return alpha here as well
            return beta
    
    # alpha is my best score
    return alpha

def alphabeta(game, maxply, eval_fn = None):
    """Find the best move in the game, looking ahead maxply moves.

    Returns a tuple (estimated value, move)
    The game must support the following functions:
    
        copy() to make a deep copy of the game
        score() a naive utility fn for non-terminal positions,
               but precise for terminal positions
        terminal_test() to determine whether the game is over
        generate_moves() to return a list of legal moves in the current
                         game state
        play_move() to modify the game state by applying an operator

    maxply  the number of moves of lookahead 0=> no lookahead

    eval_fn instead of using the default game.eval(),
            to be used only for non-terminal positions
    """

    best_val, best_move = None, None

    # try each move    
    for move in game.generate_moves():
        g = game.copy()
        g.play_move(move)
        # evaluate the position and choose the best move
        # NOTE: the minimax function computes the value for the current
        # player which is the opponent so we need to invert the value
        # the -ve of my best val is the opponent's beta value
        if best_val is not None:
            opp_beta = -1 * best_val
        else:
            opp_beta = None
        val = -1 * alphabeta_value(g, maxply, None, opp_beta, eval_fn)
        # update the best operator so far
        if best_val is None or val > best_val:
            (best_val, best_move) = (val, move)

    return (best_val, best_move)
