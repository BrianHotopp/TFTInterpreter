from pathlib import Path
from multiprocessing import Pool
import itertools
from re import M
import heapq
import functools
import re
import numpy as np
import queue 
import random
from functools import partial
def load_breakpoints(path):
    """
    load breakpoints from a file
    each line has the first column as the breakpoint and all other
    columns are part of the breakpoint
    """
    with path.open() as f:
        breakpoints = f.readlines()
    breakpoints = [[x.strip() for x in breakpoint.split(",")] for breakpoint in breakpoints]
    traits = [x[0] for x in breakpoints]
    breakpoints = [[int(y) for y in x[1:]] for x in breakpoints]
    breakpoints = {trait:breakpoint for trait, breakpoint in zip(traits, breakpoints)}
    return breakpoints
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
    unit_names = list([unit[0] for unit in units])
    # get a set of all traits
    traits = list(set([unit[2] for unit in units]).union(set([unit[3] for unit in units])).union(set([unit[4] for unit in units])).union(set([unit[5] for unit in units])))
    # create a dictionary mapping number to unit name
    unit_dict = {i:unit for i, unit in enumerate(unit_names)}
    # inverse of unit_dict
    unit_dict_inv = {unit:i for i, unit in enumerate(unit_names)}
    # create a dict mapping number to trait
    trait_dict = {i:trait for i, trait in enumerate(traits)}
    # inverse of trait_dict
    trait_dict_inv = {trait:i for i, trait in enumerate(traits)}
    # convert the units list to numbers using the dictionaries  
    units = [[unit_dict_inv[unit[0]], unit[1], trait_dict_inv[unit[2]], trait_dict_inv[unit[3]], trait_dict_inv[unit[4]], trait_dict_inv[unit[5]]] for unit in units]
    # to np array for big zoom zoom
    units = np.array(units)
    return units, unit_dict, unit_dict_inv, trait_dict, trait_dict_inv

def add_if_good(measure, queue, team):
    """
    measure: function to use to evaluate a combination
    queue: thread safe priority queue
    team: list of indexes of units
    """
    measure_value = measure(team)
    # attempt to add to the priority queue if measure value is better (larger) than the worst element
    if queue.full():
        if measure_value > queue.queue[0][0]:
            print("found a better team")
            # remove the worst element
            queue.get()
            # add the new element
            queue.put((measure_value, team))
    else:
        print("insert initial")
        queue.put((measure_value, team))
def best_of_size(units, size, measure, top_n):
    """
    returns the top n teams of size size using measure to evaluate the teams
    """
    p = Pool(processes=200)
    combs = itertools.combinations(range(units.shape[0]), size)
    # copy of combs iterator
    first_combs, second_combs = itertools.tee(combs)
    # get the top n teams in parallel
    all_teams_it = zip(p.imap(measure, first_combs, chunksize=10000), second_combs)
    r = heapq.nlargest(top_n, all_teams_it, key=lambda x: x[0])
    p.close()
    return r

def fill_mask(mask, input_traits, l, id, breaks):
    """
    fills the mask as much as possible for the given input trait id
    """
    for b in reversed(breaks):
        # todo do this fast with numba
        # count the number of times id occurs in the input traits list
        count = 0
        for i in range(l):
            if input_traits[i] == id:
                count += 1
        if count >= b:
            # fill b spots in the mask where id is input_traits
            filled = 0
            for i in range(l):
                if input_traits[i] == id:
                    mask[i] = 1
                    filled += 1
                    if filled == b:
                        break
            
def is_perfect_synergy(team, units, trait_breaks, null_trait_id, traits_arr, t_mask):
    # build up the traits array
    # zero the mask
    t_mask[:] = 0
    l = 0
    for i in team:
        # paste the masked values onto the next available indices of traits_arr
        t = units[i][2:6][units[i][2:6] != null_trait_id]
        traits_arr[l:l+t.shape[0]] = t
        l += t.shape[0]
    for trait_id in trait_breaks:
        fill_mask(t_mask, traits_arr, l, trait_id, trait_breaks[trait_id])
    return int(np.all(t_mask[:l]))

def main():
    units_data_path = Path("src/resources/champs.csv")
    units_data = load_units("units.txt")
    
if __name__ == "__main__":
    main()
