"""test the BIAMeasure class"""

import sys
from datetime import datetime
from os.path import dirname, join

sys.path += [dirname(dirname(__file__))]

from checkupy import CheckupBIA


def read_txt(file: str):
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
    with open(file, encoding="utf8") as buf:
        lines = [i.split("\t") for i in buf.readlines()]

    # adjust the data
    for i in range(4):
        for j in range(1, len(lines[i])):
            val = lines[i][j].replace("\n", "").replace("-", "").replace(" ", "")
            if val == "":
                lines[i][j] = lines[i][j - 1]
    cols = [[i[j] for i in lines] for j in range(len(lines[0]))]
    obj = {}
    for i in cols:

        # get the header
        i[:2] = [i[1], i[0]]
        key = "_".join(i[:3])
        if key.startswith("_"):
            key = key[1:]
        if key.endswith("_"):
            key = key[:-1]
        key = key.lower().replace("\n", "")

        # adjust the values
        if not key.endswith("_ph"):
            vals = []
            for j in i[4:]:
                try:
                    val = float(j)
                except Exception:
                    val = str(j)
                vals += [val]
            obj[key] = vals

    # wrap and sort the tests
    lines = []
    for i in range(len(obj["userid"])):
        user = obj["userid"][i]
        date = obj["test_date"][i]
        time = obj["test_time"][i]
        test_date = datetime.strptime("-".join([date, time]), "%d/%m/%Y-%H:%M:%S")
        bia = {
            j: v[i]
            for j, v in obj.items()
            if j not in ["userid", "test_date", "test_time"]
            and not j.startswith("upper")
            and not j.startswith("lower")
        }
        bia = CheckupBIA(**bia, raw_electric_data=True)
        lines += [(bia, str(user), test_date)]

    # return
    return lines


if __name__ == "__main__":

    # open the available data
    path = dirname(__file__)
    for bia, user, date in read_txt(join(path, "test_data.txt")):
        print("\n")
        print(f"userid: {user}")
        print(f"datetime: {date}")
        print(f"valid: {bia.is_valid()}")
        for i, v in bia.to_dict().items():
            if isinstance(v, tuple):
                t = f"{v[0]:0.3f} ({(v[1]*100):0.1f}%)"
            elif isinstance(v, str):
                t = v
            elif v is None:
                t = ""
            else:
                t = f"{v:0.3f}"
            print(f"{i}: {t}")
