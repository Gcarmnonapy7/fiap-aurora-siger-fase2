
from collections import deque
from dataclasses import dataclass
from typing import Optional, List,Tuple, Any
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
    AUTHORIZED = "Autorized stop"
    DENIED = "Denied stop"
    EMERGENCY = "Emergency post"
    LANDED = "Landed"
    
@dataclass
class Module: 
    """
    Represents a module to Mars
    """
    
    id: int             
    name: str           
    type: ModuleType    
    weight: float       
    arrival_time: float 
    sensor_ok: bool      

    stop_condition: LandingStatus = LandingStatus.WAITING  
    fuel_level: float = 100.0  
    priority: int = 0  
    speed: float = 0.0  
    module_integrity: float = 100.0  
    status: str = "In transit"  
    
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
        comparation = [0]
        
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
                
                comparation[0] += 1 
                
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
        print(f"Quick sort completed in {end - begin:.6f} seconds.")
        print(f"Total comparisons made: {comparation}.")
        return sorted_modules, (end - begin) * 1000, comparation
    
    @staticmethod
    def merge_sort(modules: List[Module], camp: str = "priority"):
        """
        Merge Sort algorithm for sorting modules by priority.
        """
        
        if modules is None: 
            raise ValueError("The list of modules cannot be None.")
        elif camp not in ["priority"]:
            raise ValueError("The sorting camp must be 'priority'.")
        
        begin = time.perf_counter()
    
        comparation = [0]  
        
        def merge(left: List[Module], right: List[Module]) -> List[Module]:
            merged = []
            i = j = 0
            
            while i < len(left) and j < len(right):
                comparation[0] += 1  
                
                if camp == "priority":
                    if left[i].priority <= right[j].priority:  
                        merged.append(left[i])
                        i += 1
                    else:
                        merged.append(right[j])
                        j += 1
            
            merged.extend(left[i:])
            merged.extend(right[j:])
            return merged
        
        def _merge_sort(arr: List[Module]) -> List[Module]:
            if len(arr) <= 1:
                return arr
            
            mid = len(arr) // 2
            left_half = _merge_sort(arr[:mid])
            right_half = _merge_sort(arr[mid:])
            
            return merge(left_half, right_half)
        
        sorted_modules = _merge_sort(modules.copy())
        end = time.perf_counter()
        elapsed_ms = (end - begin) * 1000
        
        print(f"Merge sort completed in {elapsed_ms:.6f} ms.")
        print(f"Total comparisons made: {comparation[0]}.")
        
        return sorted_modules, elapsed_ms, comparation[0]
                
class LogicalGatesMGPEB:
    """
    Implement decision rules using boolean logic
    """
    @staticmethod
    def fuel_sufficient(fuel_level: float, threshold: float = 20.0) -> bool:
        return fuel_level > threshold
    
    @staticmethod
    def atmosphere_favorable(condition: AtmosfericClassifier) -> bool:
        return condition == AtmosfericClassifier.GREEN
    
    @staticmethod
    def area_available(area_free: bool) -> bool:
        return area_free
    
    @staticmethod
    def sensors_operational(sensors_ok: bool) -> bool:
        return sensors_ok
    
    @staticmethod
    def good_atmosferic_conditions(condition : AtmosfericClassifier) -> bool : 
        return condition == AtmosfericClassifier.GREEN or condition == AtmosfericClassifier.YELLOW

    @staticmethod
    def enough_fuel(fuel_level: float, threshold: float = 75.0) -> bool:
        return fuel_level >= threshold  # Safe if fuel level is above the threshold
           
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
        
    @staticmethod
    def safe_to_land(conditions: List[bool]) -> bool:
        return all(conditions)  # Safe to land if all conditions are True
    
