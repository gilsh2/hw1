from typing import Set, Dict, Tuple, Optional, Sequence, List
import heapq
import math
import time

Map = List[List[str]]
Point = Tuple[int, int]

def manhattan_distance(p1:Point, p2:Point) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def astar(terrain:Map, start:Point, goal:Point) -> Tuple[int, int, Optional[List[Point]]]:
    open_list: List[Tuple[int, Point]] = [(0, start)]         
    best_costs: Dict[Point, Tuple[int, Point]] = {start:(0, start)}
    visit_count = 0
    found = False
    while open_list:
        # Dijkstra's search uses the priority queue data structure
        dummycost, node = heapq.heappop(open_list)  
        cost,point = best_costs.get(node)
                
        #print(node)
       
        if(compare_points(node,goal)):
            #print ("found it") 
            found = True;
            break;
                
        visit_count += 1
         
        neighbors = find_neighbors(terrain, node)
        for neighbor, neighbor_cost in neighbors:
            estimated=manhattan_distance(neighbor,goal)
            if(neighbor in  best_costs):
                #print("found=" , neighbor)     
                ncost,npoint = best_costs.get(neighbor)
                
                if(ncost > cost + neighbor_cost) :        
                    #print("update cost for ", neighbor ,"newcost", cost + neighbor_cost)
                    best_costs[neighbor] = ( cost + neighbor_cost ,  node )   
                    heapq.heappush (open_list,  (cost + neighbor_cost + estimated,  (neighbor) ) )     
            else:    
                    #print(neighbor ,"newcost", cost + neighbor_cost)
                    best_costs[neighbor] = ( cost + neighbor_cost ,  node )    
                    heapq.heappush (open_list,  (cost + neighbor_cost + estimated,  (neighbor) ) )       
                    
    if(found == False) :                   
        return (visit_count, -1, None)
    
   
    node = goal
    bestcost,point = best_costs.get(node)   
    retpath: List[Point] = []
    while(1):       
        cost,point = best_costs.get(node)          
        retpath.insert(0,node)
        if(compare_points(point,start)) :
            retpath.insert(0,point)
            break;
        node = point
     
    print("bestcost" ,bestcost    )
    print("path" ,retpath    )
   
 
    return (visit_count, bestcost, retpath)    




def best_first(terrain:Map, start:Point, goal:Point) -> Tuple[int, int, Optional[List[Point]]]:
    # In the open list we use heuristic values as the priority
    open_list: List[Tuple[int, Point]] = [(manhattan_distance(start, goal), start)]
    # But in best_costs we still want to track real costs
    best_costs: Dict[Point, Tuple[int, Point]] = {start:(0, start)}
    visit_count = 0
    found = False
    while open_list:
        # Dijkstra's search uses the priority queue data structure
        dummycost, node = heapq.heappop(open_list)              
        #print(node)
       
        if(compare_points(node,goal)):            
            #print(node,goal)
            found = True;
            break;
        visit_count += 1        
        
        neighbors = find_neighbors(terrain, node)       
        for neighbor, neighbor_cost in neighbors:
            if(neighbor in  best_costs):
                #print("found=" , neighbor)     
                continue
            else:    
                    cost,point = best_costs.get(node)#print(neighbor ,"newcost", cost + neighbor_cost)
                    best_costs[neighbor] = ( cost + neighbor_cost ,  node )                   
                    heapq.heappush (open_list,  ( manhattan_distance(neighbor, goal),  neighbor ) )     
                    
    if(found == False) :                   
        return (visit_count, -1, None)
    

   
    node = goal
    bestcost,point = best_costs.get(node)   
    retpath: List[Point] = []
    while(1):       
        cost,point = best_costs.get(node)          
        retpath.insert(0,node)
        if(compare_points(point,start)) :
            retpath.insert(0,point)
            break;
        node = point
     
    print("bestcost" ,bestcost    )
    print("path" ,retpath    )
   
 
    return (visit_count, bestcost, retpath)    

 

