"""utility functions module"""

#! IMPORTS


import pandas as pd


#! FUNCTIONS


__all__ = ["get_id", "read_akern"]


def get_id(x: int):
    """
    adjust the user's id

    Parameters
    ----------
    x: int
        the user's id

    Returns
    -------
    id: str
        the user id as string
    """
    out = str(x)
    while len(out) < 3:
        out = "0" + out
    return out


def _format_condition(con: str):
    """
    return the appropriate label for the testing condition

    Parameters
    ----------
    con : str
        the testing condition code. It should be any of the following:
            'A1': 'STANDING STANDARD GRIP'
            'A2': 'STANDING STRONG GRIP'
            '1': 'STANDING STANDARD GRIP'
            '2': 'STANDING STRONG GRIP'

    Returns
    -------
    condition: str
        the appropriate condition label
    """
    conditions = {
        "A1": "PRESA NORMALE",
        "A2": "PRESA STRETTA",
        "1": "PRESA NORMALE",
        "2": "PRESA STRETTA",
        "PRESA NORMALE": "PRESA NORMALE",
        "PRESA STRETTA": "PRESA STRETTA",
    }
    if con not in list(conditions.keys()):
        raise ValueError(f"{con} must be any of {list(conditions.keys())}")
    return conditions[con]


def _format_timing(con: str):
    """
    return the appropriate label for the testing time

    Parameters
    ----------
    con : str
        the testing time code. It should be any of the following:
            'T0': 'MATTINA'
            'T1': 'SERA'
            '1': 'MATTINA'
            '2': 'SERA'
            '3': 'PREEX'
            '4': 'POSTEX'
            'Tpre': 'PREEX'
            'Tpost': 'POSTEX'
            'MATTINA': 'MATTINA'
            'SERA': 'SERA'
            'PREEX': 'PREEX',
            'POSTEX': 'POSTEX'

    Returns
    -------
    timing: str
        the appropriate timing condition label
    """
    conditions = {
        "T0": "MATTINA",
        "T1": "SERA",
        "1": "MATTINA",
        "2": "SERA",
        "3": "PREEX",
        "4": "POSTEX",
        "Tpre": "PREEX",
        "Tpost": "POSTEX",
        "MATTINA": "MATTINA",
        "SERA": "SERA",
        "PREEX": "PREEX",
        "POSTEX": "POSTEX",
    }
    if con not in list(conditions.keys()):
        raise ValueError(f"{con} must be any of {list(conditions.keys())}")
    return conditions[con]


def _format_time(con: str):
    """
    return the appropriate label for the test time

    Parameters
    ----------
    con : str
        the entry time

    Returns
    -------
    label:
        the output label
    """
    msg = con
    while len(msg) < 6:
        msg = "0" + msg
    return ":".join([msg[:2], msg[2:4], msg[4:]])


def read_akern(file: str):
    """
    read akern data.

    Parameters
    ----------
    file: str
        read the akern data

    Returns
    -------
    data: DataFrame
        the resulting outcomes.
    """

    # read the data
    with open(file, "r", errors="replace") as buf:  # type: ignore
        lines = [i.split(";") for i in buf.read().replace("�", "°").split("\n")]
    lines[0] = lines[0]
    dfr = pd.DataFrame(lines[1:], columns=lines[0]).dropna()

    # format data
    cols = [i.replace(" ", "_").replace("[*]", "") for i in dfr.columns]
    dfr.columns = pd.Index(cols)
    idx = dfr.index
    formats = [("Time", _format_time), ("Id", get_id)]
    formats += [("Condition_tag", _format_condition)]
    formats += [("Timing_tag", _format_timing)]
    for key, fun in formats:
        if dfr.Project.values[0] == "BIA_101_BIVA" and key == "Condition_tag":
            dfr.loc[idx, key] = "DISTESO"
        else:
            dfr.loc[idx, key] = dfr[key].map(fun)  # type: ignore

    # update the columns
    cols = []
    for i in dfr.columns:
        new = i.split("[")[0]
        new = new.replace("_R", "_Resistance").replace("_X", "_Reactance")
        cols += ["".join(j.capitalize() for j in new.lower().split("_")).strip()]
    dfr.columns = pd.Index(cols)

    return dfr