class MGPEBSystem:    
    def __init__(self):
        self.waiting_modules: deque[Module] = deque()
        self.authorized_modules: List[Module] = []  
        self.emergency_stack: List[Module] = []
        self.alert_list: List[Module] = []  
        self.landed_modules: List[Module] = []  
        self.alert_log: List[str] = [] 
        
        self.logic = LogicalGatesMGPEB()
        self.search_algorithms = SearchAlgorithms()
        self.sort_algorithms = SortAlgorithms()
        
        self.next_id = 1
        self.area_landing_free = True 
        self.area_landing_released = True
        self.sensors_ok = True
        self.current_atmosphere = AtmosfericClassifier.GREEN 
        self.total_landings = 0
        self.total_emergencies = 0  
        
    def module_registration(self, name: str, module_type: ModuleType, weight: float, 
                        arrival_time: float, sensor_ok: bool = True,
                        priority: int = 5, criticality: int = 1, fuel_level: float = 100.0):
        module = Module(
            id=self.next_id,
            name=name,
            type=module_type,
            weight=weight,
            arrival_time=arrival_time,
            sensor_ok=sensor_ok,
            priority=priority,
            fuel_level=fuel_level,
            module_integrity=100.0
        )
        self.waiting_modules.append(module)
        self.next_id += 1
        print(f"Module {module.id} ({name}) registered and added to waiting queue.")
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
        
        random_modules = []
        
        for i in range(num_modules):
            random_priority = random.randint(1,5),
            module = Module(
                id=self.next_id ,# Assign unique ID starting from 1
                name=f"Module_{self.next_id}",
                type=random.choice(module_types),
                weight=random.uniform(100.0, 1000.0),  # Random weight between 100 and 1000 kg
                arrival_time=time.time() + random.uniform(0, 10000),  # Random arrival time within the next 10,000 seconds
                sensor_ok=random.choice([True, False]), # Randomly set sensor status
                priority = random_priority, # based on the time arrival set the priority of the module, the less time to arrive the more priority it has.
                fuel_level= random.uniform(10.0,95.0),
                module_integrity= random.uniform(50.0,100.0)
            ) 
            random_modules.append(module)
            self.next_id +=1 
        return random_modules
    
    def reorder_queue_by_priority(self):
        """Reorders the waiting queue based on module priority."""
        
        if len(self.waiting_modules) == 0:
            print("No modules in the waiting queue to reorder.")
            return 0,0
        
        queue_list = list(self.waiting_modules)
        sorted_queue, time_taken, comparisons = self.sort_algorithms.merge_sort(queue_list)
        self.waiting_modules = deque(sorted_queue)
        print(f"Waiting queue reordered by priority in {time_taken:.2f} ms with {comparisons} comparisons.")
        return time_taken, comparisons
        
    def evaluate_module_for_landing(self, module: Module, medical_urgency: bool = False) -> Tuple[bool, str]:
        """Evaluates if a module is ready for landing based on its attributes."""
        # Verificar emergência primeiro
        if medical_urgency and module.type == ModuleType.MEDICAL:
            print(f"Medical emergency override for module {module.id}!")
            module.stop_condition = LandingStatus.EMERGENCY
            return True, "EMERGENCY LANDING AUTHORIZED"
        
        # Verificar combustível (crítico)
        if module.fuel_level < 20:
            module.stop_condition = LandingStatus.DENIED
            self.alert_log.append(f"Module {module.id} denied: low fuel ({module.fuel_level:.1f}%)")
            return False, f"DENIED: Low fuel ({module.fuel_level:.1f}% < 20%)"
        
        # Verificar sensores
        if not module.sensor_ok:
            module.stop_condition = LandingStatus.DENIED
            self.alert_log.append(f"Module {module.id} denied: sensor failure")
            return False, "DENIED: Sensor failure"
        
        # Verificar área de pouso
        if not self.area_landing_free:
            module.stop_condition = LandingStatus.DENIED
            self.alert_log.append(f"Module {module.id} denied: landing area occupied")
            return False, "DENIED: Landing area occupied"
        
        # Verificar atmosfera
        if self.current_atmosphere != AtmosfericClassifier.GREEN:
            module.stop_condition = LandingStatus.DENIED
            self.alert_log.append(f"Module {module.id} denied: bad atmosphere")
            return False, f"DENIED: Bad atmosphere ({self.current_atmosphere.value})"
        
        # Todas as condições atendidas
        module.stop_condition = LandingStatus.AUTHORIZED
        print(f"Module {module.id} is ready for landing.")
        return True, "LANDING AUTHORIZED"
    
    def simulate_landing_process(self, module: Module) -> bool:
        if module.stop_condition not in [LandingStatus.AUTHORIZED, LandingStatus.EMERGENCY]:
            print(f"Module {module.id} cannot proceed to landing. Current status: {module.stop_condition.value}")
            return False
        
        self.area_landing_free = False
        print(f"\n Module {module.id} ({module.name}) is landing...")
        
        descent_time = 45
        braking_speed = 15
        
        consumption_rate = fuel_consumption_rate(braking_speed)
        fuel_used = (consumption_rate * descent_time) / 100
        module.fuel_level = max(0, module.fuel_level - fuel_used)
        
        print(f"   Initial fuel level: {(module.fuel_level + fuel_used):.1f}%")
        
        for t in range(0, descent_time + 1, 15):
            alt = descent_altitude(t)
            energy = solar_energy(t % 24)
            print(f"   Time: {t}s | Altitude: {alt:.1f}m | Solar Energy: {energy:.1f}W")
        
        print(f"   Remaining fuel: {module.fuel_level:.1f}%")
        
        module.stop_condition = LandingStatus.LANDED
        self.landed_modules.append(module)
        self.area_landing_free = True
        self.total_landings += 1
        
        print(f" Module {module.id} has successfully landed!\n")
        return True

    def process_next_module(self, medical_urgency: bool = False) -> Optional[Module]:
        if not self.waiting_modules:
            print("No modules waiting for landing.")
            return None
        
        next_module = self.waiting_modules.popleft()
        
        authorized, message = self.evaluate_module_for_landing(next_module, medical_urgency)
        print(f" {message}")
        
        if authorized:
            self.simulate_landing_process(next_module)
        else:
            print(f" Module {next_module.id} added to alert list")
            self.alert_list.append(next_module)
        
        return next_module
    
    def process_emergency_module(self) -> Optional[Module]:
        """_summary_

        Args:
            module_id (int): _description_

        Returns:
            Optional[Module]: _description_
        """
        
        if not self.emergency_stack:
            print("No emergency modules to process.")
            return None
        
        module = self.emergency_stack.pop() # Get the most recent emergency module
        self.area_landing_released = True  # Ensure the landing area is released for emergency processing
        self.simulate_landing_process(module)
        
        return module  
    
    def search_module(self, module_id: int) -> Optional[Module]:
        """Search for a module by ID."""
        
        # Collect data from all modules
        all_modules = list(self.waiting_modules) + self.authorized_modules + self.emergency_stack + self.landed_modules
        
        # Linear search
        result_index = self.search_algorithms.linear_search(all_modules, module_id)
        
        if result_index is not None:
            print(f"\n Module found: {all_modules[result_index]}")
            return all_modules[result_index]
        else:
            print(f"\n Module with ID {module_id} not found in the system.")
            return None
    
    def show_status(self):
        print("\n" + "=" * 60)
        print("MGPEB SYSTEM STATUS")
        print("=" * 60)
        print(f"   Waiting queue: {len(self.waiting_modules)}")
        print(f"   Landed modules: {len(self.landed_modules)}")
        print(f"   Alert list: {len(self.alert_list)}")
        print(f"   Emergency stack: {len(self.emergency_stack)}")
        print(f"   Total landings: {self.total_landings}")
        print(f"   Landing area: {'FREE' if self.area_landing_free else 'OCCUPIED'}")
        print(f"   Sensors: {'OK' if self.sensors_ok else 'FAIL'}")
        print("=" * 60)
        
    def generate_report(self) -> str:
        """
        Generate complete system report
        """
        
        report = []
        report.append("=" * 70)
        report.append("MGPEB report - Aurora mission phase 2") 
        report.append("=" * 70)

        report.append(f"\n Operational statistics:")
        report.append(f"Total modules processed: {self.total_landings}")
        report.append(f"Total emergency landings: {len(self.emergency_stack)}")
        report.append(f"Total alerts generated: {len(self.alert_log)}")
        report.append(f"Landing area status: {'Free' if self.area_landing_released else 'Occupied'}") 

        if self.authorized_modules:  
            report.append(f"\n Authorized modules:") 
            for module in self.authorized_modules[-5:]:
                report.append(f"   Module ID: {module.id} - Priority: {module.priority}")

        if self.alert_list: 
            report.append(f"\n Alert modules:")
            for module in self.alert_list[-5:]:
                report.append(f"   Module ID: {module.id} - Priority: {module.priority}")
    
