"""
8-puzzle using A* algorithm
Edit by Phan Hong Son
Project AI Ho Chi Minh University of Technology and Education
"""

import numpy as np

size = 3

class Node:
    def __init__(self, node_count = 0, data = None, parent = None, cost = 0, h = 0, 
                 operation = None):
        self.node_count = node_count
        self.data = data
        self.parent = parent
        self.cost = cost
        self.h = h
        self.operation = operation  
    
    def __lt__(self, other):
        if other == None:
            return False
        return self.cost + self.h < other.cost + other.h
    
    
    def __eq__(self, other):
        if other == None:
            return False
        return self.data.tolist() == other.data.tolist()
    

class Operator:
    def __init__(self, i):
        self.i = i
        
    def find_pos(self, puzzle):
        i, j = np.where(puzzle == 0)
        i = int(i)
        j = int(j)
        return i, j
        
    def Up(self, puzzle):
        if self.check_state_null(puzzle.tolist()):
            return None
        x, y = self.find_pos(puzzle)
        if x == 0:
            return None
        return self.swap(puzzle, x, y)
    
    def Down(self, puzzle):
        if self.check_state_null(puzzle.tolist()):
            return None
        x, y = self.find_pos(puzzle)
        if x == size - 1:
            return None
        return self.swap(puzzle, x, y)
    
    def Left(self, puzzle):
        if self.check_state_null(puzzle.tolist()):
            return None
        x, y = self.find_pos(puzzle)
        if y == 0:
            return None
        return self.swap(puzzle, x, y)
    
    def Right(self, puzzle):
        if self.check_state_null(puzzle.tolist()):
            return None
        x, y = self.find_pos(puzzle)
        if y == size - 1:
            return None
        return self.swap(puzzle, x, y)
    
    def Move(self, puzzle):
        if self.i == "up":
            return self.Up(puzzle)
        if self.i == "down":
            return self.Down(puzzle)
        if self.i == "left":
            return self.Left(puzzle)
        if self.i == "right":
            return self.Right(puzzle)
    
    def swap(self, puzzle, x, y):
        temp = np.copy(puzzle)
        x_new = x
        y_new = y
        if self.i == "up": # Up
            x_new -= 1
        if self.i == "down": # Down
            x_new += 1
        if self.i == "left": # Left
            y_new -= 1
        if self.i == "right": # Right
            y_new += 1
        temp[x][y] = temp[x_new][y_new]
        temp[x_new][y_new] = 0
        return temp
        
    def check_state_null(self, puzzle):
        return puzzle == None
    
# Get the beginning state for puzzle
def get_initial():
    print("Please enter the number from 0-8, no number should be repeated or be out of this range !")
    initial_state = np.zeros(size * size)
    for i in range(size * size):
        states = int(input("Enter the " + str(i + 1) + " number: "))
        if states < 0 or states > 8:
            print("System was stopped because you enter the number is out of range [0-8]")
            exit(0)
        else:
            initial_state[i] = states
    return np.reshape(initial_state, (size, size))

# To print the final states on the console   
def print_states(list_final):  
    print("Printing final solution")
    step = int(0)
    for l in list_final:
        print("Step " + str(step) + ":Move " + str(l.operation) + "\n" + 
              "Result : " + "\n" + str(l.data) + "\t" + "g(x) = " + 
              str(l.cost) + "; h(x) = " + str(l.h) + "; Node number = " + str(l.node_count))
        step += 1
        
# To find the path from the beginning state to the goal state
def path(node):
    p = []
    p.append(node)
    parent_node = node.parent
    while parent_node is not None:
        p.append(parent_node)
        parent_node = parent_node.parent
    return list(reversed(p))

def exploring_nodes(node, goal_state):
    print("Exploring Nodes")
    actions = ["up", "down", "left", "right"]
    Open_queue = [node]
    Close_queue = []
    node_count = int(0)
    
    while Open_queue:
        current_node = Open_queue.pop(0)
        if current_node.data.tolist() == goal_state.tolist():
            return current_node
        if current_node not in Open_queue and current_node not in Close_queue:
            Close_queue.append(current_node)
            for i in range(4):
                op = Operator(actions[i])
                temp = op.Move(current_node.data) 
                if temp is not None:                       
                    node_count += 1
                    child_node = Node(node_count, temp, current_node, current_node.cost + 1,
                                      Hx(temp, goal_state), actions[i])              
                    Open_queue.append(child_node)
            # Open_queue.sort(key = lambda x : x.h + x.cost)
            Open_queue.sort()                                          
    return None

def Hx(S, G):
    res = 0
    temp_S = np.reshape(S, size * size)
    temp_G = np.reshape(G, size * size)
    for i in range(size * size):
        if temp_S[i] != temp_G[i]:
            res += 1
    return res

def check_correct_input(puzzle):
    array = np.reshape(puzzle, size * size)
    for i in range(size * size):
        count_appear = int(0)
        temp = array[i]
        for j in range(size * size):
            if temp == array[j]:
                count_appear += 1
        if count_appear > 1:
            print("Invalid input, same number entered 2 times")
            exit(0)
            
if __name__ == "__main__":
    k = get_initial()
    goal_state = np.array([[3, 5, 6], [1, 2, 4], [8, 0, 7]])
    check_correct_input(k)
    
    root = Node(0, k, None, 0, Hx(k, goal_state), None)
    
    # Call DFS algorithm
    goal = exploring_nodes(root, goal_state)
    
    if goal is None:
        print("Goal State could not be reached, Sorry")
    else:
        # Print and write the final output
        print_states(path(goal))



    
    
        