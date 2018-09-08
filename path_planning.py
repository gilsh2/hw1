from typing import Set, Dict, Tuple, Optional, Sequence, List
import heapq
import math
import time

# This is how we write a type alias in Python
Map = List[List[str]]
# Now we can write load_map in terms of Map:
def load_map(mapfile:str) -> Map:
    with open(mapfile,encoding='utf-8') as infile:
        # This "list comprehension" is a very useful syntactic trick
        return [list(line.rstrip()) for line in infile]

terrain = load_map('terrain.txt')

Point = Tuple[int, int]

# Now we can define our function in terms of Points
def find_neighbors(terrain:Map, p:Point) -> List[Tuple[Point, int]]:
    # Python has destructuring assignment.
    # You could just as well write `x = p[0]` and `y = p[1]`.
    x,y = p
    neighbors : List[Tuple[Point,int]] = []
    # A. Your code here...
    west = (x - 1, y)
    east = (x + 1, y)
    north = (x, y - 1)
    south = (x, y + 1)
    neighbors += (west, cost_of_point(west))
    neighbors += (east, cost_of_point(east))
    neighbors += (north, cost_of_point(north))
    neighbors += (south, cost_of_point(south))
    # Feel free to introduce other variables if they'd be helpful too.
    return neighbors

def cost_of_point(p:Point):
    x, y = p
    if terrain[x][y] == "🌿" or terrain[x][y] == "🌉" or terrain[x][y] == "🌲":
        return 1
    elif terrain[x][y] == "🌼":
        return 2
    elif terrain[x][y] == "🌊":
        return 5

print(terrain)
print(find_neighbors(terrain, (3,3)))
