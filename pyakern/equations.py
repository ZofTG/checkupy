"""module dedicated to the integration of akern data"""

#! IMPORTS


from math import atan, pi
from typing import Literal

#! FUNCTIONS


def phase_angle_deg(
    res: float | int,
    rea: float | int,
):
    """
    return the phase angle

    Parameters
    ----------
    res: float | int
        the resistance value

    rea: float | int
        the reactance value

    Returns
    -------
    angle: float
        the phase angle in degrees
    """
    resistance = float(res)
    reactance = float(rea)
    return float(atan(reactance / resistance)) * 180 / pi


def tbw_std_lt(
    res: float | int,
    rea: float | int,
    hcm: float | int,
    wgt: float | int,
    age: int,
    sex: Literal["M", "F"],
):
    """
    return the total body water

    Parameters
    ----------
    res: float | int
        the resistance value

    rea: float | int
        the reactance value

    hcm: float | int
        the user height in cm

    weight: float | int
        the user weight in kg

    age: int
        the age of the user

    sex: Literal['M', 'F']
        the sex of the user

    Returns
    -------
    value: float
        the predicted value
    """
    if sex == "M":
        return float(+1.2 + 0.45 * float(hcm) ** 2 / float(res) + 0.18 * float(wgt))
    return float(+3.75 + 0.45 * float(hcm) ** 2 / float(res) + 0.11 * float(wgt))


def tbw_atl_lt(
    res: float | int,
    rea: float | int,
    hcm: float | int,
    wgt: float | int,
    age: int,
    sex: Literal["M", "F"],
):
    """
    return the total body water

    Parameters
    ----------
    res: float | int
        the resistance value

    rea: float | int
        the reactance value

    hcm: float | int
        the user height in cm

    weight: float | int
        the user weight in kg

    age: int
        the age of the user

    sex: Literal['M', 'F']
        the sex of the user

    Returns
    -------
    value: float
        the predicted value
    """
    return float(
        +0.286
        + 0.195 * float(hcm) ** 2 / float(res)
        + 0.385 * float(wgt)
        + 5.086 * (sex == "M")
    )


def ecw_std_lt(
    res: float | int,
    rea: float | int,
    hcm: float | int,
    wgt: float | int,
    age: int,
    sex: Literal["M", "F"],
):
    """
    return the extracellular water

    Parameters
    ----------
    res: float | int
        the resistance value

    rea: float | int
        the reactance value

    hcm: float | int
        the user height in cm

    weight: float | int
        the user weight in kg

    age: int
        the age of the user

    sex: Literal['M', 'F']
        the sex of the user

    Returns
    -------
    value: float
        the predicted value
    """
    return float(
        -5.22
        + 0.2 * float(hcm) ** 2 / float(res)
        + 0.005 * float(hcm) ** 2 / float(rea)
        + 1.86 * (sex == "F")
        + 0.08 * float(wgt)
        + 1.9
    )


def ecw_atl_lt(
    res: float | int,
    rea: float | int,
    hcm: float | int,
    wgt: float | int,
    age: int,
    sex: Literal["M", "F"],
):
    """
    return the extracellular water

    Parameters
    ----------
    res: float | int
        the resistance value

    rea: float | int
        the reactance value

    hcm: float | int
        the user height in cm

    weight: float | int
        the user weight in kg

    age: int
        the age of the user

    sex: Literal['M', 'F']
        the sex of the user

    Returns
    -------
    value: float
        the predicted value
    """
    return float(
        +1.579
        + 0.055 * float(hcm) ** 2 / float(res)
        + 0.127 * float(wgt)
        + 0.006 * float(hcm) ** 2 / float(rea)
        + 0.932 * (sex == "M")
    )


def icw_std_lt(
    res: float | int,
    rea: float | int,
    hcm: float | int,
    wgt: float | int,
    age: int,
    sex: Literal["M", "F"],
):
    """
    return the intracellular water

    Parameters
    ----------
    res: float | int
        the resistance value

    rea: float | int
        the reactance value

    hcm: float | int
        the user height in cm

    weight: float | int
        the user weight in kg

    age: int
        the age of the user

    sex: Literal['M', 'F']
        the sex of the user

    Returns
    -------
    value: float
        the predicted value
    """
    return tbw_std_lt(res, rea, hcm, wgt, age, sex) - ecw_std_lt(
        res, rea, hcm, wgt, age, sex
    )


