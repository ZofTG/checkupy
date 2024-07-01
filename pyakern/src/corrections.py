"""
module containing the correction coefficients for resistance
and reactance values.
"""

#! IMPORTS


from typing import Literal

import pandas as pd


#! RAW TO CORRECTED COEFFICIENTS


_coefs = [
    ["LEFT", "ARM", "R", -26.52469483, 0.890449104],
    ["LEFT", "ARM", "X", 2.285094205, 0.641054712],
    ["LEFT", "BODY", "R", -16.67861046, 0.945093853],
    ["LEFT", "BODY", "X", -3.4758113, 0.948008502],
    ["LEFT", "LEG", "R", 32.27067501, 0.927296855],
    ["LEFT", "LEG", "X", 0.89664892, 0.991384925],
    ["LEFT", "TRUNK", "R", -3.466485256, 1.18316196],
    ["LEFT", "TRUNK", "X", 7.4473968, 0.073604247],
    ["LOWER", "BODY", "R", 52.56977552, 0.948773993],
    ["LOWER", "BODY", "X", -0.823281553, 1.00633072],
    ["RIGHT", "ARM", "R", -23.34396035, 0.872451337],
    ["RIGHT", "ARM", "X", 2.614929578, 0.653447308],
    ["RIGHT", "BODY", "R", -0.074877704, 0.91119084],
    ["RIGHT", "BODY", "X", -0.514277526, 0.907606249],
    ["RIGHT", "LEG", "R", 25.18288672, 0.941388917],
    ["RIGHT", "LEG", "X", -1.155987874, 1.066059805],
    ["RIGHT", "TRUNK", "R", -3.218942633, 1.164758399],
    ["RIGHT", "TRUNK", "X", 7.76203773, 0.073428646],
    ["UPPER", "BODY", "R", -63.78991222, 0.901742825],
    ["UPPER", "BODY", "X", 9.520406271, 0.612947206],
]
CORRECTION_COEFFICIENTS = pd.DataFrame(
    _coefs, columns=["SIDE", "REGION", "PARAMETER", "B0", "B1"]
)


#! FUNCTIONS


def _apply(
    val: float,
    side: Literal["RIGHT", "LEFT", "UPPER", "LOWER"],
    region: Literal["BODY", "TRUNK", "ARM", "LEG"],
    param: Literal["R", "X"],
    adjust: bool,
    unadjust: bool,
    coefs: pd.DataFrame,
):
    """
    private method used to manipulate the specific value (val).

    Parameters
    ----------
    val: float
        the input value

    side:Literal['RIGHT', 'LEFT', 'UPPER', 'LOWER']
        the side of interest

    region:Literal['BODY', 'TRUNK', 'ARM', 'LEG']
        the region of interest

    param:Literal['R', 'X']
        the parameter of interest

    adjust: bool
        apply the correction

    unadjust: bool
        remove the correction

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the output value after the application of adjust and/or unadjust
        operations.
    """
    ssb = (coefs.SIDE == side).astype(bool)  # type: ignore
    rrb = (coefs.REGION == region).astype(bool)  # type: ignore
    ppb = (coefs.PARAMETER == param).astype(bool)  # type: ignore
    idx = ssb & rrb & ppb
    b0, b1 = coefs.loc[idx, ["B0", "B1"]].values.astype(float).flatten()
    out = float(val)
    if adjust:
        out = float(out * b1 + b0)
    if unadjust:
        out = float((out - b0) / b1)
    return out


def right_body_r_ohm(
    value: float | int,
    adjust: bool = False,
    unadjust: bool = False,
    coefs: pd.DataFrame = CORRECTION_COEFFICIENTS,
):
    """
    return the right body resistance

    Parameters
    ----------
    value: float | int
        the input data

    adjust: bool (default=False)
        if True linear correction is applied to the data

    unadjust: bool (default=False)
        if True linear correction is removed from the data

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the resistance value
    """
    return _apply(value, "RIGHT", "BODY", "R", adjust, unadjust, coefs)


def right_body_x_ohm(
    value: float | int,
    adjust: bool = False,
    unadjust: bool = False,
    coefs: pd.DataFrame = CORRECTION_COEFFICIENTS,
):
    """
    return the right body reactance

    Parameters
    ----------
    value: float | int
        the input data

    adjust: bool (default=False)
        if True linear correction is applied to the data

    unadjust: bool (default=False)
        if True linear correction is removed from the data

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the reactance value
    """
    return _apply(value, "RIGHT", "BODY", "X", adjust, unadjust, coefs)


def left_body_r_ohm(
    value: float | int,
    adjust: bool = False,
    unadjust: bool = False,
    coefs: pd.DataFrame = CORRECTION_COEFFICIENTS,
):
    """
    return the left body resistance

    Parameters
    ----------
    value: float | int
        the input data

    adjust: bool (default=False)
        if True linear correction is applied to the data

    unadjust: bool (default=False)
        if True linear correction is removed from the data

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the resistance value
    """
    return _apply(value, "LEFT", "BODY", "R", adjust, unadjust, coefs)


