
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
    team_size = 4
    top_n = 8 
    null_trait_id = trait_dict_inv[""]
    traits_arr = np.zeros(((4 * team_size),))
    t_mask = np.zeros(((4 * team_size),))
    perfect = functools.partial(
        gps.is_perfect_synergy,
        units=units,
        trait_breaks=trait_breaks,
        null_trait_id=null_trait_id,
        traits_arr=traits_arr,
        t_mask=t_mask
    )
    for i in range(4, 9):
            

        ovr = gps.best_of_size(units, i, perfect, top_n, workers=100, chunksize=1000)
        header = f"Found the following teams for team size {i}:"
        print(header)
        lines = []
        for j in range(len(ovr)):
            team_indices = ovr[j][1]
            team_unit_names = [unit_dict[j] for j in team_indices]
            line = "Team: {} Score: {}\n".format(team_unit_names, ovr[j][0])
            lines.append(line)
            print(line)
        # create a new file to write to if it doesn't exist
        fpath = Path("test/app/test_resources/best_of_{}.csv".format(i))
        if not fpath.exists():
            fpath.touch()
        # load the file for writing
        # with open(fpath, "w") as f:
        #     f.writelines(header)
        #     f.writelines(lines)
        break
        

if __name__ == "__main__":
    test_best_of_size()
