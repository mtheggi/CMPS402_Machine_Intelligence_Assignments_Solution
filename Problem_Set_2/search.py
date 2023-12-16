from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented
import math 

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: 
        return values[agent], None

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
    agent = game.get_turn(state)  # Get the current player's turn

    terminal, values = game.is_terminal(state)  # Check if the state is a terminal state and get the values for all agents
    if terminal:
        return values[0], None  # If it is a terminal state, return the value for the player and no action

    if max_depth == 0:
        return heuristic(game, state, 0), None  # If the maximum depth is reached, return the heuristic value for the player and no action

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]  # Get all possible actions and their resulting states
    if agent == 0:
        value, dumm, action = max((minimax(game, state, heuristic, max_depth-1)[0], -index, action) for index, (action, state) in enumerate(actions_states))  # If it is the player's turn, select the action that maximizes the minimax value
    else:
        value, dumm, action = min((minimax(game, state, heuristic, max_depth-1)[0], index, action) for index, (action, state) in enumerate(actions_states))  # If it is an enemy's turn, select the action that minimizes the minimax value
    return value, action  # Return the selected minimax value and the corresponding action
    
    
    #NotImplemented()

# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.

    #NotImplemented()

# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    return recursive_alphabeta(game, state, heuristic, max_depth, -math.inf, math.inf)

def recursive_alphabeta(game, state, heuristic, max_depth, alpha, beta, sort=False):
    agent = game.get_turn(state)  # Get the current player's turn

    terminal, values = game.is_terminal(state)  # Check if the state is a terminal state and get the values for all agents
    if terminal:
        return values[0], None  # If it is a terminal state, return the value for the player and no action

    if max_depth == 0:
        return heuristic(game, state, 0), None  # If the maximum depth is reached, return the heuristic value for the player and no action

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]  # Get all possible actions and their resulting states

    if sort:
        actions_states = sorted(actions_states, key=lambda item: -heuristic(game, item[1], agent))  # Sort the actions based on the heuristic value of their resulting states

    if agent == 0:  # If it is the player's turn
        results = []
        value, action = -math.inf, None
        for index, (action, state) in enumerate(actions_states):
            cur_value = recursive_alphabeta(game, state, heuristic, max_depth - 1, alpha, beta, sort)[0]  # Recursively call alphabeta on the next state
            results.append((cur_value, -index, action))  # Store the value, index, and action in the results list
            value, dumm, action = max(results)  # Select the action that maximizes the value
            if value >= beta:  # If the value is greater than or equal to beta, prune the remaining actions
                return value, action
            alpha = max(alpha, value)  # Update the alpha value
    else:  # If it is an enemy's turn
        results = []
        value, action = math.inf, None
        for index, (action, state) in enumerate(actions_states):
            cur_value = recursive_alphabeta(game, state, heuristic, max_depth - 1, alpha, beta, sort)[0]  # Recursively call alphabeta on the next state
            results.append((cur_value, -index, action))  # Store the value, index, and action in the results list
            value, dum, action = min(results)  # Select the action that minimizes the value
            if value <= alpha:  # If the value is less than or equal to alpha, prune the remaining actions
                return value, action
            beta = min(beta, value)  # Update the beta value
    return value, action  # Return the selected value and action

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    return recursive_alphabeta(game, state, heuristic, max_depth, -math.inf, math.inf, True)

def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    return recursive_expectimax(game ,state ,heuristic , max_depth , False)

def recursive_expectimax(game, state, heuristic, max_depth, chance) -> Tuple[float, A]:
    agent = game.get_turn(state)  # Get the current player's turn

    terminal, values = game.is_terminal(state)  # Check if the state is a terminal state and get the values for all agents
    if terminal:
        return values[0], None  # If it is a terminal state, return the value for the player and no action

    if max_depth == 0:
        return heuristic(game, state, 0), None  # If the maximum depth is reached, return the heuristic value for the player and no action

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]  # Get all possible actions and their resulting states

    if chance and agent != 0:  # If it is a chance node and not the player's turn
        _sum = 0
        _num = len(actions_states)
        for action, state in actions_states:
            value, action = recursive_expectimax(game, state, heuristic, max_depth-1, False)  # Recursively call expectimax on the next state
            _sum += value  # Sum up the values of all possible actions
        value = _sum / _num  # Calculate the average value
    elif agent == 0:  # If it is the player's turn
        value, dum, action = max((recursive_expectimax(game, state, heuristic, max_depth-1, True)[0], -index, action) for index, (action, state) in enumerate(actions_states))  # Select the action that maximizes the value
    else:  # If it is an enemy's turn
        value, dum, action = min((recursive_expectimax(game, state, heuristic, max_depth-1, True)[0], index, action) for index, (action, state) in enumerate(actions_states))  # Select the action that minimizes the value
    return value, action  # Return the selected value and action
