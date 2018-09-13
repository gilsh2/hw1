import json
from typing import NamedTuple, Dict, Tuple, Optional, Sequence, List
import array
import heapq
import time
import itertools

with open('Crafting.json') as f:
    Crafting = json.load(f)
    


items_by_index: List[str] = Crafting['Items']
items_to_indices: Dict[str, int] = {
    item2: index2 for index2, item2 in enumerate(items_by_index)
}



class State:
    items: array.array

    def __init__(self, items: Optional[Sequence[int]] = None) -> None:
        if items is not None:
            # Copying a state from an old state.
            # This call to the array constructor creates an array of unsigned integers and initializes it from the contents of items.
            self.items = array.array('I', items)
        else:
            self.items = array.array('I', [0 for item in items_by_index])

    def __add__(self, other:'State') -> 'State':
        s = State(self.items)
        
        for i in range(len (other.items)) :
            s.items[i] = s.items[i] + other.items[i]
        # A. How do we add together the contents of two states?
        return s

    def __sub__(self, other:'State') -> 'State':
        s = State(self.items)
        for i in range(len (other.items)) :
            s.items[i] = max(s.items[i] - other.items[i],0)
        # B. How do we subtract one state from another?
        return s

    def __ge__(self, other: 'State') -> bool:
        for i in range(len (other.items)) :
            if self.items[i] < other.items[i] :
                return False
        # C. How do we know whether one state (self) contains everything that's inside of another (other)? 
        return True

    def __lt__(self, other: 'State') -> bool:
        return not (self >= other)

    def __eq__(self, other) -> bool:
        return self.items == other.items

    def __hash__(self) -> int:
        hsh = 5381
        for s in self.items:
            hsh = ((hsh << 5) + hsh) + s
        return hsh

    def __str__(self) -> str:
        return self.to_dict().__str__()

    def to_dict(self) -> Dict[str, int]:
        return {items_by_index[idx]: self.items[idx]
                for idx in range(len(self.items))}

    @classmethod
    def from_dict(cls, item_dict: Dict[str, int]) -> 'State':
        return cls([
            item_dict.get(item,0) for item in items_by_index
        ])

class Recipe(NamedTuple):    
    produces: State
    consumes: State
    requires: State
    cost: int
    
def preconditions_satisfied(state: State, recipe: Recipe) -> bool:
  
    if ( state >= recipe.requires and state >= recipe.consumes) :
        return True
    
    return False

def apply_effects(state: State, recipe: Recipe) -> State:
    # E. How do you make a new state out of a state and a recipe?
    # Note, DO NOT change state in-place!
     newstate  =  state - recipe.consumes + recipe.produces
    
     return newstate 
   
    

def plan_dijkstra(initial: State, goal: State, limit:int) -> Tuple[int, int, Optional[List[str]]]:
    start_time = time.time()
    open_list: List[Tuple[int, State,str]] = [(0, initial, "")]         
    best_costs: Dict[State, Tuple[int, str,State]] = {initial:(0, "",initial)}
    visit_count = 0
    found = False
    while open_list:
        # Dijkstra's search uses the priority queue data structure
        cost, curstate , gotfrom  = heapq.heappop(open_list)       
        #print("cost=",cost,"curstate=",curstate,"from=",gotfrom)
       
        if(curstate >= goal):
            print ("found it!! Number of visited nodes=" ,visit_count , ". time it took=", time.time()-start_time,"seconds") 
            found = True;
            break;
                
        visit_count += 1
        if(visit_count > limit) :
            print("too many iterations , current state=",curstate)            
            break
        
        
                 
        for candidaterecipename in recipes:
            if (preconditions_satisfied(curstate,recipes[candidaterecipename])) == False:
                continue 
            
            candidatestate = apply_effects(curstate,recipes[candidaterecipename])
            
            if(candidatestate in  best_costs):
                #print("found=" , neighbor)     
                candidatestate_cost,rname,fromstate = best_costs.get(candidatestate)
                if(candidatestate_cost > cost + recipes[candidaterecipename].cost) :        
                    #print("update cost for ", neighbor ,"newcost", cost + neighbor_cost)
                    best_costs[candidatestate] = (cost + recipes[candidaterecipename].cost ,  gotfrom, curstate )   
                    heapq.heappush (open_list,  (cost + recipes[candidaterecipename].cost, candidatestate,  candidaterecipename ) )     
            else:    
                    #print(neighbor ,"newcost", cost + neighbor_cost)
                    best_costs[candidatestate] = (cost + recipes[candidaterecipename].cost ,  gotfrom,curstate )   
                    heapq.heappush (open_list,  (cost + recipes[candidaterecipename].cost, candidatestate,  candidaterecipename ) )     
                    
    if(found == False) :                   
        return (visit_count, -1, None)
    
    
    state  = curstate
    bestcost,dummy1,dummy2 = best_costs.get(state)   
    retpath: List[str] = []
    while(1):       
        cost,rname,fromstate  = best_costs.get(state)      
        if(rname == "") :           
            break;
        retpath.insert(0,rname)       
        state = fromstate
      
   
    return (visit_count, bestcost, retpath)       
    
recipes: Dict[str, Recipe] = {}
for name, rule in Crafting['Recipes'].items():
    recipes[name] = Recipe(
        State.from_dict(rule.get('Produces', {})),
        State.from_dict(rule.get('Consumes', {})),
        State.from_dict({item: 1 if req else 0
                         for item, req in rule.get('Requires', {}).items()}),
        rule['Time']
    )    
#print(items_to_indices)

#print(Crafting['Items'])
#print(Crafting['Goal'])
#print(Crafting['Recipes']['craft stone_pickaxe at bench'])  
# Example
initial = State.from_dict({'stone_pickaxe':1, 'ingot':2})
goal = State.from_dict({'ingot':1})
assert(initial >= goal)
#print("initial",initial)
#print("goal",goal)
#all = initial + goal
#print("all",initial + goal)

print(plan_dijkstra(State.from_dict({}),
                    State.from_dict({'stone_pickaxe':1}),
                    200000))
print(plan_dijkstra(State.from_dict({'bench':1,'stone_pickaxe':1}),
                    State.from_dict({'ingot':1}),
                    200000))