def dijkstra(terrain:Map, start:Point, goal:Point) -> Tuple[int, int, Optional[List[Point]]]:
    open_list: List[Tuple[int, Point]] = [(0, start)]         
    best_costs: Dict[Point, Tuple[int, Point]] = {start:(0, start)}
    visit_count = 0
    found = False
    while open_list:
        # Dijkstra's search uses the priority queue data structure
        cost, node = heapq.heappop(open_list)       
        #print(node)
       
        if(compare_points(node,goal)):
            #print ("found it") 
            found = True;
            break;
                
        visit_count += 1
         
        neighbors = find_neighbors(terrain, node)
        for neighbor, neighbor_cost in neighbors:
            if(neighbor in  best_costs):
                #print("found=" , neighbor)     
                ncost,npoint = best_costs.get(neighbor)
                if(ncost > cost + neighbor_cost) :        
                    #print("update cost for ", neighbor ,"newcost", cost + neighbor_cost)
                    best_costs[neighbor] = ( cost + neighbor_cost ,  node )   
                    heapq.heappush (open_list,  (cost + neighbor_cost,  (neighbor) ) )     
            else:    
                    #print(neighbor ,"newcost", cost + neighbor_cost)
                    best_costs[neighbor] = ( cost + neighbor_cost ,  node )    
                    heapq.heappush (open_list,  (cost + neighbor_cost,  (neighbor) ) )       
                    
    if(found == False) :                   
        return (visit_count, -1, None)
    
   
    node = goal
    bestcost,point = best_costs.get(node)   
    retpath: List[Point] = []
    while(1):       
        cost,point = best_costs.get(node)          
        retpath.insert(0,node)
        if(compare_points(point,start)) :
            retpath.insert(0,point)
            break;
        node = point
     
    print("bestcost" ,bestcost    )
    print("path" ,retpath    )
   
 
    return (visit_count, bestcost, retpath)    

 
   

def breadth_first(terrain:Map, start:Point, goal:Point) -> Tuple[int, int, Optional[List[Point]]]:
    open_list: List[Point] = [start]   
 
    # We'll treat start specially
    best_costs: Dict[Point, Tuple[int, Point]] = {start:(0, start)}
    visit_count = 0
    found_count = 0
    while open_list:
        # Breadth-first search takes the first thing from the list...
        node = open_list.pop(0)
       
        cost,point = best_costs.get(node)     
        #print("node=",node,"cost=",cost)
        
        if(compare_points(node,goal)):
            #print ("found it") 
            found_count += 1;
            continue
        
        visit_count += 1
        
        neighbors = find_neighbors(terrain, node)
        #print(neighbors)      
        for neighbor, neighbor_cost in neighbors:   
            if(neighbor in  best_costs):
                #print("found=" , neighbor)     
                ncost,npoint = best_costs.get(neighbor)
                if(ncost > cost + neighbor_cost) :        
                    #print("update cost for ", neighbor ,"newcost", cost + neighbor_cost)
                    best_costs[neighbor] = ( cost + neighbor_cost ,  node )   
                    open_list.insert( len(open_list)  , (neighbor) )      
            else:    
                    #print(neighbor ,"newcost", cost + neighbor_cost)
                    best_costs[neighbor] = ( cost + neighbor_cost ,  node )    
                    open_list.insert( len(open_list)  , (neighbor) )                                                          
                      
                    #print("new=" , neighbor,open_list)  
                        
                  
    if(found_count == 0):
          return (visit_count, -1, None)                         
    
   
    node = goal
    bestcost,point = best_costs.get(node)   
    retpath: List[Point] = []
    while(1):       
        cost,point = best_costs.get(node)          
        retpath.insert(0,node)
        if(compare_points(point,start)) :
            retpath.insert(0,point)
            break;
        node = point
     
    print("bestcost" ,bestcost    )
    print("path" ,retpath    )
    print("found_count" , found_count )   
 
    return (visit_count, bestcost, retpath)    

       
   
    

