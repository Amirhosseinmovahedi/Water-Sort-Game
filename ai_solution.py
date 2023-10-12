import copy

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

    def converted(self, data: list[list]) -> tuple[tuple]:
        """convert a list of lists to a hashable type"""

        arr = data.copy()
        for i in range(len(arr)):
            arr[i] = tuple(arr[i])
        
        arr = tuple(arr)

        return arr

    def has_capacity(self, tube_des: list) -> int:
        "returns capacity of that tube"
        return self.capacity - len(tube_des) 
            


    def all_moves(self, current_state):
        """returns all the possible moves with this state"""

        possible_moves = [] # a list of tuples
        for s in range(len(current_state)):
            if len(current_state[s]) == 0:
                continue
            for des in range(len(current_state)):
                if des == s:
                    continue

                if len(current_state[des]) == 0:
                    possible_moves.append((s, des))
                
                elif (current_state[s][-1] == current_state[des][-1]) and (self.has_capacity(current_state[des]) > 0):
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
        capacity_des = self.has_capacity(current_state[des])
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
            self.moves.pop()
            return

        if self.ws_game.check_victory(current_state):
            self.solution_found = True
            return

        all_moves = self.all_moves(current_state)
        if len(all_moves) == 0:
            self.moves.pop()
            return

        flag = True
        for move in all_moves:
            current_state_copy = copy.deepcopy(current_state)
            self.move_water(move[0], move[1], current_state_copy)
            if self.converted(current_state_copy) in self.visited_tubes:
                continue
            else:
                flag = False
                self.visited_tubes.add(self.converted(current_state_copy))
                self.moves.append(move)
                self.solve(current_state_copy)
        
        if not self.solution_found:
            self.moves.pop()
                

        




    def optimal_solve(self, current_state):
        """
            Find an optimal solution to the Water Sort game from the current state.

            Args:
                current_state (List[List[int]]): A list of lists representing the colors in each tube.

            This method attempts to find an optimal solution to the Water Sort game by minimizing
            the number of moves required to complete the game, starting from the current state.
        """
        pass
