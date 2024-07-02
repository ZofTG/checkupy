"""test the BIAMeasure class"""

from os.path import dirname, join
import sys

sys.path += [dirname(dirname(__file__))]
from src import BIAMeasure

if __name__ == "__main__":

    # open the available data
    path = dirname(__file__)
    with open(join(path, "test_data.txt")) as buf:
        lines = buf.readlines()
    headers = lines[0].split("\t")
    headers[-1] = headers[-1].split("\n")[0]
    values = lines[1].split("\t")
    values[-1] = values[-1].split("\n")[0]
    data = dict(zip(headers, values))
    data = {key: str(val) if key == "sex" else float(val) for key, val in data.items()}

    # get the body measurements
    bia = BIAMeasure(**data)  # type: ignore
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
