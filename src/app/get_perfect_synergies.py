from pathlib import Path
import itertools
import numpy as np
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
    # remove newline characters
    units = [[unit[0].strip(), int(unit[1].strip()), unit[2].strip(), unit[3].strip(), unit[4].strip(), unit[5].strip()] for unit in units]
    # get a set of all unit names
    unit_names = set([unit[0] for unit in units])
    # get a set of all origins 
    origins = set([unit[2] for unit in units]).union(set([unit[3] for unit in units]))
    # get a set of all classes
    classes = set([unit[4] for unit in units]).union(set([unit[5] for unit in units]))
    # create a dictionary mapping number to unit name
    unit_dict = {i:unit[0] for i, unit in enumerate(unit_names)}
    # inverse of unit_dict
    unit_dict_inv = {unit[0]:i for i, unit in enumerate(unit_names)}
    # create a dict mapping number to origin
    origin_dict = {i:unit[2] for i, unit in enumerate(origins)}
    # inverse of origin_dict
    origin_dict_inv = {unit[2]:i for i, unit in enumerate(origins)}
    # create a dict mapping number to class
    class_dict = {i:unit[4] for i, unit in enumerate(classes)}
    # inverse of class_dict
    class_dict_inv = {unit[4]:i for i, unit in enumerate(classes)}
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
def get_unused_it(units, prefix):
    """
    prefix: list of indexes we should not use
    returns an iterator of all possible combinations of units excluding the prefix (uses indexes)
    """
    # the prefix is in sorted order already
    ranges = []
    for i in range(len(prefix)-1):
        if i == 0:
            ranges.append(range(prefix[i]))
        else:
            ranges.append(range(prefix[i-1]+1, prefix[i]))
    # the last range is the last index
    ranges.append(range(prefix[-1], units.shape[0]))
    return itertools.chain(*ranges)
    
def get_combinations(units, prefix):
    """
    units: np array
    prefix: list of indexes we should not use
    returns an iterator of all possible combinations of units excluding the prefix (uses indexes)
    """
    # the prefix is in sorted order already
    ranges = []
    for i in range(len(prefix)):
        if i == 0:
            ranges.append(range(prefix[i]))
        else:
            ranges.append(range(prefix[i-1]+1, prefix[i]))
    itertools.chain(*ranges)

def main():
    units_data_path = Path("src/resources/champs.csv")
    units_data = load_units("units.txt")
    
if __name__ == "__main__":
    main()