# Comparing searches // sorting

def comparing_searches_algorithms():
    print(f"\n {'='*50}")
    print("Comparation between search algoritms...")
    print(f"\n {"=" * 60}")
    
    system = MGPEBSystem()
    modules = system.generate_random_modules(10)
    
    target_id = random.randint(1,10)
    
    # Linear search
    start = time.perf_counter()
    result_index = system.search_algorithms.linear_search(modules, target_id)
    time_lin = (time.perf_counter() - start) * 1000
    
    # Binary search (requires sorted list)
    sorted_modules, sort_time, _ = system.sort_algorithms.merge_sort(modules, "priority")
    start = time.perf_counter()
    result_bin_index = system.search_algorithms.binary_search(sorted_modules, target_id)
    time_bin = (time.perf_counter() - start) * 1000
    
    print(f"\n RESULTS (SEARCHING FOR ID {target_id}):")
    print(f"   Linear search:  {time_lin:.4f} ms")
    print(f"   Binary search: {time_bin:.4f} ms")
    
    if time_lin > 0 and time_bin > 0:
        speedup = time_lin / time_bin
        print(f"\n  Binary search was {speedup:.2f}x faster!")
  
def comparing_sorting_algorithms():
    print("\n" + "=" * 50)
    print("Comparison between search algorithms...")
    print("\n" + "=" * 60)
        
    system = MGPEBSystem()
    modules = system.generate_random_modules(10)

    start = time.perf_counter()
    time_lin_ms = (time.perf_counter() - start) * 1000
    
       # Bubble Sort
    _, time_bubble, comps_bubble = system.sort_algorithms.bubble_sort(modules, "priority")
    
    # Quick Sort
    _, time_quick, comps_quick = system.sort_algorithms.quick_sort(modules, "priority")
    
    # Merge Sort
    _, time_merge, comps_merge = system.sort_algorithms.merge_sort(modules, "priority")
    
    print(f"\n RESULTS (50 elements):")
    print(f"   Bubble Sort: {time_bubble:.4f} ms, {comps_bubble} comparisons")
    print(f"   Quick Sort:  {time_quick:.4f} ms, {comps_quick} comparisons")
    print(f"   Merge Sort:  {time_merge:.4f} ms, {comps_merge} comparisons")
    
    if time_merge > 0:
        print(f"\n  Merge Sort was {time_bubble/time_merge:.2f}x faster than Bubble Sort")
        print(f"  Quick Sort was {time_bubble/time_quick:.2f}x faster than Bubble Sort")

