"""test the BIAMeasure class"""

from os.path import dirname, join
import sys

sys.path += [dirname(dirname(__file__))]
from checkupy import read_txt

if __name__ == "__main__":

    # open the available data
    path = dirname(__file__)
    for bia, user, date in read_txt(join(path, "test_data.txt")):
        print("\n")
        print(f"userid: {user}")
        print(f"datetime: {date}")
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
