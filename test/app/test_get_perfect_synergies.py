from cgi import test
import functools
from pathlib import Path
import itertools
import pytest
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
        path = Path("test/app/test_resources/traits.csv")
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
        units, unit_dict, unit_dict_inv, trait_dict, triat_dict_inv = gps.load_units(path)
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
        units, unit_dict, unit_dict_inv, trait_dict, triat_dict_inv = gps.load_units(path)
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
        units, unit_dict, unit_dict_inv, trait_dict, triat_dict_inv = gps.load_units(path)
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
        units, unit_dict, unit_dict_inv, trait_dict, triat_dict_inv = gps.load_units(path)
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
        team_size = 10
        id = 1
        traits_arr = np.zeros((team_size,))
        mask_arr = np.zeros((team_size,))
        alltraits = [1, 2, 3, 1, 1, 1, 1, 1, 1, 1]
        traits_arr[:len(alltraits)] = alltraits
        l = len(alltraits)
        breaks = [3, 5, 7]
        gps.fill_mask(mask_arr, traits_arr, l, id, breaks)
        truth = [1, 0, 0, 1, 1, 1, 1, 1, 1, 0]
        truth_arr = np.zeros((team_size,))
        truth_arr[:len(truth)] = truth
        assert(np.array_equal(truth_arr, mask_arr))
    @pytest.mark.skip(reason="not implemented")
    def test_is_perfect_synergy(self):
        # load champs
        path = Path("test/app/test_resources/champs.csv")
        units, unit_dict, unit_dict_inv, trait_dict, trait_dict_inv = gps.load_units(path)
        # arbitrary team
        team = (0, 1, 2)
        team_size = len(team) * 4
        # print the origins of the tea
        # constructed breakpoints
        # team has
        # syndicate arcanist hextech colossus syndicate sniper
        syn_trait_id = trait_dict_inv["Syndicate"]
        arcan_trait_id = trait_dict_inv["Arcanist"]
        hex_trait_id = trait_dict_inv["Hextech"]
        colo_trait_id = trait_dict_inv["Colossus"]
        sniper_trait_id = trait_dict_inv["Sniper"]
        null_trait_id = trait_dict_inv[""]
        # construct a set of breakpoints that makes the team a perfect synergy
        trait_breaks = {syn_trait_id: [2], arcan_trait_id: [1], hex_trait_id: [1], colo_trait_id: [1], sniper_trait_id: [1]}
        traits_arr = np.zeros((team_size,))
        mask_arr = np.zeros((team_size,))
        print("initial traits array: ", traits_arr)
        print("initial mask array: ", mask_arr)
        pf = functools.partial(gps.is_perfect_synergy, trait_breaks = trait_breaks, null_trait_id = null_trait_id, traits_arr=traits_arr, t_mask = mask_arr, l=0)
        assert pf(units, team)
    def test_is_perfect_synergy2(self):
        # load champs
        path = Path("test/app/test_resources/champs.csv")
        units, unit_dict, unit_dict_inv, trait_dict, trait_dict_inv = gps.load_units(path)
        # load the breakpoints
        tpath = Path("test/app/test_resources/traits.csv")
        breakpoints = gps.load_breakpoints(tpath)
        trait_breaks = {trait_dict_inv[k]: v for k, v in breakpoints.items()}
        # some known perfect synergies
        #t1 = ["Poppy", "Ziggs", "Blitzcrank", "Vex"]
        t1 = ["Ziggs", "Gnar", "Vex", "Irelia"]
        # try looking up the traits for each unit
        # get the indices of the units in the team
        t1_ids = [unit_dict_inv[u] for u in t1]
        team_size = len(t1_ids)
        max_size = team_size * 4
        traits_arr = np.zeros((max_size,))
        mask_arr = np.zeros((max_size,))
        l=0
        null_trait_id = trait_dict_inv[""]
        pf = functools.partial(gps.is_perfect_synergy, trait_breaks = trait_breaks, null_trait_id = null_trait_id, traits_arr=traits_arr, t_mask = mask_arr, l=l)
        assert pf(units, t1_ids)
    def test_is_perfect_synergy3(self):
        # load champs
        path = Path("test/app/test_resources/champs.csv")
        units, unit_dict, unit_dict_inv, trait_dict, trait_dict_inv = gps.load_units(path)
        # load the breakpoints
        tpath = Path("test/app/test_resources/traits.csv")
        breakpoints = gps.load_breakpoints(tpath)
        trait_breaks = {trait_dict_inv[k]: v for k, v in breakpoints.items()}
        # some known perfect synergies
        t1 = ['Ahri', 'Ashe', 'Alistar', 'Braum']
        # try looking up the traits for each unit
        # get the indices of the units in the team
        t1_ids = [unit_dict_inv[u] for u in t1]
        team_size = len(t1_ids)
        max_size = team_size * 4
        traits_arr = np.zeros((max_size,))
        mask_arr = np.zeros((max_size,))
        l=0
        null_trait_id = trait_dict_inv[""]
        pf = functools.partial(gps.is_perfect_synergy, trait_breaks = trait_breaks, null_trait_id = null_trait_id, traits_arr=traits_arr, t_mask = mask_arr, l=l)
        assert not pf(units, t1_ids)
    @pytest.mark.skip(reason="not implemented")
    def test_best_overall(self):
        # load champs
        path = Path("test/app/test_resources/champs.csv")
        units, unit_dict, unit_dict_inv, trait_dict, trait_dict_inv = gps.load_units(path)
        # load origin breaks
        path = Path("test/app/test_resources/traits.csv")
        trait_breaks_sk = gps.load_breakpoints(path)
        trait_breaks = {trait_dict_inv[k]: v for k, v in trait_breaks_sk.items()}
        prefix_size = 2
        team_size = 4
        top_n = 8 
        null_trait_id = trait_dict_inv[""]
        traits_arr = np.zeros((4 * team_size,))
        t_mask = np.zeros((4 * team_size,))
        pf = partial(gps.is_perfect_synergy, trait_breaks=trait_breaks, null_trait_id=null_trait_id, traits_arr = traits_arr, t_mask = t_mask, l=0)
        ovr = gps.best_overall(units, prefix_size, team_size, pf, top_n)
        # dump the queue to a list
        print("Found the following teams:", ovr.queue)
        # for each team, check that it is a perfect synergy
        # print the team with the unit names
        for i in range(top_n):
            team_indices = ovr.queue[i][1]
            team_unit_names = [unit_dict[i] for i in team_indices]
            print("Team: ", team_unit_names, "Score: ", ovr.queue[i][0])
        assert(False)
        for team in ovr.queue:
            print("Team: ", team)
            assert pf(units, team[1])
