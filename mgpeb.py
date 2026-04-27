
from collections import deque
from dataclasses import dataclass
from typing import Optional, List, Tuple, Any
from enum import Enum
import time
import random

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
    
class StopCondition(Enum):
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
    stop_condition: StopCondition = StopCondition.WAITING
    fuel_level: float = 100.0
    priority: int = 0
    
    def __str__(self):
        return f"Module {self.id} - Type: {self.type.value}, Weight: {self.weight}kg, Arrival: {time.ctime(self.arrival_time)}, Condition: {self.stop_condition.value}"
    
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
                A new list of Module objects sorted by priority or arrival time.
        """
        
        if modules is None:
            raise ValueError("The list of modules cannot be None.")
        elif camp not in ["priority", "arrival_time"]:
            raise ValueError("The sorting camp must be either 'priority' or 'arrival_time'.")
        
        begin = time.perf_counter()
        comparation = 0

        len_modules = len(modules)
        
        modules_copy = modules.copy()  # Create a copy of the list to avoid modifying the original
        
        for first in range(len_modules - 1):
            for second in range(0, len_modules - first - 1):
                comparation += 1
    
                if camp == "priority":
                    if modules_copy[second].priority > modules_copy[second + 1].priority:
                        modules_copy[second], modules_copy[second + 1] = modules_copy[second + 1], modules_copy[second]
                        
                elif camp == "arrival_time":
                    if modules_copy[second].arrival_time > modules_copy[second + 1].arrival_time:
                        modules_copy[second], modules_copy[second + 1] = modules_copy[second + 1], modules_copy[second]
        
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
                A new list of Module objects sorted by priority or arrival time.
        """
        
        if modules is None: 
            raise ValueError("The list of modules cannot be None.")
        elif camp not in ["priority", "arrival_time"]:
            raise ValueError("The sorting camp must be either 'priority' or 'arrival_time'.")
        
        begin = time.perf_counter()
        comparation = 0
        
        def _quick_sort(arr):
            """_summary_
            quick sort implementation for sorting modules by priority or arrival time.
            
            Args:
                    arr: A list of Module objects to be sorted.
            Returns:
                    A new list of Module objects sorted by priority or arrival time.
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
                        
                elif camp == "arrival_time":
                    if modules.arrival_time < pivot.arrival_time:
                        less.append(modules)
                    elif modules.arrival_time == pivot.arrival_time:
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
        pass
            
            
        
        


# =============================================================================
# [3] REGRAS LÓGICAS — Autorização de pouso com expressões booleanas
# =============================================================================


# =============================================================================
# [4] BUSCA — Algoritmos de busca linear
#

# =============================================================================
# [6] FUNÇÕES MATEMÁTICAS — Modelagem de fenômenos do pouso
# =============================================================================


# =============================================================================
# [7] SIMULAÇÃO — Execução do pouso sequencial
# =============================================================================


# =============================================================================
# [8] EXIBIÇÃO E MENU — Interface com o operador
# =============================================================================


# Execute the main program
