from pathlib import Path
import itertools
import numpy as np
import src.app.get_perfect_synergies as gps
from functools import partial
class TestClass:
    def test_load_units(self):
        path = Path("test/app/test_resources/champs.csv")
        # load the units
        units, unit_dict, unit_dict_inv, trait_dict, trait_dict_inv = gps.load_units(path)
        # check that the units are the correct length
        assert units.shape[0] == len(unit_dict)
        # check that the unit_dict is the same length as the inverse
        assert len(unit_dict) == len(unit_dict_inv)
        # check that the trait dict is the same length as the inverse
        assert len(trait_dict) == len(trait_dict_inv)
        # check that the keys of unit dict are ints
        for k in unit_dict:
            assert isinstance(k, int)
        # check that the values of unit dict are strings
        for v in unit_dict.values():
            assert isinstance(v, str)
        # check that the keys of unit dict inv are strings
        for k in unit_dict_inv:
            assert isinstance(k, str)
        # check that the values of unit dict inv are ints
        for v in unit_dict_inv.values():
            assert isinstance(v, int)
        # check that the keys of origin dict are ints
        for k in trait_dict:
            assert isinstance(k, int)
        # check that the values of origin dict are strings
        for v in trait_dict.values():
            assert isinstance(v, str)
        # check that the keys of origin dict inv are strings
        for k in trait_dict_inv:
            assert isinstance(k, str)
        # check that the values of origin dict inv are ints
        for v in trait_dict_inv.values():
            assert isinstance(v, int)
    def test_load_breakpoints(self):
        path = Path("test/app/test_resources/origins.csv")
        breakpoints = gps.load_breakpoints(path)
        # spot check some known breakpoints
        bp = breakpoints["Mastermind"]
        assert(len(bp) == 1)
        bp = breakpoints["Debonair"]
        assert(len(bp) == 3)
        truth = [3, 5, 7]
        for i in range(len(bp)):
            assert(bp[i] == truth[i])

    def test_get_ranges(self):
        path = Path("test/app/test_resources/champs.csv")
        units, unit_dict, unit_dict_inv, origin_dict, origin_dict_inv, class_dict, class_dict_inv = gps.load_units(path)
        prefix_size = 2
        prefix = [0, 1]
        ranges = gps.get_ranges(units.shape[0], prefix)
        # print the endpoints of each range
        for r in ranges:
            print(r.start, r.stop)
        # check that the ranges are the correct length
        assert len(ranges) == prefix_size + 1
        # check that the ranges don't overlap
        for i in range(len(ranges) - 1):
            assert ranges[i].stop < ranges[i+1].start
        # check that the ranges don't go past the end of the array
        assert ranges[-1].stop == units.shape[0]

    def test_get_unused_it(self):
        path = Path("test/app/test_resources/champs.csv")
        units, unit_dict, unit_dict_inv, origin_dict, origin_dict_inv, class_dict, class_dict_inv = gps.load_units(path)
        prefix_size = 2
        prefix = [0, 1]
        unused_it = gps.get_unused_it(units, prefix)
        unused_it_list = list(unused_it)
        # check that the unused_it is the correct length
        print(unused_it_list)
        assert len(unused_it_list) == units.shape[0] - prefix_size
        # check that unused it does not contain the prefix
        for i in prefix:
            assert i not in unused_it_list
        # check that unused it contains all other indices
        for i in range(units.shape[0]):
            if i not in prefix:
                assert i in unused_it_list
    def test_get_partial_combination(self):
        path = Path("test/app/test_resources/champs.csv")
        units, unit_dict, unit_dict_inv, origin_dict, origin_dict_inv, class_dict, class_dict_inv = gps.load_units(path)
        prefix_size = 2
        prefix = [0, 1]
        size = 5
        partial_combination = gps.get_partial_combination(units, prefix, size)
        # check that each element in the partial combination has the correct length
        for c in partial_combination:
            assert len(c) == size-prefix_size
        # check that each element in the partial combination does not contain any of the prefix
        for c in partial_combination:
            for i in prefix:
                assert i not in c
    def test_best_overall(self):
        path = Path("test/app/test_resources/champs.csv")
        units, unit_dict, unit_dict_inv, origin_dict, origin_dict_inv, class_dict, class_dict_inv = gps.load_units(path)
        prefix_size = 2
        team_size = 3
        top_n = 1
        def dummy_measure(units, full):
            return sum(full)
        ovr = gps.best_overall(units, prefix_size, team_size, dummy_measure, top_n)
        # dump the queue to a list
        ovr_list = list(ovr.queue)
        assert len(ovr_list) == top_n
        for i in range(top_n):
            assert len(ovr_list[i][1]) == team_size
        # print the scores of the top n
        for i in range(len(ovr_list)):
            print("Team: ", i, "Score: ", ovr_list[i])
            print(ovr_list[i][0])
        # since the dummy scoring just adds the indices of the team
        # the top team should just be the last 3 units in the input file
        # because they have the highest indices
        assert(ovr_list[i][0] == 57 + 58 + 59)

    def test_fill_mask(self):
        mask = [0] * 10
        id = 1
        input_traits = [1, 2, 3, 1, 1, 1, 1, 1, 1, 1]
        breaks = [3, 5, 7]
        gps.fill_mask(mask, input_traits, id, breaks)
        truth = [1, 0, 0, 1, 1, 1, 1, 1, 1, 0]
        assert(mask == truth)
        gps.fill_mask(mask, input_traits, id, breaks)
        assert(mask == truth)
    def test_is_perfect_synergy(self):
        # load champs
        path = Path("test/app/test_resources/champs.csv")
        units, unit_dict, unit_dict_inv  = gps.load_units(path)
        # load origin breaks
        path = Path("test/app/test_resources/origins.csv")
        origin_breakpoints_str_k = gps.load_breakpoints(path)
        origin_breakpoints = {origin_dict_inv[k] : v for k, v in origin_breakpoints_str_k.items()}
        # load class breaks
        path = Path("test/app/test_resources/classes.csv")
        class_breakpoints_str_k = gps.load_breakpoints(path)
        print(class_breakpoints_str_k)
        class_breakpoints = {class_dict_inv[k] : v for k, v in class_breakpoints_str_k.items()}
        prefix_size = 2
        team_size = 3
        top_n = 100
        pf = partial(gps.is_perfect_synergy, origin_breaks=origin_breakpoints, class_breaks=class_breakpoints)
        ovr = gps.best_overall(units, prefix_size, team_size, pf, top_n)
        # dump the queue to a list
        ovr_list = list(ovr.queue)
        # check that the top team is perfect synergy
        assert gps.is_perfect_synergy(ovr_list[0][0], units, prefix_size, team_size)
        # check that the top team is not perfect synergy
        assert not gps.is_perfect_synergy(ovr_list[0][0], units, prefix_size, team_size, False)