def left_body_x_ohm(
    value: float | int,
    adjust: bool = False,
    unadjust: bool = False,
    coefs: pd.DataFrame = CORRECTION_COEFFICIENTS,
):
    """
    return the left body reactance

    Parameters
    ----------
    value: float | int
        the input data

    adjust: bool (default=False)
        if True linear correction is applied to the data

    unadjust: bool (default=False)
        if True linear correction is removed from the data

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the reactance value
    """
    return _apply(value, "LEFT", "BODY", "X", adjust, unadjust, coefs)


def right_arm_r_ohm(
    value: float | int,
    adjust: bool = False,
    unadjust: bool = False,
    coefs: pd.DataFrame = CORRECTION_COEFFICIENTS,
):
    """
    return the right arm resistance

    Parameters
    ----------
    value: float | int
        the input data

    adjust: bool (default=False)
        if True linear correction is applied to the data

    unadjust: bool (default=False)
        if True linear correction is removed from the data

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the resistance value
    """
    return _apply(value, "RIGHT", "ARM", "R", adjust, unadjust, coefs)


def right_arm_x_ohm(
    value: float | int,
    adjust: bool = False,
    unadjust: bool = False,
    coefs: pd.DataFrame = CORRECTION_COEFFICIENTS,
):
    """
    return the right arm reactance

    Parameters
    ----------
    value: float | int
        the input data

    adjust: bool (default=False)
        if True linear correction is applied to the data

    unadjust: bool (default=False)
        if True linear correction is removed from the data

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the reactance value
    """
    return _apply(value, "RIGHT", "ARM", "X", adjust, unadjust, coefs)


def left_arm_r_ohm(
    value: float | int,
    adjust: bool = False,
    unadjust: bool = False,
    coefs: pd.DataFrame = CORRECTION_COEFFICIENTS,
):
    """
    return the left arm resistance

    Parameters
    ----------
    value: float | int
        the input data

    adjust: bool (default=False)
        if True linear correction is applied to the data

    unadjust: bool (default=False)
        if True linear correction is removed from the data

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the resistance value
    """
    return _apply(value, "LEFT", "ARM", "R", adjust, unadjust, coefs)


def left_arm_x_ohm(
    value: float | int,
    adjust: bool = False,
    unadjust: bool = False,
    coefs: pd.DataFrame = CORRECTION_COEFFICIENTS,
):
    """
    return the left arm reactance

    Parameters
    ----------
    value: float | int
        the input data

    adjust: bool (default=False)
        if True linear correction is applied to the data

    unadjust: bool (default=False)
        if True linear correction is removed from the data

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the reactance value
    """
    return _apply(value, "LEFT", "ARM", "X", adjust, unadjust, coefs)


def right_leg_r_ohm(
    value: float | int,
    adjust: bool = False,
    unadjust: bool = False,
    coefs: pd.DataFrame = CORRECTION_COEFFICIENTS,
):
    """
    return the right leg resistance

    Parameters
    ----------
    value: float | int
        the input data

    adjust: bool (default=False)
        if True linear correction is applied to the data

    unadjust: bool (default=False)
        if True linear correction is removed from the data

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the resistance value
    """
    return _apply(value, "RIGHT", "LEG", "R", adjust, unadjust, coefs)


def right_leg_x_ohm(
    value: float | int,
    adjust: bool = False,
    unadjust: bool = False,
    coefs: pd.DataFrame = CORRECTION_COEFFICIENTS,
):
    """
    return the right leg reactance

    Parameters
    ----------
    value: float | int
        the input data

    adjust: bool (default=False)
        if True linear correction is applied to the data

    unadjust: bool (default=False)
        if True linear correction is removed from the data

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the reactance value
    """
    return _apply(value, "RIGHT", "LEG", "X", adjust, unadjust, coefs)


def left_leg_r_ohm(
    value: float | int,
    adjust: bool = False,
    unadjust: bool = False,
    coefs: pd.DataFrame = CORRECTION_COEFFICIENTS,
):
    """
    return the left leg resistance

    Parameters
    ----------
    value: float | int
        the input data

    adjust: bool (default=False)
        if True linear correction is applied to the data

    unadjust: bool (default=False)
        if True linear correction is removed from the data

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the resistance value
    """
    return _apply(value, "LEFT", "LEG", "R", adjust, unadjust, coefs)


def left_leg_x_ohm(
    value: float | int,
    adjust: bool = False,
    unadjust: bool = False,
    coefs: pd.DataFrame = CORRECTION_COEFFICIENTS,
):
    """
    return the left leg reactance

    Parameters
    ----------
    value: float | int
        the input data

    adjust: bool (default=False)
        if True linear correction is applied to the data

    unadjust: bool (default=False)
        if True linear correction is removed from the data

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the reactance value
    """
    return _apply(value, "LEFT", "LEG", "X", adjust, unadjust, coefs)


def right_trunk_r_ohm(
    value: float | int,
    adjust: bool = False,
    unadjust: bool = False,
    coefs: pd.DataFrame = CORRECTION_COEFFICIENTS,
):
    """
    return the right trunk resistance

    Parameters
    ----------
    value: float | int
        the input data

    adjust: bool (default=False)
        if True linear correction is applied to the data

    unadjust: bool (default=False)
        if True linear correction is removed from the data

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the resistance value
    """
    return _apply(value, "RIGHT", "TRUNK", "R", adjust, unadjust, coefs)


