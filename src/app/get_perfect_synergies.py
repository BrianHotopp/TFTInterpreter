import multiprocessing
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
    get back
    units: dict int -> list of int showing which traits the unit has
    unit_names: dict int -> string mapping unit id to name
    unit_names_inv: dict string -> int mapping unit name to id
    traits: dict int -> string mapping trait id to name
    traits_inv: dict string -> int mapping trait name to id

    """
    with open(path, "r") as f:
        units = f.readlines()
    # parse each line
    data = [unit.split(",") for unit in units]
    units = {}
    unit_names = {}
    unit_names_inv = {}
    traits = {}
    traits_inv = {}
    # map id to unit name
    for i, unit in enumerate(data):
        units[i] = unit[2:6]
        unit_names[i] = unit[0]
        unit_names_inv[unit[0]] = i
    # collect all unique traits
    all_traits = set()
    for unit in units:
        all_traits.update(units[unit])
    # map id to trait name
    for i, trait in enumerate(all_traits):
        traits[i] = trait
        traits_inv[trait] = i
    return units, unit_names, unit_names_inv, traits, traits_inv

def best_of_size(units, size, measure, top_n, workers = 16, chunksize = 10000):
    """
    returns the top n teams of size size using measure to evaluate the teams
    """
    p = Pool(processes=workers)
    combs = itertools.combinations(range(units.shape[0]), size)
    # copy of combs iterator
    first_combs, second_combs = itertools.tee(combs)
    # get the top n teams in parallel
    all_teams_it = zip(p.imap(measure, first_combs, chunksize=chunksize), second_combs)
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