def analyze_performance():
    """Analyze performance with different input sizes"""
    print("\n" + "=" * 60)
    print("PERFORMANCE ANALYSIS - GROWTH CURVE")
    print("=" * 60)
    
    sizes = [10, 50, 100, 200]
    
    print(f"\n{'Size':<10} {'Bubble (ms)':<15} {'Merge (ms)':<15} {'Quick (ms)':<15}")
    print("-" * 55)
    
    for n in sizes:
        system = MGPEBSystem()
        modules = system.generate_random_modules(n)
        
        _, time_bubble, _ = system.sort_algorithms.bubble_sort(modules, "priority")
        _, time_merge, _ = system.sort_algorithms.merge_sort(modules, "priority")
        _, time_quick, _ = system.sort_algorithms.quick_sort(modules, "priority")
        
        print(f"{n:<10} {time_bubble:<15.4f} {time_merge:<15.4f} {time_quick:<15.4f}")
    
    print("\n GROWTH ANALYSIS:")
    print("   • Bubble Sort (O(n²)) - Quadratic growth")
    print("   • Merge Sort (O(n log n)) - Efficient for all cases")
    print("   • Quick Sort (O(n log n) avg) - Fastest on average")

def list_modules(system:MGPEBSystem):
    """_summary_
    List all modules with their IDs and information

    Args:
        system (MGPEBSystem): class of the project 
    """
    print("\n" + "=" * 60)
    print("ALL MODULES IN THE SYSTEM")
    print("=" * 60)
    
    all_modules = []
    all_modules.extend(list(system.waiting_modules))
    all_modules.extend(system.authorized_modules)
    all_modules.extend(system.emergency_stack)
    all_modules.extend(system.landed_modules)
    all_modules.extend(system.alert_list)
    
    if not all_modules:
        print("No modules found in the system.")
        return
    
    print(f"\n TOTAL MODULES: {len(all_modules)}")
    print("-" * 60)
    
    # Listar módulos por categoria
    if system.waiting_modules:
        print(f"\n  WAITING QUEUE ({len(system.waiting_modules)} modules):")
        for module in system.waiting_modules:
            print(f"   • ID: {module.id} | Name: {module.name} | Priority: {module.priority} | Fuel: {module.fuel_level:.1f}%")
    
    if system.authorized_modules:
        print(f"\n AUTHORIZED MODULES ({len(system.authorized_modules)}):")
        for module in system.authorized_modules:
            print(f"   • ID: {module.id} | Name: {module.name} | Priority: {module.priority}")
    
    if system.emergency_stack:
        print(f"\n EMERGENCY STACK ({len(system.emergency_stack)}):")
        for module in system.emergency_stack:
            print(f"   • ID: {module.id} | Name: {module.name} | Priority: {module.priority}")
    
    if system.landed_modules:
        print(f"\n LANDED MODULES ({len(system.landed_modules)}):")
        for module in system.landed_modules:
            print(f"   • ID: {module.id} | Name: {module.name} | Priority: {module.priority} | Fuel: {module.fuel_level:.1f}%")
    
    if system.alert_list:
        print(f"\n ALERT LIST ({len(system.alert_list)}):")
        for module in system.alert_list:
            print(f"   • ID: {module.id} | Name: {module.name} | Priority: {module.priority}")
    
    print("\n" + "=" * 60)
    
