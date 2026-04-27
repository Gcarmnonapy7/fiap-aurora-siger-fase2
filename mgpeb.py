
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
    
    def __str__(self):
        return f"Module {self.id} - Type: {self.type.value}, Weight: {self.weight}kg, Arrival: {time.ctime(self.arrival_time)}, Condition: {self.stop_condition.value}"
    
    def __lt__(self, other):
        """Defines the less-than operator for sorting modules by arrival time."""
        return self.arrival_time < other.arrival_time
    
# === Algorithms for searching and sorting === 

class SearchAlgorithms:
    
    @staticmethod
    def linear_search(list_to_search: List[Any], target: Any) -> Optional[int]:
        """
        Performs a linear search for the target item in the list.
        
        Args:
                list: A list of items to search through.
                target: The item to search for in the list.
        Returns:
                The index of the target item if found, otherwise None.
        """
        
        if list_to_search is None:
            raise ValueError("The list to search cannot be None.")
        elif target is None:
            raise ValueError("The target to search cannot be None.")
            
        begin_time = time.perf_counter()
        comparation = 0
        
        for index, module in enumerate(list_to_search):
            comparation += 1 
            
            if hasattr(module, 'id') and module.id == target:
            
                end_time = time.perf_counter()
                
                print(
                    f"Linear search found target {target} at index {index} " 
                    f"in {end_time - begin_time:.6f} seconds"
                    f" with {comparation} comparisons."
                )
                
                return index
        
        return None # Return None if target is not found
    
    @staticmethod
    def binary_search(sorted_list: List[Any], target: Any) -> Optional[int]:
        """
        Performs a binary search for the target item in a sorted list.
        
        Args:
                sorted_list: A list of items that is already sorted.
                target: The item to search for in the list.
        Returns:
                The index of the target item if found, otherwise None.
        """
        
        if sorted_list is None:
            raise ValueError("The list to search cannot be None.")
        elif target is None:
            raise ValueError("The target to search cannot be None.")
            
        begin_time = time.perf_counter()
        comparation = 0
        left, right = 0, len(sorted_list) - 1
        
        while left <= right:
            mid = (left + right) // 2
            comparation += 1
            
            if hasattr(sorted_list[mid], 'id') and sorted_list[mid].id == target:
                end_time = time.perf_counter()
                
                print(
                    f"Binary search found target {target} at index {mid} " 
                    f"in {end_time - begin_time:.6f} seconds"
                    f" with {comparation} comparisons."
                )
                
                return mid
            elif hasattr(sorted_list[mid], 'id') and sorted_list[mid].id < target:
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
    def priority_linear(list_to_modules: List[Module], priority : int) -> List[Module]:
        """
        Searches all modules in the list with priority for the target type.
        """
                
        return [module for module in list_to_modules if module.type.value == priority]
          
# =============================================================================
# [2] ESTRUTURAS LINEARES — Operações de fila, pilha e verificação
# =============================================================================


# =============================================================================
# [3] REGRAS LÓGICAS — Autorização de pouso com expressões booleanas
# =============================================================================


# =============================================================================
# [4] BUSCA — Algoritmos de busca linear
# =============================================================================


# =============================================================================
# [5] ORDENAÇÃO — Bubble Sort e Selection Sort
# =============================================================================


# =============================================================================
# [6] FUNÇÕES MATEMÁTICAS — Modelagem de fenômenos do pouso
# =============================================================================


# =============================================================================
# [7] SIMULAÇÃO — Execução do pouso sequencial
# =============================================================================


# =============================================================================
# [8] EXIBIÇÃO E MENU — Interface com o operador
# =============================================================================


# =============================================================================
# Ponto de entrada
# =============================================================================