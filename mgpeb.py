
from collections import deque
from dataclasses import dataclass
from typing import Optional, List, Tuple, Any
from enum import Enum
import time
import random
import math

# =============================================================================
# [0] Utils
# =============================================================================

def time_distance(distance: float, speed: float) -> float:
    """Calculates the time needed to travel a certain distance at a given speed."""
    if speed <= 0:
        return float('inf')
    return distance / speed


def descent_altitude(t: float, h0: float = 2000.0, v0: float = 80.0, a: float = 3.7) -> float:
    """Calculates the altitude of the module during descent using the formula: h(t) = h0 - v0·t - 0.5·a·t²"""
    return max(0.0, h0 - v0 * t - 0.5 * a * t ** 2)


def fuel_consumption_rate(v: float, c0: float = 10.0, k: float = 0.02) -> float:
    """Calculates the fuel consumption rate using the formula   : C(v) = C₀ · e^(k·v)"""
    return c0 * math.exp(k * v)


def solar_energy(t: float, t_mid: float = 12.3, e_max: float = 2200.0, a: float = 15.0) -> float:
    """ Solar energy : E(t) = -a·(t - t_mid)² + E_max"""
    return max(0.0, -a * (t - t_mid) ** 2 + e_max)


# =============================================================================
# [1] Data - Classes struct
# =============================================================================

class ModuleType(Enum):
    HABITAT = "habitation"
    ENERGY = "energy"
    LAB = "laboratory"
    LOGISTIC = "Logistic"
    MEDICAL = "Medical support"
    
class AtmosfericClassifier(Enum):
    GREEN = "OK"
    YELLOW = "CAUTION"
    RED = "DANGER"
    
class LandingStatus(Enum):
    WAITING = "Waiting autorization"
    AUTORIZED = "Autorized stop"
    DENIED = "Denied stop"
    EMERGENCY = "Emergency post"
    STOPPED = "Stopped"
    
@dataclass
class Module: 
    """
    Represents a module to Mars
    """
    
    id: int
    type: ModuleType
    weight: float
    arrival_time: float
    stop_condition: LandingStatus = LandingStatus.WAITING
    fuel_level: float = 100.0
    priority: int = 0
    speed : float = 0.0
    sensor_ok: bool
    module_integrity: float = 100.0
    status : str = "In transit"
    
    def __str__(self):
        return f"Module {self.id} - Type: {self.type.value}, Weight: {self.weight}kg, Arrival: {time.ctime(self.arrival_time)}, Condition: {self.stop_condition.value}, Speed: {self.speed}km/h, Integrity: {self.module_integrity}%"
    
    def __lt__(self, other):
        """Defines the less-than operator for sorting modules by priority."""
        return self.priority < other.priority
    
# === Algorithms for searching and sorting === 

class SearchAlgorithms:
    
    @staticmethod
    def linear_search(modules_list: List[Any], target: Any) -> Optional[int]:
        """
        Performs a linear search for the target item in the list.
        
        Args:
                modules_list: A list of Module objects to search through.
                target: The item to search for in the list.
        Returns:
                The index of the target item if found, otherwise None.
        """
        
        if modules_list is None:
            raise ValueError("The list to search cannot be None.")
        elif target is None:
            raise ValueError("The target to search cannot be None.")
            
        begin_time = time.perf_counter()
        comparation = 0
        
        for index, module in enumerate(modules_list):
            comparation += 1 
            
            if hasattr(module, 'id') and module.id == target:
            
                end_time = time.perf_counter()
                
                print(
                    f"Linear search found target {target} at index {index} " 
                    f"in {end_time - begin_time:.6f} seconds"
                    f" with {comparation} comparisons."
                )
                
                return index
        
        print(
            f"Linear search did not find target {target} after " 
            f"{time.perf_counter() - begin_time:.6f} seconds with {comparation} comparisons."
        )
        return None # Return None if target is not found
    
    @staticmethod
    def binary_search(sorted_modules: List[Any], target: Any) -> Optional[int]:
        """
        Performs a binary search for the target item in a sorted list.
        
        Args:
                sorted_modules: A list of items that is already sorted.
                target: The item to search for in the list.
        Returns:
                The index of the target item if found, otherwise None.
        """
        
        if sorted_modules is None:
            raise ValueError("The list to search cannot be None.")
        elif target is None:
            raise ValueError("The target to search cannot be None.")
            
        begin_time = time.perf_counter()
        comparation = 0
        left, right = 0, len(sorted_modules) - 1
        
        while left <= right:
            mid = (left + right) // 2
            comparation += 1
            
            if hasattr(sorted_modules[mid], 'id') and sorted_modules[mid].id == target:
                end_time = time.perf_counter()
                
                print(
                    f"Binary search found target {target} at index {mid} " 
                    f"in {end_time - begin_time:.6f} seconds"
                    f" with {comparation} comparisons."
                )
                
                return mid
            elif hasattr(sorted_modules[mid], 'id') and sorted_modules[mid].id < target:
                left = mid + 1
            else:
                right = mid - 1
        
        end_time = time.perf_counter()
        
        print(
            f"Binary search did not find target {target} after " 
            f"{end_time - begin_time:.6f} seconds with {comparation} comparisons."
        )
        
        return None # Return None if target is not found
    
    @staticmethod
    def priority_module(list_to_modules: List[Module], priority : int) -> List[Module]:
        """
        Searches all modules in the list with priority for the target type.
        """
                
        return [module for module in list_to_modules if module.type.value == priority]