def icw_atl_lt(
    res: float | int,
    rea: float | int,
    hcm: float | int,
    wgt: float | int,
    age: int,
    sex: Literal["M", "F"],
):
    """
    return the intracellular water

    Parameters
    ----------
    res: float | int
        the resistance value

    rea: float | int
        the reactance value

    hcm: float | int
        the user height in cm

    weight: float | int
        the user weight in kg

    age: int
        the age of the user

    sex: Literal['M', 'F']
        the sex of the user

    Returns
    -------
    value: float
        the predicted value
    """
    return tbw_atl_lt(res, rea, hcm, wgt, age, sex) - ecw_atl_lt(
        res, rea, hcm, wgt, age, sex
    )


def ffm_std_kg(
    res: float | int,
    rea: float | int,
    hcm: float | int,
    wgt: float | int,
    age: int,
    sex: Literal["M", "F"],
):
    """
    return the free-fat mass

    Parameters
    ----------
    res: float | int
        the resistance value

    rea: float | int
        the reactance value

    hcm: float | int
        the user height in cm

    weight: float | int
        the user weight in kg

    age: int
        the age of the user

    sex: Literal['M', 'F']
        the sex of the user

    Returns
    -------
    value: float
        the predicted value
    """
    ffm = (
        +12.299
        - 0.116 * float(res) / (hcm / 100) ** 2
        + 0.164 * wgt
        + 0.365 * float(res) / (hcm / 100) ** 2
        + 7.827 * (sex == "M")
        + 0.2157 * hcm
    )
    bmi = wgt / (hcm / 100) ** 2
    if bmi >= 30:
        ffm -= 0.256 * (bmi - 30)
    return ffm


def ffm_atl_kg(
    res: float | int,
    rea: float | int,
    hcm: float | int,
    wgt: float | int,
    age: int,
    sex: Literal["M", "F"],
):
    """
    return the free-fat mass

    Parameters
    ----------
    res: float | int
        the resistance value

    rea: float | int
        the reactance value

    hcm: float | int
        the user height in cm

    weight: float | int
        the user weight in kg

    age: int
        the age of the user

    sex: Literal['M', 'F']
        the sex of the user

    Returns
    -------
    value: float
        the predicted value
    """
    return float(
        -2.261
        + 0.327 * float(hcm) ** 2 / float(res)
        + 0.525 * float(wgt)
        + 5.462 * (sex == "M")
    )


def fm_std_kg(
    res: float | int,
    rea: float | int,
    hcm: float | int,
    wgt: float | int,
    age: int,
    sex: Literal["M", "F"],
):
    """
    return the fat mass

    Parameters
    ----------
    res: float | int
        the resistance value

    rea: float | int
        the reactance value

    hcm: float | int
        the user height in cm

    weight: float | int
        the user weight in kg

    age: int
        the age of the user

    sex: Literal['M', 'F']
        the sex of the user

    Returns
    -------
    value: float
        the predicted value
    """
    return wgt - ffm_std_kg(res, rea, hcm, wgt, age, sex)


def fm_atl_kg(
    res: float | int,
    rea: float | int,
    hcm: float | int,
    wgt: float | int,
    age: int,
    sex: Literal["M", "F"],
):
    """
    return the fat mass

    Parameters
    ----------
    res: float | int
        the resistance value

    rea: float | int
        the reactance value

    hcm: float | int
        the user height in cm

    weight: float | int
        the user weight in kg

    age: int
        the age of the user

    sex: Literal['M', 'F']
        the sex of the user

    Returns
    -------
    value: float
        the predicted value
    """
    return wgt - ffm_std_kg(res, rea, hcm, wgt, age, sex)


def smm_std_kg(
    res: float | int,
    rea: float | int,
    hcm: float | int,
    wgt: float | int,
    age: int,
    sex: Literal["M", "F"],
):
    """
    return the skeletal muscle mass

    Parameters
    ----------
    res: float | int
        the resistance value

    rea: float | int
        the reactance value

    hcm: float | int
        the user height in cm

    weight: float | int
        the user weight in kg

    age: int
        the age of the user

    sex: Literal['M', 'F']
        the sex of the user

    Returns
    -------
    value: float
        the predicted value
    """
    return float(
        +5.102
        + 0.401 * float(hcm) ** 2 / float(res)
        - 0.071 * int(age)
        + 3.825 * (sex == "M")
    )


def smm_atl_kg(
    res: float | int,
    rea: float | int,
    hcm: float | int,
    wgt: float | int,
    age: int,
    sex: Literal["M", "F"],
):
    """
    return the skeletal muscle mass

    Parameters
    ----------
    res: float | int
        the resistance value

    rea: float | int
        the reactance value

    hcm: float | int
        the user height in cm

    weight: float | int
        the user weight in kg

    age: int
        the age of the user

    sex: Literal['M', 'F']
        the sex of the user

    Returns
    -------
    value: float
        the predicted value
    """
    return smm_std_kg(res, rea, hcm, wgt, age, sex)


