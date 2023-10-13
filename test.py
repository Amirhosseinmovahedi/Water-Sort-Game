from heapq import heappush, heappop

class test:
    
    def __init__(self, value) -> None:
        self.value = value
    def __gt__(self, other):
        return other



   

t1 = test(1)
t5 = test(5)
t4 = test(4)
t3 = test(3)
t2 = test(2)

h = []
heappush(h, (5, t1))
heappush(h, (1, t2))
heappush(h, (1, t3))
heappush(h, (3, t4))
print(heappop(h))

a = [1, 2, 3]
a = list(reversed(a))
print(a)


