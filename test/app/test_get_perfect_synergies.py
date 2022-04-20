from pathlib import Path
import itertools
import numpy as np
import src.app.get_perfect_synergies as gps

class TestClass:
    def test_load_units(self):
        path = Path("test/app/test_resources/champs.csv")
        # load the units
        units, unit_dict, unit_dict_inv, origin_dict, origin_dict_inv, class_dict, class_dict_inv = gps.load_units(path)
        # check that the units are the correct length
        assert units.shape[0] == len(unit_dict)
        # check that the unit_dict is the same length as the inverse
        assert len(unit_dict) == len(unit_dict_inv)
        # check that the origin dict is the same length as the inverse
        assert len(origin_dict) == len(origin_dict_inv)
        # check that the class dict is the same length as the inverse
        assert len(class_dict) == len(class_dict_inv)
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
        top_n = 10
        ovr = gps.best_overall(units, prefix_size, team_size, gps.measure, top_n)
        # dump the queue to a list
        ovr_list = list(ovr.queue)
        assert len(ovr_list) == top_n
        for i in range(top_n):
            assert len(ovr_list[i][1]) == team_size
        # print the scores of the top n
        for i in range(len(ovr_list)):
            print("Team: ", i, "Score: ", ovr_list[i])
            print(ovr_list[i][0])
        assert(False)