def right_trunk_x_ohm(
    value: float | int,
    adjust: bool = False,
    unadjust: bool = False,
    coefs: pd.DataFrame = CORRECTION_COEFFICIENTS,
):
    """
    return the right trunk reactance

    Parameters
    ----------
    value: float | int
        the input data

    adjust: bool (default=False)
        if True linear correction is applied to the data

    unadjust: bool (default=False)
        if True linear correction is removed from the data

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the reactance value
    """
    return _apply(value, "RIGHT", "TRUNK", "X", adjust, unadjust, coefs)


def left_trunk_r_ohm(
    value: float | int,
    adjust: bool = False,
    unadjust: bool = False,
    coefs: pd.DataFrame = CORRECTION_COEFFICIENTS,
):
    """
    return the left trunk resistance

    Parameters
    ----------
    value: float | int
        the input data

    adjust: bool (default=False)
        if True linear correction is applied to the data

    unadjust: bool (default=False)
        if True linear correction is removed from the data

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the resistance value
    """
    return _apply(value, "LEFT", "TRUNK", "R", adjust, unadjust, coefs)


def left_trunk_x_ohm(
    value: float | int,
    adjust: bool = False,
    unadjust: bool = False,
    coefs: pd.DataFrame = CORRECTION_COEFFICIENTS,
):
    """
    return the left trunk reactance

    Parameters
    ----------
    value: float | int
        the input data

    adjust: bool (default=False)
        if True linear correction is applied to the data

    unadjust: bool (default=False)
        if True linear correction is removed from the data

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the reactance value
    """
    return _apply(value, "LEFT", "TRUNK", "X", adjust, unadjust, coefs)


def upper_body_r_ohm(
    value: float | int,
    adjust: bool = False,
    unadjust: bool = False,
    coefs: pd.DataFrame = CORRECTION_COEFFICIENTS,
):
    """
    return the upper body resistance

    Parameters
    ----------
    value: float | int
        the input data

    adjust: bool (default=False)
        if True linear correction is applied to the data

    unadjust: bool (default=False)
        if True linear correction is removed from the data

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the resistance value
    """
    return _apply(value, "UPPER", "BODY", "R", adjust, unadjust, coefs)


def upper_body_x_ohm(
    value: float | int,
    adjust: bool = False,
    unadjust: bool = False,
    coefs: pd.DataFrame = CORRECTION_COEFFICIENTS,
):
    """
    return the right leg reactance

    Parameters
    ----------
    value: float | int
        the input data

    adjust: bool (default=False)
        if True linear correction is applied to the data

    unadjust: bool (default=False)
        if True linear correction is removed from the data

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the reactance value
    """
    return _apply(value, "UPPER", "BODY", "X", adjust, unadjust, coefs)


def lower_body_r_ohm(
    value: float | int,
    adjust: bool = False,
    unadjust: bool = False,
    coefs: pd.DataFrame = CORRECTION_COEFFICIENTS,
):
    """
    return the lower body resistance

    Parameters
    ----------
    value: float | int
        the input data

    adjust: bool (default=False)
        if True linear correction is applied to the data

    unadjust: bool (default=False)
        if True linear correction is removed from the data

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the resistance value
    """
    return _apply(value, "LOWER", "BODY", "R", adjust, unadjust, coefs)


def lower_body_x_ohm(
    value: float | int,
    adjust: bool = False,
    unadjust: bool = False,
    coefs: pd.DataFrame = CORRECTION_COEFFICIENTS,
):
    """
    return the lower body reactance

    Parameters
    ----------
    value: float | int
        the input data

    adjust: bool (default=False)
        if True linear correction is applied to the data

    unadjust: bool (default=False)
        if True linear correction is removed from the data

    coefs: pd.DataFrame (optional)
        if provided, the table must be a dataframe table where each row contains
        the conversion coefficients to be applied to one specific parameter.
        The dataframe must have columns: ["SIDE", "REGION", "PARAMETER", "B0", "B1"].

    Returns
    -------
    out: float
        the reactance value
    """
    return _apply(value, "LOWER", "BODY", "X", adjust, unadjust, coefs)


__all__ = [
    "CORRECTION_COEFFICIENTS",
    "right_body_r_ohm",
    "right_body_x_ohm",
    "left_body_r_ohm",
    "left_body_x_ohm",
    "upper_body_r_ohm",
    "upper_body_x_ohm",
    "lower_body_r_ohm",
    "lower_body_x_ohm",
    "right_arm_r_ohm",
    "right_arm_x_ohm",
    "left_arm_r_ohm",
    "left_arm_x_ohm",
    "right_trunk_r_ohm",
    "right_trunk_x_ohm",
    "left_trunk_r_ohm",
    "left_trunk_x_ohm",
    "right_leg_r_ohm",
    "right_leg_x_ohm",
    "left_leg_r_ohm",
    "left_leg_x_ohm",
]