# Implementing sorting algorithms for the modules based on their priority and arrival time
class SortAlgorithms: 
    
    @staticmethod
    def bubble_sort(modules: List[Module], camp: str=  "priority") -> List[Module]:
        """
        Sorts a list of modules using the Bubble Sort algorithm.
        Args:
                modules: A list of Module objects to be sorted.
        Returns: 
                A new list of Module objects sorted by priority .
        """
        
        if modules is None:
            raise ValueError("The list of modules cannot be None.")
        elif camp not in ["priority"]:
            raise ValueError("The sorting camp must be either 'priority'.")
        
        begin = time.perf_counter()
        comparation = 0

        len_modules = len(modules)
        
        modules_copy = modules.copy()  # Create a copy of the list to avoid modifying the original
                
        for first in range(len_modules - 1):
            for second in range(0, len_modules - first - 1):
                comparation += 1
                swapped = False
                
                if camp == "priority":
                    if modules_copy[second].priority > modules_copy[second + 1].priority:
                        modules_copy[second], modules_copy[second + 1] = modules_copy[second + 1], modules_copy[second]
                        swapped = True
                
            if not swapped:
               break  # No swaps means the list is already sorted, so we can exit early
        
        end = time.perf_counter()
        print(f"Bubble sort completed in {end - begin:.6f} seconds.")
        print(f"Total comparisons made: {comparation}.")
        
        return modules_copy , (end - begin) * 1000, comparation
    
    @staticmethod
    def quick_sort(modules: List[Module], camp: str=  "priority") -> List[Module]:
        """
        Sorts a list of modules using the Quick Sort algorithm.
        Args:
                modules: A list of Module objects to be sorted.
        Returns: 
                A new list of Module objects sorted by priority.
        """
        
        if modules is None: 
            raise ValueError("The list of modules cannot be None.")
        elif camp not in ["priority", "arrival_time"]:
            raise ValueError("The sorting camp must be eithr 'priority'.")
        
        begin = time.perf_counter()
        comparation = 0
        
        def _quick_sort(arr):
            """_summary_
            quick sort implementation for sorting modules by priority.
            
            Args:
                    arr: A list of Module objects to be sorted.
            Returns:
                    A new list of Module objects sorted by priority.
            """
            if len(arr) <= 1:
                return arr
            
            pivot = arr[len(arr) // 2] 
            
            less = []
            equal = []
            greater = []
            
            for modules in arr:
                
                comparation += 1 
                
                if camp == "priority": 
                    if modules.priority < pivot.priority:
                        less.append(modules)
                    elif modules.priority == pivot.priority:
                        equal.append(modules)
                    else:
                        greater.append(modules)

            
            return _quick_sort(less) + equal + _quick_sort(greater) # Recursively sort the less and greater partitions and concatenate the results
        
        sorted_modules = _quick_sort(modules)
        end = time.perf_counter()
        
        return sorted_modules, (end - begin) * 1000, comparation
    
    @staticmethod
    def merge_sort(modules: List[Module], camp: str=  "priority"):
        """_summary_

        Args:
            modules (List[Module]): _description_
            camp (str, optional): _description_. Defaults to "priority".
        """
        
        if modules is None: 
            raise ValueError("The list of modules cannot be None.")
        elif camp not in ["priority"]:
            raise ValueError("The sorting camp must be 'priority'.")
        
        begin = time.perf_counter()
        comparation = 0
        
        def merge(left: List[Module], right: List[Module]) -> List[Module]:
            merged = []
            i = j = 0
            
            while i < len(left) and j < len(right):
                comparation += 1
                
                if camp == "priority":
                    if left[i].priority < right[j].priority:
                        merged.append(left[i])
                        i += 1
                    else:
                        merged.append(right[j])
                        j += 1
            
            merged.extend(left[i:])
            merged.extend(right[j:])
            return merged
        
        def _merge_sort_recursive(arr : List[Module]) -> List[Module]:
            if len(arr) <= 1:
                return arr
            
            mid = len(arr) // 2
            left_half = _merge_sort_recursive(arr[:mid])
            right_half = _merge_sort_recursive(arr[mid:])
            
            return merge(left_half, right_half)
            
            sorted_modules = _merge_sort_recursive(modules)
            end = (time.perf_counter() - begin) * 1000
            
            print(f"Merge sort completed in {end:.6f} seconds.")
            return sorted_modules, end, comparation
             

class LogicalGatesMGPEB:
    """
    Implement decision rules using boolean logic
    """
    
    @staticmethod
    def good_atmosferic_conditions(condition : AtmosfericClassifier) -> bool : 
        return condition in [AtmosfericClassifier.GREEN, AtmosfericClassifier.YELLOW]
    
    @staticmethod
    def enough_fuel(fuel_level: float, threshold: float) -> bool:
       return fuel_level > threshold # Arbitrary threshold for "enough" fuel\
           
    @staticmethod
    def safe_to_land(conditions: List[bool]) -> bool:
        return all(conditions)  # Safe to land if all conditions are True
    
    @staticmethod
    def integrity_ok(integrity: float) -> bool:
        return integrity > 75.0  # Arbitrary threshold for "ok" integrity
    
    @staticmethod
    def module_ready_for_landing(module: Module) -> bool:
        return (module.sensor_ok and 
                module.module_integrity > 80.0 and 
                module.stop_condition == LandingStatus.AUTORIZED)
        
    @staticmethod
    def emergency_stop_needed(module: Module) -> bool:
        return (module.fuel_level < 10.0 or 
                module.module_integrity < 50.0 or 
                module.stop_condition == LandingStatus.EMERGENCY)
    
class MGPEBSystem:    
    def __init__(self):
        self.waiting_modules : deque[Module] = deque()
        self.autorized_modules : List[Module] = []
        self.emergency_stack : List[Module] = []
        self.alert_log : List[str] = []
        
        self.logic = LogicalGatesMGPEB()
        self.search_algorithms = SearchAlgorithms()
        self.sort_algorithms = SortAlgorithms()
        
        self.next_id = 1  # To assign unique IDs to modules
        self.area_landing_released = True  # To track the landing area
        self.sensors_ok = True  # To track sensor status
        
    def module_registration(self, name:str, type: ModuleType, weight: float, arrival_time: float, sensor_ok: bool):
        module = Module(
            id=self.next_id,
            type=type,
            weight=weight,
            arrival_time=arrival_time,
            sensor_ok=sensor_ok
        )
        self.waiting_modules.append(module)
        self.next_id += 1
        print(f"Module {module.id} registered and added to waiting queue.")
        return module
    
    def generate_random_modules(self, num_modules: int) -> List['Module']:
        """
        Generates a list of random Module objects for testing purposes.
        
        Args:
                num_modules: The number of random modules to generate.
        Returns:
                A list of randomly generated Module objects.
        """
        
        module_types = list(ModuleType)
        stop_conditions = list(LandingStatus)
        
        random_modules = []
        
        for i in range(num_modules):
            module = Module(
                id= i + 1, # Assign unique ID starting from 1
                type=random.choice(module_types),
                weight=random.uniform(100.0, 1000.0),  # Random weight between 100 and 1000 kg
                arrival_time=time.time() + random.uniform(0, 10000),  # Random arrival time within the next 10,000 seconds
                sensor_ok=random.choice([True, False]), # Randomly set sensor status
                priority = int(time_distance(0, random.uniform(0, 10000)))  # based on the time arrival set the priority of the module, the less time to arrive the more priority it has.
            )
            random_modules.append(module)
        
        return random_modules
    
    def reoder_queue_by_priority(self):
        """Reorders the waiting queue based on module priority."""
        
        if len(self.waiting_modules) == 0:
            print("No modules in the waiting queue to reorder.")
            return 0,0
        
        queue_list = list(self.waiting_modules)
        sorted_queue, time_taken, comparisons = self.sort_algorithms.merge_sort(queue_list)
        self.waiting_modules = deque(sorted_queue)
        print(f"Waiting queue reordered by priority in {time_taken:.2f} ms with {comparisons} comparisons.")
        return time_taken, comparisons
        
    def evaluate_module_for_landing(self, module: Module) -> bool:
        """Evaluates if a module is ready for landing based on its attributes."""
        
        if self.logic.module_ready_for_landing(module):
            print(f"Module {module.id} is ready for landing.")
            module.stop_condition = LandingStatus.AUTORIZED
            return True
        elif self.logic.emergency_stop_needed(module):
            print(f"Module {module.id} is not ready for landing.")
            module.stop_condition = LandingStatus.DENIED
            return False
    
    
    
# Execute the main program

def comparing_searches_algorithms():
    pass

def comparing_sorting_algorithms():
    pass

def analysis_of_modules_performance():
    pass

def menu(running: bool = True):
    while running : 
        print("\n=== Mars Ground Processing and Entry/Descent/landing System (MGPEB) ===")
        print("1. Generate random modules")
        print("2. Search for a module by ID")
        print("3. Sort modules by priority")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
       