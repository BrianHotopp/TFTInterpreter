
import functools
from pathlib import Path
import numpy as np
import src.app.get_perfect_synergies as gps
def test_best_of_size():
    # load champs
    path = Path("test/app/test_resources/champs.csv")
    units, unit_dict, unit_dict_inv, trait_dict, trait_dict_inv = gps.load_units(
        path
    )
    # load origin breaks
    path = Path("test/app/test_resources/traits.csv")
    trait_breaks_sk = gps.load_breakpoints(path)
    trait_breaks = {trait_dict_inv[k]: v for k, v in trait_breaks_sk.items()}
    team_size = 3
    top_n = 8
    null_trait_id = trait_dict_inv[""]
    traits_arr = np.zeros((4 * team_size,))
    t_mask = np.zeros((4 * team_size,))
    perfect = functools.partial(
        gps.is_perfect_synergy,
        units=units,
        trait_breaks=trait_breaks,
        null_trait_id=null_trait_id,
        traits_arr=traits_arr,
        t_mask=t_mask,
    )
    ovr = gps.best_of_size(units, team_size, perfect, top_n)
    # dump the queue to a list
    print("Found the following teams:", ovr)
    # for each team, check that it is a perfect synergy
    # print the team with the unit names
    for i in range(len(ovr)):
        team_indices = ovr[i][1]
        team_unit_names = [unit_dict[i] for i in team_indices]
        print("Team: ", team_unit_names, "Score: ", ovr[i][0])
if __name__ == "__main__":
    test_best_of_size()