def menu():
    """Main interactive menu"""
    system = MGPEBSystem()
    
    print("\n" + "=" * 70)
    print("==     MGPEB - Aurora Mission (Mars)     ==")
    print("=" * 70)
    
    # Register initial modules
    # Register initial modules - usando os parâmetros corretos
    system.module_registration("Central Habitat", ModuleType.HABITAT, 12000, 
                            time.time() + 3600, True, priority=1, fuel_level=85)
    system.module_registration("Power Reactor", ModuleType.ENERGY, 8500,
                            time.time() + 7200, True, priority=1, fuel_level=75)
    system.module_registration("Science Lab", ModuleType.LAB, 6200,
                            time.time() + 10800, True, priority=2, fuel_level=65)
    system.module_registration("Medical Support", ModuleType.MEDICAL, 4500,
                            time.time() + 14400, True, priority=1, fuel_level=90)
    
    running = True
    while running:
        print("\n" + "=" * 50)
        print("MAIN MENU - MGPEB")
        print("=" * 50)
        print("1. Show system status")
        print("2. Reorder queue by priority")
        print("3. Process next module")
        print("4. Simulate medical emergency")
        print("5. Search module by ID")
        print("6. Compare search algorithms")
        print("7. Compare sorting algorithms")
        print("8. Show performance analysis")
        print("9 List Modules ")
        print("0. Exit")
        print("-" * 50)
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            system.show_status()
        
        elif choice == "2":
            system.reorder_queue_by_priority()
        
        elif choice == "3":
            system.process_next_module()
        
        elif choice == "4":
            system.process_next_module(medical_urgency=True)
        
        elif choice == "5":
            try:
                module_id = int(input("Enter module ID: "))
                result = system.search_module(module_id)
                if result is None: 
                    print(f"Module with ID {module_id} not found!")
            except ValueError:
                print(" Invalid ID! Please enter a number.")
        
        elif choice == "6":
            comparing_searches_algorithms()
        
        elif choice == "7":
            comparing_sorting_algorithms()
        
        elif choice == "8":
            analyze_performance()
            
        elif choice == "9":
            list_modules(system)
                        
        elif choice == "0":
            print("\n Shutting down MGPEB. Aurora Mission continues!")
            running = False
        else:
            print("Invalid option!")

if __name__ == "__main__" :
    menu()