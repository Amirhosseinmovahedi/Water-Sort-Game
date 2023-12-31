import copy
import heapq

class State:

    def __init__(self,current_state: list[list[int]] , g: int, h: int
                                , parent_state, move: tuple) -> None:
        self.values = current_state
        self.g = g
        self.h = h
        self.parent_state = parent_state
        self.move = move

    def __gt__(self, other) -> None:
        return True
    
    def __repr__(self) -> str:
        """using string representation for dubuging purposes"""
        return f"<< {self.values}, {self.g}, {self.h}, {self.parent_state}, {self.move} >>"

class GameSolution:
    """
        A class for solving the Water Sort game and finding solutions(normal, optimal).

        Attributes:
            ws_game (Game): An instance of the Water Sort game which implemented in game.py file.
            moves (List[Tuple[int, int]]): A list of tuples representing moves between source and destination tubes.
            solution_found (bool): True if a solution is found, False otherwise.

        Methods:
            solve(self, current_state):
                Find a solution to the Water Sort game from the current state.
                After finding solution, please set (self.solution_found) to True and fill (self.moves) list.

            optimal_solve(self, current_state):
                Find an optimal solution to the Water Sort game from the current state.
                After finding solution, please set (self.solution_found) to True and fill (self.moves) list.
    """
    def __init__(self, game):
        """
            Initialize a GameSolution instance.
            Args:
                game (Game): An instance of the Water Sort game.
        """
        self.ws_game = game  # An instance of the Water Sort game.
        self.moves = []  # A list of tuples representing moves between source and destination tubes.
        self.tube_numbers = game.NEmptyTubes + game.NColor  # Number of tubes in the game.
        self.solution_found = False  # True if a solution is found, False otherwise.
        self.visited_tubes = set()  # A set of visited tubes.
        self.capacity = self.ws_game.NColorInTube


    def calculate_capacity(self, tube_des: list) -> int:
        "returns capacity of that tube"
        return self.capacity - len(tube_des) 
            

    def all_moves(self, current_state):
        """returns all the possible moves with this state"""

        possible_moves = [] # a list of tuples
        for s in range(len(current_state)):
            source = current_state[s]
            color_num = len(set(source))
            
            if len(source) == 0:
                continue   
            
            if len(source) == self.capacity and color_num == 1:
                continue

            empty_move_flg = False
            for des in range(len(current_state)):
                destination = current_state[des]
                if des == s:
                    continue

                if color_num == 1 and len(destination) == 0:
                    continue

                if len(destination) == 0:
                    if empty_move_flg == False:
                        empty_move_flg = True
                        possible_moves.append((s, des))
                elif (source[-1] == destination[-1]) and (self.capacity - len(destination) > 0):
                    possible_moves.append((s, des))

        return possible_moves
    

    def counting_top(self, tube) -> int:
        """returns the number of similar colors in the top of the tube"""

        topest_color = tube[-1]
        total = 1
        for col in tube[-2::-1]:
            if col == topest_color:
                total += 1
            else:
                break

        return total

    def move_water(self, s: int, des: int, current_state: list[tuple]):
        """moves water from source tube to the destination tube"""
        
        counting_s = self.counting_top(current_state[s])
        capacity_des = self.calculate_capacity(current_state[des])
        n = min(counting_s, capacity_des)
        for i in range(n):
            current_state[des].append(current_state[s].pop())

        return current_state



    def solve(self, current_state):
        """
            Find a solution to the Water Sort game from the current state.

            Args:
                current_state (List[List[int]]): A list of lists representing the colors in each tube.

            This method attempts to find a solution to the Water Sort game by iteratively exploring
            different moves and configurations starting from the current state.
        """
        if self.solution_found:
            if len(self.moves) > 0:
                self.moves.pop()
            return

        if self.ws_game.check_victory(current_state):
            self.solution_found = True
            return

        all_moves = self.all_moves(current_state)
        if len(all_moves) == 0:
            if len(self.moves) > 0:
                self.moves.pop()
            return

        for move in all_moves:
            current_state_copy = copy.deepcopy(current_state)
            self.move_water(move[0], move[1], current_state_copy)
            hashable_state = str(current_state_copy)
            if hashable_state in self.visited_tubes:
                continue
            else:
                self.visited_tubes.add(hashable_state)
                self.moves.append(move)
                self.solve(current_state_copy)
        
        if not self.solution_found:
            if len(self.moves) > 0:
                self.moves.pop()

    def calculate_heuristic_V0(self, current_state: list[list[int]]) -> int:
        "this function calculate h(n) based on different colors in each tube -> version 0"

        h = 0
    
        for tube in current_state:
            for i in range(len(tube) - 1):
                if tube[i] != tube[i + 1]:
                    h += 1

        return h


    def calculate_heuristic_V1(self, current_state: list[list[int]], former_h: int, move: tuple, former_state: list[list[int]]) -> int:
        "this function calculate h(n) based on different colors in each tube -> version 1"

        h = former_h
        
        for i in range(len(former_state[move[0]]) - 1):
            if former_state[move[0]][i] != former_state[move[0]][i + 1]:
                h -= 1

        for i in range(len(former_state[move[1]]) - 1):
            if former_state[move[1]][i] != former_state[move[1]][i + 1]:
                h -= 1

        for i in range(len(current_state[move[0]]) - 1):
            if current_state[move[0]][i] != current_state[move[0]][i + 1]:
                h += 1

        for i in range(len(current_state[move[1]]) - 1):
            if current_state[move[1]][i] != current_state[move[1]][i + 1]:
                h += 1
        
        return h
    

    def calculate_heuristic_V2(self, current_state: list[list[int]]) -> int:
        "this function calculate h(n) based on different colors in each tube -> version 2(fastest)"

        bag = set()
        h = 0

        for tube in current_state:
            for i in range(len(tube) - 1):
                if tube[i] != tube[i + 1]:
                    h += 1
            if len(tube) >= 1:
                h += 1

        for i in range(len(current_state)):
            if len(current_state[i]):
                bag.add(current_state[i][0])

        h -= len(bag)

        return h
              

    def initialize_pq(self, current_state, queue):
        """a function to add initial states in the queue"""
        
        possible_moves = self.all_moves(current_state)
        for move in possible_moves:
            current_state_copy = copy.deepcopy(current_state)
            self.move_water(move[0], move[1], current_state_copy)
            h = self.calculate_heuristic_V2(current_state_copy)
            new_state = State(current_state_copy, 1, h, None, move)
            heapq.heappush(queue, (h, new_state))

        
    def optimal_solve(self, current_state):
        """
            Find an optimal solution to the Water Sort game from the current state.

            Args:
                current_state (List[List[int]]): A list of lists representing the colors in each tube.

            This method attempts to find an optimal solution to the Water Sort game by minimizing
            the number of moves required to complete the game, starting from the current state.
        """
        
        priority_queue = []
        self.initialize_pq(current_state, priority_queue)
        
        counter = 0
        while priority_queue:
            
            node = heapq.heappop(priority_queue)[1]

            if self.ws_game.check_victory(node.values):
                self.solution_found = True
                break

            if str(node.values) in self.visited_tubes:
                continue

            self.visited_tubes.add(str(node.values))
            possible_moves = self.all_moves(node.values)
            for move in possible_moves:
                counter += 1
                current_state_copy = copy.deepcopy(node.values)
                self.move_water(move[0], move[1], current_state_copy)
                new_h = self.calculate_heuristic_V2(current_state_copy)
                new_g = node.g + 1
                new_state = State(current_state_copy, new_g, new_h, node, move)
                heapq.heappush(priority_queue, (new_h + new_g, new_state))

        # Creating self.moves list
        if self.solution_found:
            while node.parent_state != None:
                self.moves.append(node.move)
                node = node.parent_state
            self.moves.append(node.move)
            self.moves.reverse()