"""
8-puzzle using UCS algorithm
Edit by Phan Hong Son
Project AI Ho Chi Minh University of Technology and Education
"""

import numpy as np
from sys import exit

size = 3

class Node:
    def __init__(self, node_number, data, parent, act, cost):
        self.node_number = node_number
        self.data = data
        self.parent = parent
        self.act = act
        self.cost = cost
        
    def __lt__(self, other):
        if other == None:
            return False
        return self.cost < other.cost 
    
    
    def __eq__(self, other):
        if other == None:
            return False
        return self.data.tolist() == other.data.tolist()
        
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

# Find index 0 in Puzzle
def find_index(puzzle):
    i, j = np.where(puzzle == 0)
    i = int(i)
    j = int(j)
    return i, j

def move_left(data):
    i, j = find_index(data)
    if j == 0:
        return None
    else:
        temp_arr = np.copy(data)
        temp_arr[i][j] = temp_arr[i][j - 1]
        temp_arr[i][j - 1] = 0
        return temp_arr
    
def move_right(data):
    i, j = find_index(data)
    if j == size - 1:
        return None
    else:
        temp_arr = np.copy(data)
        temp_arr[i][j] = temp_arr[i][j + 1]
        temp_arr[i][j + 1] = 0
        return temp_arr
        
def move_up(data):
    i, j = find_index(data)
    if i == 0:
        return None
    else:
        temp_arr = np.copy(data)
        temp_arr[i][j] = temp_arr[i - 1][j]
        temp_arr[i - 1][j] = 0
        return temp_arr
    
def move_down(data):
    i, j = find_index(data)
    if i == size - 1:
        return None
    else:
        temp_arr = np.copy(data)
        temp_arr[i][j] = temp_arr[i + 1][j]
        temp_arr[i + 1][j] = 0
        return temp_arr
        
def move_title(action, data):
    if action == "up":
        return move_up(data)
    else:
        if action == "down":
            return move_down(data)
        else:
            if action == "right":
                return move_right(data)
            else:
                if action == "left":
                    return move_left(data)  
                else:
                    return None

def print_states(list_final):  # To print the final states on the console
    print("Printing final solution")
    step = int(0)
    for l in list_final:
        print("Step " + str(step) + ":Move " + str(l.act) + "\n" + "Result : " + "\n" + str(l.data) + "\t" + "node number:" + str(l.node_number))
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

def exploring_nodes(node):
    print("Exploring Nodes")
    actions = ["up", "left", "down", "right"]
    goal_state = np.array([[3, 5, 6], [1, 2, 4], [8, 0, 7]])
    fringe = [node]
    # To check if the current state was seen
    checked_node = []
    node_count = int(0)
    
    while fringe:
        current_node = fringe.pop(0)
        if current_node.data.tolist() == goal_state.tolist():
            return current_node
        
        checked_node.append(current_node)
        for i in actions:
            temp = move_title(i, current_node.data)  
            if temp is not None:                       
                node_count += 1
                child_node = Node(node_count, temp, current_node, i, current_node.cost + 1) 
                if child_node not in fringe and child_node not in checked_node:
                    fringe.append(child_node)
        fringe.sort()                                         
    return None

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
    check_correct_input(k)
    
    root = Node(0, k, None, None, 0)
    
    # Call DFS algorithm
    goal = exploring_nodes(root)
    
    if goal is None:
        print("Goal State could not be reached, Sorry")
    else:
        # Print and write the final output
        print_states(path(goal))
    
    