def _trunk_appendicular_index(
    ltres: float | int,
    rtres: float | int,
    lares: float | int,
    rares: float | int,
    llres: float | int,
    rlres: float | int,
):
    """
    return the ratio between the trunk and appendicular resistance

    Parameters
    ----------
    ltres: float | int
        the left trunk resistance

    rtres: float | int
        the right trunk resistance

    lares: float | int
        the left arm resistance

    rares: float | int
        the right arm resistance

    llres: float | int
        the left leg resistance

    rlres: float | int
        the right leg resistance

    Returns
    -------
    value: float
        the predicted value
    """
    num = (ltres + rtres) / 2
    den = (lares + rares + llres + rlres) / 4
    return num / den


def smm_left_arm_kg(data: pd.Series):
    """
    return the skeletal muscle mass of the left arm

    Parameters
    ----------
    data: pd:Series
        a set of info about the user

    Returns
    -------
    value: float
        the predicted value
    """
    return float(
        +0.676
        + 0.026 * float(data.Height) ** 2 / float(data.LeftArmResistance)
        - 11.398 * _trunk_appendicular_index(data)
        + 0.346 * (data.Gender == "M")
    )


def smm_right_arm_kg(data: pd.Series):
    """
    return the skeletal muscle mass of the right arm

    Parameters
    ----------
    data: pd:Series
        a set of info about the user

    Returns
    -------
    value: float
        the predicted value
    """
    return float(
        +1.034
        + 0.024 * float(data.Height) ** 2 / float(data.RightArmResistance)
        - 12.272 * _trunk_appendicular_index(data)
        + 0.388 * (data.Gender == "M")
    )


def smm_left_leg_kg(data: pd.Series):
    """
    return the skeletal muscle mass of the left leg

    Parameters
    ----------
    data: pd:Series
        a set of info about the user

    Returns
    -------
    value: float
        the predicted value
    """
    return float(
        +4.756
        + 0.067 * float(data.Height) ** 2 / float(data.LeftLegResistance)
        - 54.597 * _trunk_appendicular_index(data)
        + 0.901 * (data.Gender == "M")
    )


def smm_right_leg_kg(data: pd.Series):
    """
    return the skeletal muscle mass of the right arm

    Parameters
    ----------
    data: pd:Series
        a set of info about the user

    Returns
    -------
    value: float
        the predicted value
    """
    return float(
        +3.724
        + 0.071 * float(data.Height) ** 2 / float(data.RightLegResistance)
        - 46.197 * _trunk_appendicular_index(data)
        + 0.733 * (data.Gender == "M")
    )


def bmr_std_kcal(data: pd.Series):
    """
    return the basal metabolic rate

    Parameters
    ----------
    data: pd:Series
        a set of info about the user

    Returns
    -------
    value: float
        the predicted value
    """
    bmi = float(data.Weight) / (float(data.Height) / 100) ** 2
    if bmi >= 30:
        return float(
            +478.23
            + 18.72 * ffm_std_kg(data)
            + 5.83 * fm_std_kg(data)
            - 2.55 * int(data.Age)
        )
    return float(
        238.85
        * (
            +0.05192 * ffm_std_kg(data)
            + 0.04036 * fm_std_kg(data)
            + 0.869 * (data.Gender == "M")
            - 0.01181 * int(data.Age)
            + 2.992
        )
    )


def bmr_atl_kcal(data: pd.Series):
    """
    return the basal metabolic rate

    Parameters
    ----------
    data: pd:Series
        a set of info about the user

    Returns
    -------
    value: float
        the predicted value
    """
    return 22.771 * ffm_atl_kg(data) + 484.264


__all__ = [
    "phase_angle_deg",
    "tbw_std_lt",
    "tbw_atl_lt",
    "ecw_std_lt",
    "ecw_atl_lt",
    "icw_std_lt",
    "icw_atl_lt",
    "ffm_std_kg",
    "ffm_atl_kg",
    "fm_std_kg",
    "fm_atl_kg",
    "smm_std_kg",
    "smm_atl_kg",
    "smm_left_arm_kg",
    "smm_left_leg_kg",
    "smm_right_arm_kg",
    "smm_right_leg_kg",
    "bmr_std_kcal",
    "bmr_atl_kcal",
]
