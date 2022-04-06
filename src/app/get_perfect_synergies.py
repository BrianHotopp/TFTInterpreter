#!python

# Third Party Imports
# from string import whitespace
# from tkinter import ALL
# from webbrowser import get
import itertools

class Unit():
    """
    A Unit object stores a TFT unit with attributes.
    """
    def __init__(self, name: str, abb: str, origins: set(), classes: set(), cost: str) -> None:
        """
        Initialize attributes of a Unit.
        """
        self.name = name
        self.abb = abb
        self.origins = origins
        self.classes = classes
        self.cost = cost

    def __str__(self) -> str:
        """
        toString function.
        """
        return f"{self.name} {self.abb} {self.origins} {self.classes} {self.cost}"

def consume(origins_classes_list, curr_origin_class, splits):
    """
    Parse the origin classes list.
    Args:
        origins_classes_list: list of origin classes
        curr_origin_class: current origin class
        splits: 
    """
    num_origin_class = origins_classes_list.count(curr_origin_class)
    for split in splits:
        if num_origin_class >= split:
            for i in range(num_origin_class):
                origins_classes_list.remove(curr_origin_class)
            break

def is_perfect_synergy(units):
    """
    """
    all_stuff = []
    for unit in units:
        all_stuff.extend(list(unit.origins))
        all_stuff.extend(list(unit.classes))
    # for each trait included, pop off as many as possible
    # todo factor hardcoded data out of function, use loop
    # origins
    consume(all_stuff, "Chemtech", [3, 5, 7, 9])
    consume(all_stuff, "Clockwork", [2, 4, 6])
    consume(all_stuff, "Debonair", [3, 5, 7])
    consume(all_stuff, "Enforcer", [2, 4])
    consume(all_stuff, "Glutton", [1])
    consume(all_stuff, "Hextech", [2, 4, 6, 8])
    consume(all_stuff, "Mastermind", [1])
    consume(all_stuff, "Mercenary", [3, 5, 7])
    consume(all_stuff, "Mutant", [3, 5, 7])
    consume(all_stuff, "Rival", [1])
    consume(all_stuff, "Scrap", [2, 4, 6])
    consume(all_stuff, "Socialite", [1, 2, 3, 5])
    consume(all_stuff, "Syndicate", [3, 5, 7])
    consume(all_stuff, "Yordle", [3, 6])
    consume(all_stuff, "Yordle-Lord", [1])
    # classes
    consume(all_stuff, "Arcanist", [2, 4, 6, 8])
    consume(all_stuff, "Assassin", [2, 4, 6])
    consume(all_stuff, "Bodyguard", [2, 4, 6, 8])
    consume(all_stuff, "Bruiser", [2, 4, 6, 8])
    consume(all_stuff, "Challenger", [2, 4, 6, 8])
    consume(all_stuff, "Colossus", [2])
    consume(all_stuff, "Enchanter", [2, 3, 4, 5])
    consume(all_stuff, "Innovator", [3, 5, 7])
    consume(all_stuff, "Mastermind", [1])
    consume(all_stuff, "Scholar", [2, 4, 6])
    consume(all_stuff, "Sniper", [2, 4, 6])
    consume(all_stuff, "Transformer", [1])
    consume(all_stuff, "Twinshot", [2, 3, 4, 5])
    l = len(all_stuff)
    return l == 0


def test_is_perfect_synergy():
    a = Unit("a", "b", set(["Chemtech"]), set(), "1")
    z = Unit("a", "b", set(["Syndicate"]), set(), "1")
    b = [a, a, a, z]
    c = is_perfect_synergy(b)
    print(f"is perfect synergy: {c}")


def get_perfect_synergies(units_on_board):
    SET_6_UNITS = dict()
    with open(
            "E:\Dropbox\Spring 2022\Software Design and Documentation\code\gather_data\\resources\set6_classes.txt") as classes_file_handle:
        for line in classes_file_handle.readlines():
            unit_name, abbreviated_name = [x.strip() for x in line.split(",")]
            SET_6_UNITS[unit_name] = abbreviated_name
    abb_to_full = {v: k for k, v in SET_6_UNITS.items()}
    # load the csv of units, origin, class1, class2, cost
    ALL_UNITS = []
    champs = "E:\Dropbox\Spring 2022\Software Design and Documentation\code\gather_data\\resources\champs.csv"
    with open(champs) as classes_csv_file_handle:
        lines = classes_csv_file_handle.readlines()
        for line in lines:
            line = [x.strip() for x in line.split(",")]
            name = line[0]
            abb = SET_6_UNITS[name]
            cost = line[1]
            origin1 = line[2]
            origin2 = line[3]
            class1 = line[4]
            class2 = line[5]
            origins = set()
            origins.add((origin1))
            classes = set()
            classes.add((class1))
            if origin2 != "":
                classes.add((origin2))
            if class2 != "":
                classes.add((class2))

            ALL_UNITS.append(Unit(name, abb, origins, classes, cost))
        for unit in ALL_UNITS:
            print(unit)
    # for every way to choose a set of n units (n from 1 to 10), check if the chosen set is a perfect combination
    perfects = []
    for i in range(1, 10):
        com = itertools.combinations(ALL_UNITS, i)
        for c in com:
            if is_perfect_synergy(c):
                print("set consisting of")
                for u in c:
                    print(u.name)
                print("is perfect")
                perfects.append(c)
    return perfects


ps = get_perfect_synergies([])
with open("psyns.pickle", "wb+") as psyns_file_handle:
    pickle.dump(ps, psyns_file_handle)
# test_is_perfect_synergy()
