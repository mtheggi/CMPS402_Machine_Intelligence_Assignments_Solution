from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use
import heapq

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    Q = deque()
    Q.append((initial_state, []))  # Add the initial state and an empty path to the queue
    reached = set()
    if problem.is_goal(initial_state):  # Check if the initial state is the goal state
        return reached
    reached.add(initial_state)  # Mark the initial state as reached
    while len(Q) != 0:  # Continue until the queue is empty
        front = Q.popleft()  # Get the front node from the queue
        frontNode = front[0]  # Extract the state from the front node
        for i in problem.get_actions(frontNode):  # Iterate over the actions of the front node
            newPath = front[1].copy()  # Create a new path by copying the existing path
            successor = problem.get_successor(frontNode, i)  # Get the successor state
            if problem.is_goal(successor):  # Check if the successor state is the goal state
                newPath.append(i)  # Append the action to the path
                return newPath  # Return the path if the goal state is reached
            if successor not in reached:  # Check if the successor state has not been reached before
                reached.add(successor)  # Mark the successor state as reached
                newPath.append(i)  # Append the action to the path
                Q.append((successor, newPath))  # Add the successor state and the updated path to the queue
    return None  # Return None if no solution is found

def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    Q = deque()
    Q.append((initial_state, []))  # Add the initial state and an empty path to the queue
    reached = set()
    reached.add(initial_state)  # Mark the initial state as reached
    while Q:
        frontNode, path = Q.pop()  # Get the front node and its path from the queue
        if problem.is_goal(frontNode):  # Check if the front node is the goal state
            return path  # Return the path if the goal state is reached
        for action in problem.get_actions(frontNode):  # Iterate over the actions of the front node
            successor = problem.get_successor(frontNode, action)  # Get the successor state
            if successor not in reached:  # Check if the successor state has not been reached before
                reached.add(successor)  # Mark the successor state as reached
                Q.append((successor, path + [action]))  # Add the successor state and the updated path to the queue
    return None  # Return None if no solution is found

def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    pq = [] # priority queue to store the nodes to be expanded
    counter =0  # counter to break ties when nodes have the same priority
    heapq.heappush(pq, (0, counter , initial_state , [])) # add the initial state to the queue
    counter+=1
    reachedCosts = {initial_state:0} # dictionary to store the minimum cost to reach each state
    while( len(pq)!= 0 ): 
        current_cost , count, currentstate , path = heapq.heappop(pq) # get the node with the lowest cost from the queue
        if(problem.is_goal(currentstate)): # check if the current state is the goal state
            return path 
        for i in problem.get_actions(currentstate): # Expand(currentstate )
            successor = problem.get_successor(currentstate, i) 
            successorCost= problem.get_cost(currentstate,i) 
            if successor not in reachedCosts: # check if the successor state has been reached before
                reachedCosts[successor] = current_cost+successorCost # update the minimum cost to reach the successor state
                heapq.heappush(pq,(current_cost+successorCost, counter, successor,path+[i] )) # add the successor state to the queue
                counter+=1 # increment counter to break ties when next pushing
            if successor in reachedCosts and reachedCosts[successor] > (current_cost+successorCost): # check if a better path to the successor state has been found
                reachedCosts[successor] = current_cost+successorCost # update the minimum cost to reach the successor state
                for j in range(len(pq)): # check if the state is already in frontier with higher cost.  
                    if pq[j][2] == successor: # if found delete it and reheapfy the pq 
                        pq.remove(pq[j]) 
                        heapq.heapify(pq) 
                        break
                heapq.heappush(pq,(current_cost+successorCost, counter, successor,path+[i] )) # add the successor state to the queue
                counter+=1                        
    return None # return None if no solution is found

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    pq = []
    counter = 0
    heapq.heappush(pq, (0, counter, initial_state, []))  # Add the initial state to the priority queue
    counter += 1
    reachedcost = {initial_state: 0}  # Dictionary to store the minimum cost to reach each state
    while pq:
        currentCost, count, currState, path = heapq.heappop(pq)  # Get the node with the lowest cost from the queue
        currentCost -= heuristic(problem, currState)  # Subtract the heuristic value from the current cost
        if problem.is_goal(currState):  # Check if the current state is the goal state
            return path  # Return the path if the goal state is reached
        for action in problem.get_actions(currState):  # Iterate over the actions of the current state
            successor = problem.get_successor(currState, action)  # Get the successor state
            successorcost = problem.get_cost(currState, action)  # Get the cost to reach the successor state
            finalcost = currentCost + heuristic(problem, successor) + successorcost  # Calculate the final cost
            if successor not in reachedcost:  # Check if the successor state has not been reached before
                reachedcost[successor] = finalcost  # Update the minimum cost to reach the successor state
                heapq.heappush(pq, (finalcost, counter, successor, path + [action]))  # Add the successor state to the queue
                counter += 1
            if successor in reachedcost and reachedcost[successor] > finalcost:  # Check if a better path to the successor state has been found
                reachedcost[successor] = finalcost  # Update the minimum cost to reach the successor state
                for j in range(len(pq)):  # Check if the state is already in the queue with a higher cost
                    if pq[j][2] == successor:  # If found, remove it from the queue
                        pq.remove(pq[j])
                        heapq.heapify(pq)  # Reheapify the queue
                        break
                heapq.heappush(pq, (finalcost, counter, successor, path + [action]))  # Add the successor state to the queue
                counter += 1
    return None  # Return None if no solution is found

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    pq = []  # Priority queue to store the states
    counter = 0  # Counter to break ties in the priority queue
    heapq.heappush(pq, (heuristic(problem, initial_state), counter, initial_state, []))  # Add the initial state to the priority queue
    counter += 1
    reachedcost = {initial_state: 0}  # Dictionary to store the minimum cost to reach each state
    while pq:
        _, _, currState, path = heapq.heappop(pq)  # Get the node with the lowest cost from the queue
        if problem.is_goal(currState):  # Check if the current state is the goal state
            return path  # Return the path if the goal state is reached
        for action in problem.get_actions(currState):  # Iterate over the actions of the current state
            successor = problem.get_successor(currState, action)  # Get the successor state
            finalcost = heuristic(problem, successor)  # Calculate the heuristic value for the successor state
            if successor not in reachedcost:  # Check if the successor state has not been reached before
                reachedcost[successor] = finalcost  # Update the minimum cost to reach the successor state
                heapq.heappush(pq, (finalcost, counter, successor, path + [action]))  # Add the successor state to the queue
                counter += 1
    return None  # Return None if no solution is found
    #NotImplemented()