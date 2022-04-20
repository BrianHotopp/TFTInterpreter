from pathlib import Path
import itertools
from re import M
import numpy as np
import queue 
import random
def load_breakpoints(path):
    """
    load breakpoints from a file
    """
def load_units(path):
    """
    Loads units from a file.
    path: Path object
    """
    with open(path, "r") as f:
        units = f.readlines()
    # each line has format name, cost, origin1, origin2, class1, class2 
    # parse each line
    units = [unit.split(",") for unit in units]
    # remove newline characters and whitespace
    units = [[unit[0].strip(), int(unit[1].strip()), unit[2].strip(), unit[3].strip(), unit[4].strip(), unit[5].strip()] for unit in units]
    # get a set of all unit names
    unit_names = set([unit[0] for unit in units])
    # get a set of all origins 
    origins = set([unit[2] for unit in units]).union(set([unit[3] for unit in units]))
    # get a set of all classes
    classes = set([unit[4] for unit in units]).union(set([unit[5] for unit in units]))
    # create a dictionary mapping number to unit name
    unit_dict = {i:unit for i, unit in enumerate(unit_names)}
    # inverse of unit_dict
    unit_dict_inv = {unit:i for i, unit in enumerate(unit_names)}
    # create a dict mapping number to origin
    origin_dict = {i:origin for i, origin in enumerate(origins)}
    # inverse of origin_dict
    origin_dict_inv = {origin:i for i, origin in enumerate(origins)}
    # create a dict mapping number to class
    class_dict = {i:cls for i, cls in enumerate(classes)}
    # inverse of class_dict
    class_dict_inv = {cls:i for i, cls in enumerate(classes)}
    # convert the units list to numbers using the dictionaries  
    units = [[unit_dict_inv[unit[0]], unit[1], origin_dict_inv[unit[2]], origin_dict_inv[unit[3]], class_dict_inv[unit[4]], class_dict_inv[unit[5]]] for unit in units]
    # to np array for big zoom zoom
    units = np.array(units)
    return units, unit_dict, unit_dict_inv, origin_dict, origin_dict_inv, class_dict, class_dict_inv
def get_prefixes(units, prefix_size):
    """
    unit_ids: np array
    returns an iterator of all possible 2 unit prefixes (uses indexes)
    """
    return itertools.combinations(range(units.shape[0]), prefix_size)
def get_ranges(l, p):
    """
    """
    # the prefix is in sorted order already
    ranges = []
    for i in range(len(p)):
        if i == 0:
            ranges.append(range(p[i]))
        else:
            ranges.append(range(p[i-1]+1, p[i]))
    ranges.append(range(min(p[-1]+1, l), l))
    return ranges

def get_unused_it(units, prefix):
    """
    prefix: list of indexes we should not use
    returns an iterator of all possible combinations of units excluding the prefix (uses indexes)
    """
    """
    units has length n
    [|0|1|] -> [2, 3, 4, 5,... n]
    [1, 2] -> [0, 3, 4, 5, ... n]
    """
    ranges = get_ranges(units.shape[0], prefix)
    return itertools.chain(*ranges)

def get_partial_combination(units, prefix, size):
    """
    units: np array
    prefix: list of indexes we should not use
    returns an iterator of all possible combinations of units excluding the prefix (uses indexes)
    each element is a list of indexes of length size-len(prefix)
    """
    unused = get_unused_it(units, prefix)
    return itertools.combinations(unused, size-len(prefix))
def dummy_measure(units, full):
    return sum(full)
def best_by_measure(units, prefix, size, measure, priority_queue):
    """
    units: np array
    prefix: list of indexes we should not use
    size: number of units to choose
    measure: function to use to evaluate a combination
    priority_queue: thread safe priority queue
    """
    for postfix in get_partial_combination(units, prefix, size):
        full = prefix + postfix
        measure_value = measure(units, full)
        # attempt to add to the priority queue if measure value is better (larger) than the worst element
        if priority_queue.full():
            if measure_value > priority_queue.queue[0][0]:
                # remove the worst element
                priority_queue.get()
                # add the new element
                priority_queue.put((measure_value, full))
        else:
            priority_queue.put((measure_value, full))

def best_overall(units, prefix_size, size, measure, top_n):
    best = queue.PriorityQueue(maxsize=top_n)
    for prefix in get_prefixes(units, prefix_size):
        best_by_measure(units, prefix, size, measure, best)
    return best
 
def main():
    units_data_path = Path("src/resources/champs.csv")
    units_data = load_units("units.txt")
    
if __name__ == "__main__":
    main()
