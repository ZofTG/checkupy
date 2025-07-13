"""test the BIAMeasure class"""

import sys
import itertools as it
from datetime import datetime
from os.path import dirname, join
import numpy as np
import pandas as pd

sys.path += [dirname(dirname(__file__))]

from checkupy import CheckupBIA


def read_file(file: str):
    """
    import data from file.

    Parameters
    ----------
    file: str
        the path of a .txt file properly formatted.

    Returns
    -------
    tests: list[tuple(CheckupBIA, str, datetime)]
        a list containing the available test. Each element of the list is
        one single test (tuple) containing:
            bia: CheckupBIA
                the bia measurement object.

            user: str
                the name of the user

            test_date: datetime
                the datetime object of the test.
    """
    # read the file
    data = pd.read_csv(file, header=[0, 1, 2, 3])
    columns = [list(i)[:2][::-1] + [i[2]] for i in data.columns]  # type: ignore
    columns = [
        "_".join([j for j in i if not "unnamed" in j.lower()])
        .lower()
        .replace("_r", "_resistance")
        .replace("_x", "_reactance")
        for i in columns
    ]
    data.columns = pd.Index(columns)

    # wrap and sort the tests
    lines = []
    for i, line in data.iterrows():
        user = line["userid"]
        date = line["test_date"]
        time = line["test_time"]
        test_date = datetime.strptime("-".join([date, time]), "%d/%m/%Y-%H:%M:%S")
        bia = ["height", "weight", "age", "gender"]
        bia += [
            "_".join(i)
            for i in it.product(
                ["left", "right"],
                ["arm", "leg", "trunk", "body"],
                ["resistance", "reactance"],
            )
        ]
        bia = {i: line[i] for i in bia}
        bia = CheckupBIA(**bia, corrected_electrical_values=False)
        lines += [(bia, str(user), test_date)]

    # return
    return lines


if __name__ == "__main__":

    # open the available data
    path = dirname(__file__)
    for bia, user, date in read_file(join(path, "test_data.csv")):
        print("\n")
        print(f"userid: {user}")
        print(f"datetime: {date}")
        print(f"valid: {bia.fitness.is_valid()}")
        for i, v in bia.to_dict().items():
            if isinstance(v, dict):
                print("\n\t" + i)
                for key, val in v.items():
                    print(f"\t\t{key}: {np.squeeze(val)}")
