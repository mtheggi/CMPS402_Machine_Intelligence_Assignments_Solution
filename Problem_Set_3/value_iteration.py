from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    def _compute_bellman(self, state, actions):
        values = []    # Initialize a list to store value of each action
        for action in actions:  # Loop over all possible actions
            # Get all the possible next states from current state taking current action
            successors = self.mdp.get_successor(state, action)
            value = 0
            # Loop over each next state and its probability
            for next_state, p in successors.items():
                # Get the reward of going to the next state taking current action from current state
                reward = self.mdp.get_reward(state, action, next_state)
                # accumulate the value calculated from Bellman Equation
                # print(type(self.utilities))
                # print(next_state)
                # print(type(next_state))
                value += p * (reward + self.discount_factor * self.utilities[next_state])
            # Append the current action with its value to the list
            values.append((value, action))
        # Sort the values depeding on the utility. This is a stable sort
        values.sort(key=lambda item: -item[0])
        # Return the first action that has the maximum utility
        return values[0]
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        #TODO: Complete this function
        #NotImplemented()
        if self.mdp.is_terminal(state):  # if the state is terminal, return 0
            return 0
        # Compute Bellman's Equation and return the utility only
        return self._compute_bellman(state, self.mdp.get_actions(state))[0]

    
    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        new_utilities = {state: self.compute_bellman(state) for state in self.mdp.get_states()}
        max_change = max(abs(new_utilities[state] - self.utilities[state]) for state in self.mdp.get_states())
        self.utilities = new_utilities
        return max_change <= tolerance
    
        # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        for i in range(iterations):
            if self.update(tolerance):
                 return i+1
        return iterations
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        if self.mdp.is_terminal(state):  # If the state is terminal, return None
            return None
        # Compute Bellman's Equation and return the action only
        return self._compute_bellman(state, env.actions())[1]

    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in utilities.items()}
