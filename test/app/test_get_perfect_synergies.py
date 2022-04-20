from pathlib import Path
import itertools
import numpy as np
from src.app.get_perfect_synergies import load_units, get_prefixes, get_combinations, get_unused_it

class TestClass:
    def test_get_unused_it(self):
        path = Path("test/app/test_resources/champs.csv")
        units, unit_dict, unit_dict_inv, origin_dict, origin_dict_inv, class_dict, class_dict_inv = load_units(path)
        prefix_size = 2
        prefix = [0, 1]
        unused_it = get_unused_it(units, prefix)
        unused_it_list = list(unused_it)
        # check that the unused_it is the correct length
        assert len(unused_it_list) == units.shape[0] - prefix_size
        # check that unused it does not contain the prefix
        for i in prefix:
            assert i not in unused_it_list
        # check that unused it contains all other indices
        for i in range(units.shape[0]):
            if i not in prefix:
                assert i in unused_it_list

