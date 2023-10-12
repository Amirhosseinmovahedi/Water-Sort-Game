class test:

    def has_capacity(self, tube_des: list) -> int:
            "returns capacity of that tube"
            return self.capacity - len(tube_des) 

    def counting_top(self, tube) -> int:
            """returns the number of similar colors in the top of the tube"""

            topest_color = tube[-1]
            total = 1
            for col in tube[:-1]:
                if col == topest_color:
                    total += 1

            return total



    def move_water(self, s: int, des: int, current_state: list[tuple]):
            """moves water from source tube to the destination tube"""
            
            current_state_copy = current_state.copy()
            counting_s = self.counting_top(current_state_copy[s])
            capacity_des = self.has_capacity(current_state_copy[des])
            n = min(counting_s, capacity_des)
            for i in range(n):
                current_state_copy[des].append(current_state_copy[s].pop())

            return current_state_copy
    
t = test()
t.move_water(0, 4, )