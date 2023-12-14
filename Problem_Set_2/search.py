from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented
import math 
#TODO: Import any modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    agent = game.get_turn(state)   # Get the current player

    # Check if you're in a terminal state, then no action is needed
    terminal, values = game.is_terminal(state)
    if terminal:
        return values[0], None

    # If you reached the maximum depth,
    # use a heuristic to evaluate the value of the terminla state and no extra actions is needed
    if max_depth == 0:
        return heuristic(game, state, 0), None

    # Get all children of the current node combined with its action
    actions_states = [(action, game.get_successor(state, action))
                      for action in game.get_actions(state)]
    if agent == 0:  # Max player
        # Get the best action that achieves the best/maximum value
        value, _, action = max((minimax(game, state, heuristic, max_depth-1)[
                               0], -index, action) for index, (action, state) in enumerate(actions_states))
    else:           # Min player
        # Get the best action that achieves the best/minimum value
        value, _, action = min((minimax(game, state, heuristic, max_depth-1)[
                               0], index, action) for index, (action, state) in enumerate(actions_states))
    return value, action
    
    #NotImplemented()

# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    return recursive_alpahbeta(game, state, heuristic, max_depth, -math.inf, math.inf)


def recursive_alpahbeta(game, state, heuristic, max_depth, alpha, beta, sort=False):
    agent = game.get_turn(state)  # Get the current player

    # Check if you're in a terminal state, then no action is needed
    terminal, values = game.is_terminal(state)
    if terminal:
        return values[0], None

    # If you reached the maximum depth,
    # use a heuristic to evaluate the value of the terminla state and no extra actions is needed
    if max_depth == 0:
        return heuristic(game, state, 0), None

    # Get all children of the current node combined with its action
    actions_states = [(action, game.get_successor(state, action))
                      for action in game.get_actions(state)]

    # In case of alpha-beta pruning with move ordering, you need to sort all possible actions/states/nodes
    # depending on the evaluated heuristic
    if sort:
        actions_states = sorted(
            actions_states, key=lambda item: -heuristic(game, item[1], agent))

    if agent == 0:  # Max player
        results = []
        value, action = -math.inf, None
        # Get the best action that achieves the best/maximum value
        for index, (action, state) in enumerate(actions_states):
            cur_value = recursive_alpahbeta(game, state, heuristic,
                                   max_depth - 1, alpha, beta, sort)[0]

            results.append((cur_value, -index, action))
            value, _, action = max(results)  # Maximum value for the MAX player

            # If the current value is greater than or equal to beta,
            # prune the search and return the best value with best action
            if value >= beta:
                return value, action

            # Update alpha with maximum possible value
            alpha = max(alpha, value)

    else:           # Min player
        results = []
        value, action = math.inf, None
        # Get the best action that achieves the best/minimum value
        for index, (action, state) in enumerate(actions_states):
            cur_value = recursive_alpahbeta(game, state, heuristic,
                                   max_depth - 1, alpha, beta, sort)[0]

            results.append((cur_value, -index, action))
            value, _, action = min(results)  # Minimum value for the MIN player

            # If the current value is less than or equal to alpha,
            # prune the search and return the best value with best action
            if value <= alpha:
                return value, action

            # Update beta with minimum possible value
            beta = min(beta, value)

    return value, action

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    return recursive_alpahbeta(game, state, heuristic, max_depth, -math.inf, math.inf, True)
    #NotImplemented()

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
    return recursive_expectimax(game ,state ,heuristic , max_depth , False)


def recursive_expectimax(game, state, heuristic, max_depth, chance) -> Tuple[float, A]:
    agent = game.get_turn(state)  # Get the current player
    # Check if you're in a terminal state, then no action is needed
    terminal, values = game.is_terminal(state)
    if terminal:
        return values[0], None
    # If you reached the maximum depth,
    # use a heuristic to evaluate the value of the terminla state and no extra actions is needed
    if max_depth == 0:
        return heuristic(game, state, 0), None
    # Get all children of the current node combined with its action
    actions_states = [(action, game.get_successor(state, action))
                      for action in game.get_actions(state)]
    if chance and agent != 0:  # Chance Node
        _sum = 0
        _num = len(actions_states)
        # Get the average value of all children for the current node
        for action, state in actions_states:
            value, action = recursive_expectimax( game, state, heuristic, max_depth-1, False)
            _sum += value
        value = _sum / _num
    elif agent == 0:  # Max player
        # Get the best action that achieves the best/maximum value
        value, _, action = max((recursive_expectimax(game, state, heuristic, max_depth-1, True)[0], -index, action)
                               for index, (action, state) in enumerate(actions_states))
    else:           # Min player
        # Get the best action that achieves the best/minimum value
        value, _, action = min((recursive_expectimax(game, state, heuristic, max_depth-1, True)[0], index, action)
                               for index, (action, state) in enumerate(actions_states))
    return value, action