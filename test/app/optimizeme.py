
import functools
from pathlib import Path
import numpy as np
import src.app.get_perfect_synergies as gps

def perfect():
    units_data_path = Path("test/app/test_resources/champs.csv")
    units, unit_names, unit_names_inv, traits, traits_inv = gps.load_units(units_data_path)
    # load breakpoints
    breakpoints_path = Path("test/app/test_resources/traits.csv")
    breakpoints_sk = gps.load_breakpoints(breakpoints_path)
    trait_breaks = {traits_inv[k]: v for k, v in breakpoints_sk.items()}
    mask_size = max(map(lambda x: len(x), units.values())) * len(units)
    t_mask = np.zeros((mask_size,))
    t= np.zeros((mask_size,))
    return functools.partial(gps.is_perfect_synergy, units=units, trait_breaks=trait_breaks, t_mask=t_mask, t=t)

def test_best_of_size(out_path, team_size, top_n):
    # load champs
    path = Path("test/app/test_resources/champs.csv")
    units, unit_dict, unit_dict_inv, trait_dict, trait_dict_inv = gps.load_units(
        path
    )
    measure = perfect()
    ovr = gps.best_of_size(units, team_size, measure, top_n)
    # dump the queue to a list
    print("Found the following teams:", ovr)
    # for each team, check that it is a perfect synergy
    # print the team with the unit names
    lines = []
    for i in range(len(ovr)):
        team_indices = ovr[i][1]
        team_unit_names = [unit_dict[i] for i in team_indices]
        line = "Team: {} Score: {}\n".format(team_unit_names, ovr[i][0])
        print(line)
        lines.append(line)
    with out_path.open("w") as f:
        f.writelines(lines)


if __name__ == "__main__":
    for i in range(4, 10):
        out_path = Path("test/app/test_resources/best_of_size_" + str(i) + ".csv")
        test_best_of_size(out_path, i, 500)
