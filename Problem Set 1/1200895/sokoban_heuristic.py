from sokoban import SokobanProblem, SokobanState , SokobanLayout , SokobanTile
from mathutils import Direction, Point, manhattan_distance,euclidean_distance
from helpers.utils import NotImplemented
from typing import Dict, List ,Set 
# from scipy.optimize import linear_sum_assignment

# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1

#TODO: Import any modules and write any functions you want to use



def is_wall(pt : Point , state:SokobanState) -> bool: 
    #check if not in walkable tiles and not in goals and not in player position and not in crates 
    if pt not in state.layout.walkable and pt not in state.layout.goals and pt != state.player and pt not in state.crates: 
        return True
    return False  

#corner deadlock occurs when a box is pushed into a corner and there are no goals along that corner then it is impossible to get away from the corner
def is_cornered(state: SokobanState, crate: Point ) -> bool:
    # Define the points that represent the adjacent squares
    left = Point(crate.x - 1, crate.y)
    right = Point(crate.x + 1, crate.y)
    up = Point(crate.x, crate.y - 1)
    down = Point(crate.x, crate.y + 1)
    # If the crate is in a corner, then it is in a deadlock
    if ((is_wall(left , state)  and is_wall(up,state)) or
        (is_wall(left,state) and is_wall(down ,state )) or
        (is_wall(right,state) and is_wall(up,state) ) or
        (is_wall(right,state) and is_wall(down,state))):
        return True
    return False


#edge deadlock occurs when a box is pushed against the wall and there are no goals along that goal then it is impossible to get away from the wall 
def is_edge_deadlocked(state: SokobanState, crate: Point) -> bool:
    x, y = crate.x, crate.y

    # Check if the crate is along a horizontal wall
    if is_wall(Point(x, y - 1),state) or is_wall(Point(x, y + 1),state):
        # Check if there are walls or other crates at both ends of the row
        if (is_wall(Point(x - 1, y),state) or Point(x - 1, y) in state.crates) and \
           (is_wall(Point(x + 1, y),state) or Point(x + 1, y) in state.crates):
            return True 
        #check if there is no goal among the row
        if not any(Point(i, y) in state.layout.goals for i in range(state.layout.width+1)):
            return True

    # Check if the crate is along a vertical wall
    if is_wall(Point(x - 1, y),state) or is_wall(Point(x + 1, y),state):
        # Check if there are walls or other crates at both ends of the column
        if (is_wall(Point(x, y - 1),state) or Point(x, y - 1) in state.crates) and \
           (is_wall(Point(x, y + 1),state) or Point(x, y + 1) in state.crates):
            # Check if there are any goals along the wall
            return True
        #check if there is no goal among the column 
        if not any(Point(x, i) in state.layout.goals for i in range(state.layout.height+1)):
            return True

    return False





def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
    
    total_cost = 0.0
    #if goal return zero 
    if problem.is_goal(state):
        return total_cost

    # For each crate in the state
    for crate in state.crates:
        # If the crate is in a corner or in edge , then it is in a deadlock and the state is unsolvable 
        # so i will return infinity to make this state at the end of frontier while searching 

        if crate not in state.layout.goals and  (is_cornered(state, crate) or is_edge_deadlocked(state, crate)): 
            return float("inf")
            
        # Calculate the sum  of Manhattan distance from each the crate to its nearest goal
        distances = {manhattan_distance(crate, goal) for goal in problem.layout.goals}
        total_cost += min(distances)

    return total_cost
