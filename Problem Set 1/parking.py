from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented

# Brief problem Formulation : 
# state :  array of array of charachters  . each row represent a row in the parking lot.
#         [parking[i][j] -> represent tile in position (i,j) in the parking lot]
# actions : move(chosen car , direction, number of steps) 
#           if(parking[i+2][j] is not awall) -> move("A", "down", 2) -> move car A 2 steps down
#         
# successor: update the state according to the action 
#           updating the position of the car in the parking lot array 
#            
# goal : each car is in its slot 
# cost : appling a cost according to :- number of steps 
#                                    - the employee type 
#                                    - if car moved in a slot that is not its slot 



#TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = list[list[str]] # reason explained in problem formulation above 

# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        intial_state = []
        # intialize the parking tiles as all walls   
        for j in range (self.height+1):
            new_default_wall = ['#']  
            for i in range(self.width) :
                new_default_wall.append('#') 
            intial_state.append(new_default_wall) 
        for pt in list(self.passages):
            intial_state[pt.y][pt.x] = "."
        # add the slots 
        for Pt , value in self.slots.items(): 
            intial_state[Pt.y][Pt.x] = str(value)
        # add the cars in the parking lot
        for i in range((len(self.cars))):
            intial_state[self.cars[i].y][self.cars[i].x] = chr(ord('A') + i)
        return intial_state 
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        # loop over the slots and check if the car is in its required slot by comparing the "char" of the car with the index of the slot
        for pt , idx in self.slots.items(): 
            if state[pt.y][pt.x] != chr(ord('A') +idx) : 
                return False 
        return True 
 
    
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        #TODO: ADD YOUR CODE HERE
        actions =[]  
        # loop over all the grid 
        for i in range(self.width): # col 
            for j in range(self.height): # row
                # check if the tile is not a wall and not empty and not a slot, then add the possible actions
                if ord(state[j][i]) >= ord('A') and ord(state[j][i]) <= ord('Z'): 
                    car_indx = ord(state[j][i]) - ord('A') # get the index of the car 
                    if i > 0 and (state[j][i-1]=='.' or Point(i-1,j) in self.slots.keys()): 
                        actions.append((car_indx, Direction.LEFT))
                    if((i+1)< self.width and (state[j][i+1]=='.' or Point(i+1,j) in self.slots.keys())): 
                        actions.append((car_indx, Direction.RIGHT))
                    if(j+1 < self.height and (state[j+1][i]=='.' or Point(i,j+1) in self.slots.keys())): 
                        actions.append((car_indx, Direction.DOWN))
                    if(j> 0 and (state[j-1][i]=='.' or Point(i,j-1) in self.slots.keys())):
                        actions.append((car_indx, Direction.UP))
        return actions 
        
    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        #TODO: ADD YOUR CODE HERE
        # get the index of the car and the direction of the action
        car_char=  chr(action[0] + ord('A')) 
        new_state =state 

        for i in range(self.width):
            for j in range(self.height):
                # get the position of the car in the parking lot 
                if new_state[j][i] == car_char : 
                    car_new_pos = action[1].to_vector().__add__(Point(i,j)) # get the new position of the car
                    # check if the new position is not a wall 
                    new_state[car_new_pos.y][car_new_pos.x] = car_char # update the car position in the parking lot
                    if Point(i,j )in self.slots.keys(): 
                        new_state[j][i] = str(self.slots[Point(i,j)]) # update the car position in the parking lot
                    elif new_state[car_new_pos.y][car_new_pos.x] != "#":
                        new_state[j][i] = "." # update the car position in the parking lot 
                    return new_state 
        return new_state             
    
    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        # Calculate the cost of applying the given action to the given state
        cost = 0.0 
        for i in range(self.width) :
            for j in range(self.height):
                if (ord(state[j][i])-ord('A')) == action[0] : 
                    char_cost = ord('Z')+1-ord(state[j][i])
                    newX = i+action[1].to_vector().x 
                    newY = j+action[1].to_vector().y 
                    # Check if the new position is within the parking lot boundaries and not a wall
                    if newX < self.width and newX > 0 and newY < self.height and newY >0 and state[newY][newX] != '#': 
                        cost += char_cost 
                        pts = Point(newX, newY)
                        # Check if the new position is a parking slot and the car is not in its required slot
                        if pts in self.slots.keys() and str(ord(state[j][i])-ord('A')) != state[newY][newX] :
                            cost = cost + 100.0   
        return cost 

    # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    