def compare_points(p1:Point, p2:Point) -> bool:
    return (p1[0] == p2[0] and   p1[1] == p2[1] )

def pretty_print_path(terrain: Map, path: List[Point]):
    emojis = ['😀','😁','😂','🤣','😃','😄','😅','😆','😉','😊','😋']
    # This is a "dictionary comprehension" like the list comprehension above
    path2len = {location:distance for distance,location in enumerate(path)}
    output = []
    for yy,row in enumerate(terrain):
        row_str = ''
        for xx, cur in enumerate(row):
            if (xx,yy) in path2len:
                row_str += emojis[path2len[(xx,yy)] % len(emojis)]
            else:
                row_str += cur
        output.append(row_str)
    return '\\n'.join(output)

def print_search_result(terrain:Map, result:Tuple[int, int, Optional[List[Point]]]) -> None:
    print("Visited:",result[0])
    if result[2]:
        print("Best path cost:",result[1])
        print(pretty_print_path(terrain, result[2]))
    else:
        print("No path found")



def find_neighbors(terrain:Map, p:Point) -> List[Tuple[Point, int]]:
    # Python has destructuring assignment.
    # You could just as well write `x = p[0]` and `y = p[1]`.
    
    x,y = p
    neighbors : List[Tuple[Point,int]] = []
    if(x-1) >= 0 :
        cost = cordinate_to_cost(terrain,x-1,y)
        neighbors.append  ( ( (x-1,y) ,cost)    )
    if (y-1) >= 0 :  
        cost = cordinate_to_cost(terrain,x,y-1)
        neighbors.append ( ((x,y-1) ,cost)    )
    if (x+1) <= len(terrain[0])-1 :  
        cost = cordinate_to_cost(terrain,x+1,y)
        neighbors.append ( ((x+1,y) ,cost)    )    
    if (y+1) <= len(terrain) -1 :        
       cost = cordinate_to_cost(terrain,x,y+1)
       neighbors.append ( ((x,y+1) ,cost)    )        
   
    # Feel free to introduce other variables if they'd be helpful too.
    return neighbors



def cordinate_to_cost (terrain: Map, x:int, y:int ):
   
    if terrain[y][x]  == '🌿' or  terrain[y][x] ==  '🌲' or  terrain[y][x] == '🌉' :
        return 1
    
    if terrain[y][x] == '🌼' :
        return 2
    
    if terrain[y][x] == '🌊' :
        return 5
    
    raise ValueError(terrain[x][y] + " is not valid")



# Now we can write load_map in terms of Map:
def load_map(mapfile:str) -> Map:
    with open(mapfile,encoding='utf-8') as infile:
        # This "list comprehension" is a very useful syntactic trick
        return [list(line.rstrip()) for line in infile]
# Example
terrain = load_map('terrain.txt')
for x in enumerate(terrain):
    print(x)
 

#print("Best_First (2,3) -> (7,0)")
#visited, cost, path, dt = run_trial(t, best_first, (2, 3), (7, 0))
#expect_nearly(visited, 8, 0.1, "Visit count")
#expect_exactly(cost, 10, "Optimal path cost...?")
#expect_path(path, t, 10, (2, 3), (7, 0), [(2, 3), (2, 2), (2, 1), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)], "Optimal path...?")

 
#print(find_neighbors(terrain, (0,3)))
#print(find_neighbors(terrain, (9,0)))
#sPoint  = (2,3)
#ePoint = (7,0)
#print_search_result(terrain, breadth_first(terrain, sPoint, ePoint))
#print_search_result(terrain, dijkstra(terrain, sPoint, ePoint))
#print_search_result(terrain, best_first(terrain, sPoint, ePoint))

