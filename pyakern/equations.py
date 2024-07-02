"""module dedicated to the integration of akern data"""

#! IMPORTS


from math import atan, pi, exp, log
from typing import Literal

from .corrections import right_body_r_ohm


#! FUNCTIONS


def ln(x: int | float):
    """return the natural logarithm of x"""
    return log(x, exp(1))


#! CLASS


class BIAMeasure:
    """
    an object with attributes:
        'age': age in years
        'sex': "M" or "F"
        'hcm': height in cm
        'wtg': weight in kg
    in addition the dictionary shall contain additional keys with structure:
    "region"_"side"_"measure" where:
        "region": "arm", "leg", "trunk", "body"
        "side": "left", "right", "upper", "lower"
        "measure": "r", "x"
    all labels should be lower case and provide as value the corresponding
    measure in Ohm.
    """

    _age: int
    _sex: Literal["M", "F"]
    _hcm: int
    _wgt: float
    _left_arm_r: int | float | None
    _left_arm_x: int | float | None
    _left_trunk_r: int | float | None
    _left_trunk_x: int | float | None
    _left_leg_r: int | float | None
    _left_leg_x: int | float | None
    _left_body_r: int | float | None
    _left_body_x: int | float | None
    _right_arm_r: int | float | None
    _right_arm_x: int | float | None
    _right_trunk_r: int | float | None
    _right_trunk_x: int | float | None
    _right_leg_r: int | float | None
    _right_leg_x: int | float | None
    _right_body_r: int | float | None
    _right_body_x: int | float | None
    _upper_body_r: int | float | None
    _upper_body_x: int | float | None
    _lower_body_r: int | float | None
    _lower_body_x: int | float | None

    def set_age(self, age: int | float):
        """set the user age in years"""
        self._age = int(age)

    def set_weight(self, wgt: int | float):
        """set the user weight in kg"""
        self._wgt = float(wgt)

    def set_height(self, hcm: int | float):
        """set the user height in cm"""
        self._hcm = int(hcm)

    def set_sex(self, sex: Literal["M", "F"]):
        """set the user sex"""
        self._sex = sex

    def set_left_arm_r(self, r: int | float | None = None):
        """set the left arm resistance in Ohm"""
        self._left_arm_r = r

    def set_left_arm_x(self, x: int | float | None = None):
        """set the left arm reactance in Ohm"""
        self._left_arm_x = x

    def set_left_leg_r(self, r: int | float | None = None):
        """set the left leg resistance in Ohm"""
        self._left_leg_r = r

    def set_left_leg_x(self, x: int | float | None = None):
        """set the left leg reactance in Ohm"""
        self._left_leg_x = x

    def set_left_trunk_r(self, r: int | float | None = None):
        """set the left trunk resistance in Ohm"""
        self._left_trunk_r = r

    def set_left_trunk_x(self, x: int | float | None = None):
        """set the left trunk reactance in Ohm"""
        self._left_trunk_x = x

    def set_left_body_r(self, r: int | float | None = None):
        """set the left body resistance in Ohm"""
        self._left_body_r = r

    def set_left_body_x(self, x: int | float | None = None):
        """set the left body reactance in Ohm"""
        self._left_body_x = x

    def set_right_arm_r(self, r: int | float | None = None):
        """set the right arm resistance in Ohm"""
        self._right_arm_r = r

    def set_right_arm_x(self, x: int | float | None = None):
        """set the right arm reactance in Ohm"""
        self._right_arm_x = x

    def set_right_leg_r(self, r: int | float | None = None):
        """set the right leg resistance in Ohm"""
        self._right_leg_r = r

    def set_right_leg_x(self, x: int | float | None = None):
        """set the right leg reactance in Ohm"""
        self._right_leg_x = x

    def set_right_trunk_r(self, r: int | float | None = None):
        """set the right trunk resistance in Ohm"""
        self._right_trunk_r = r

    def set_right_trunk_x(self, x: int | float | None = None):
        """set the right trunk reactance in Ohm"""
        self._right_trunk_x = x

    def set_right_body_r(self, r: int | float | None = None):
        """set the right body resistance in Ohm"""
        self._right_body_r = r

    def set_right_body_x(self, x: int | float | None = None):
        """set the right body reactance in Ohm"""
        self._right_body_x = x

    def set_upper_body_r(self, r: int | float | None = None):
        """set the upper body resistance in Ohm"""
        self._upper_body_r = r

    def set_upper_body_x(self, x: int | float | None = None):
        """set the upper body reactance in Ohm"""
        self._upper_body_x = x

    def set_lower_body_r(self, r: int | float | None = None):
        """set the lower body resistance in Ohm"""
        self._lower_body_r = r

    def set_lower_body_x(self, x: int | float | None = None):
        """set the lower body reactance in Ohm"""
        self._upper_body_x = x

    def __init__(
        self,
        age: int | float,
        sex: Literal["M", "F"],
        height: int,
        weight: int | float,
        left_arm_r: int | float | None = None,
        left_arm_x: int | float | None = None,
        left_trunk_r: int | float | None = None,
        left_trunk_x: int | float | None = None,
        left_leg_r: int | float | None = None,
        left_leg_x: int | float | None = None,
        left_body_r: int | float | None = None,
        left_body_x: int | float | None = None,
        right_arm_r: int | float | None = None,
        right_arm_x: int | float | None = None,
        right_trunk_r: int | float | None = None,
        right_trunk_x: int | float | None = None,
        right_leg_r: int | float | None = None,
        right_leg_x: int | float | None = None,
        right_body_r: int | float | None = None,
        right_body_x: int | float | None = None,
        upper_body_r: int | float | None = None,
        upper_body_x: int | float | None = None,
        lower_body_r: int | float | None = None,
        lower_body_x: int | float | None = None,
    ):
        self.set_age(age)
        self.set_sex(sex)
        self.set_height(height)
        self.set_weight(weight)

        self.set_left_arm_r(left_arm_r)
        self.set_left_arm_x(left_arm_x)
        self.set_left_leg_r(left_leg_r)
        self.set_left_leg_x(left_leg_x)
        self.set_left_trunk_r(left_trunk_r)
        self.set_left_trunk_x(left_trunk_x)
        self.set_left_body_r(left_body_r)
        self.set_left_body_x(left_body_x)

        self.set_right_arm_r(right_arm_r)
        self.set_right_arm_x(right_arm_x)
        self.set_right_leg_r(right_leg_r)
        self.set_right_leg_x(right_leg_x)
        self.set_right_trunk_r(right_trunk_r)
        self.set_right_trunk_x(right_trunk_x)
        self.set_right_body_r(right_body_r)
        self.set_right_body_x(right_body_x)

        self.set_upper_body_r(upper_body_r)
        self.set_upper_body_x(upper_body_x)
        self.set_lower_body_r(lower_body_r)
        self.set_lower_body_x(lower_body_x)

    @property
    def age(self):
        """the user age in years"""
        return self._age

    @property
    def weight(self):
        """the user weight in kg"""
        return self._wgt

    @property
    def height(self):
        """the user height in cm"""
        return self._hcm

    @property
    def sex(self):
        """the user sex"""
        return self._sex

    @property
    def left_arm_r(self):
        """the left arm resistance in Ohm"""
        return self._left_arm_r

    @property
    def left_arm_x(self):
        """the left arm reactance in Ohm"""
        return self._left_arm_x

    @property
    def left_leg_r(self):
        """the left leg resistance in Ohm"""
        return self._left_leg_r

    @property
    def left_leg_x(self):
        """set the left leg reactance in Ohm"""
        return self._left_leg_x

    @property
    def left_trunk_r(self):
        """the left trunk resistance in Ohm"""
        return self._left_trunk_r

    @property
    def left_trunk_x(self):
        """the left trunk reactance in Ohm"""
        return self._left_trunk_x

    @property
    def left_body_r(self):
        """the left body resistance in Ohm"""
        return self._left_body_r

    @property
    def left_body_x(self):
        """the left body reactance in Ohm"""
        return self._left_body_x

    @property
    def right_arm_r(self):
        """the right arm resistance in Ohm"""
        return self._right_arm_r

    @property
    def right_arm_x(self):
        """the right arm reactance in Ohm"""
        return self._right_arm_x

    @property
    def right_leg_r(self):
        """the right leg resistance in Ohm"""
        return self._right_leg_r

    @property
    def right_leg_x(self):
        """the right leg reactance in Ohm"""
        return self._right_leg_x

    @property
    def right_trunk_r(self):
        """the right trunk resistance in Ohm"""
        return self._right_trunk_r

    @property
    def right_trunk_x(self):
        """the right trunk reactance in Ohm"""
        return self._right_trunk_x

    @property
    def right_body_r(self):
        """the right body resistance in Ohm"""
        return self._right_body_r

    @property
    def right_body_x(self):
        """the right body reactance in Ohm"""
        return self._right_body_x

    @property
    def upper_body_r(self):
        """the upper body resistance in Ohm"""
        return self._upper_body_r

    @property
    def upper_body_x(self):
        """the upper body reactance in Ohm"""
        return self._upper_body_x

    @property
    def lower_body_r(self):
        """the lower body resistance in Ohm"""
        return self._lower_body_r

    @property
    def lower_body_x(self):
        """the lower body reactance in Ohm"""
        return self._upper_body_x

    def _nones(self, *args):
        """private method to check if any entry is None"""
        return [x is None for x in args]

    def _phase_angle_deg(
        self,
        res: float | int | None,
        rea: float | int | None,
    ):
        """return the phase angle in degrees"""
        if any(self._nones(res, rea)):
            return None
        return float(atan(rea / res)) * 180 / pi  # type: ignore

    @property
    def left_arm_phase_angle_deg(self):
        """return the left arm phase angle in degrees"""
        return self._phase_angle_deg(self.left_arm_r, self.left_arm_x)

    @property
    def left_leg_phase_angle_deg(self):
        """return the left leg phase angle in degrees"""
        return self._phase_angle_deg(self.left_leg_r, self.left_leg_x)

    @property
    def left_trunk_phase_angle_deg(self):
        """return the left trunk phase angle in degrees"""
        return self._phase_angle_deg(self.left_trunk_r, self.left_trunk_x)

    @property
    def left_body_phase_angle_deg(self):
        """return the left body phase angle in degrees"""
        return self._phase_angle_deg(self.left_body_r, self.left_body_x)

    @property
    def right_arm_phase_angle_deg(self):
        """return the right arm phase angle in degrees"""
        return self._phase_angle_deg(self.right_arm_r, self.right_arm_x)

    @property
    def right_leg_phase_angle_deg(self):
        """return the right leg phase angle in degrees"""
        return self._phase_angle_deg(self.right_leg_r, self.right_leg_x)

    @property
    def right_trunk_phase_angle_deg(self):
        """return the right trunk phase angle in degrees"""
        return self._phase_angle_deg(self.right_trunk_r, self.right_trunk_x)

    @property
    def right_body_phase_angle_deg(self):
        """return the right body phase angle in degrees"""
        return self._phase_angle_deg(self.right_body_r, self.right_body_x)

    @property
    def upper_body_phase_angle_deg(self):
        """return the upper body phase angle in degrees"""
        return self._phase_angle_deg(self.upper_body_r, self.upper_body_x)

    @property
    def lower_body_phase_angle_deg(self):
        """return the lower body phase angle in degrees"""
        return self._phase_angle_deg(self.lower_body_r, self.lower_body_x)

    def is_male(self):
        """return True if the user is declared as male"""
        return self.sex == "M"

    @property
    def tbw_std(self):
        """
        return the total body water in liters and as percentage
        of the total body weight
        """
        if any(self._nones(self.right_body_r)):
            return None, None
        if self.is_male():
            lt = float(+1.20 + 0.45 * self.height**2 / self.right_body_r + 0.18 * self.weight)  # type: ignore
        else:
            lt = float(+3.75 + 0.45 * self.height**2 / self.right_body_r + 0.11 * self.weight)  # type: ignore
        return lt, lt / self.weight

    @property
    def tbw_atl(self):
        """return the total body water in liters and as percentage
        of the total body weight"""
        if any(self._nones(self.right_body_r)):
            return None, None
        lt = float(
            +0.286
            + 0.195 * self.height**2 / self.right_body_r  # type: ignore
            + 0.385 * self.weight
            + 5.086 * self.is_male()
        )
        return lt, lt / self.weight

    @property
    def ecw_std(self):
        """return the extracellular water in liters and as percentage
        of the total body water"""
        if any(self._nones(self.right_body_r, self.right_body_x)):
            return None, None
        lt = float(
            -5.22
            + 0.2 * self.height**2 / self.right_body_r  # type: ignore
            + 0.005 * self.height**2 / self.right_body_x  # type: ignore
            + 1.86 * ~self.is_male()
            + 0.08 * self.weight
            + 1.9
        )
        tbw = self.tbw_std[0]  # type: ignore
        rl = (lt / tbw) if tbw is not None else None
        return lt, rl

    @property
    def ecw_atl(self):
        """return the extracellular water in liters and as percentage
        of the total body water"""
        lt = float(
            +1.579
            + 0.055 * self.height**2 / self.right_body_r  # type: ignore
            + 0.127 * self.weight
            + 0.006 * self.height**2 / self.right_body_x  # type: ignore
            + 0.932 * self.is_male()
        )
        tbw = self.tbw_atl[0]  # type: ignore
        rl = (lt / tbw) if tbw is not None else None
        return lt, rl

    @property
    def icw_std(self):
        """return the intracellular water in liters and as percentage
        of the total body water"""
        tbw_lt, tbw_rl = self.tbw_std  # type: ignore
        ecw_lt, ecw_rl = self.ecw_std  # type: ignore
        if any(self._nones(tbw_lt, ecw_lt)):
            icw = None
        else:
            icw = float(tbw_lt - ecw_lt)  # type: ignore
        if any(self._nones(tbw_rl, ecw_rl)):
            rl = None
        else:
            rl = float(tbw_lt - ecw_lt)  # type: ignore
        return icw, rl

    @property
    def icw_atl(self):
        """return the intracellular water in liters and as percentage
        of the total body water"""
        tbw_lt, tbw_rl = self.tbw_atl  # type: ignore
        ecw_lt, ecw_rl = self.ecw_atl  # type: ignore
        if any(self._nones(tbw_lt, ecw_lt)):
            icw = None
        else:
            icw = float(tbw_lt - ecw_lt)  # type: ignore
        if any(self._nones(tbw_rl, ecw_rl)):
            rl = None
        else:
            rl = float(tbw_lt - ecw_lt)  # type: ignore
        return icw, rl

    @property
    def bmi(self):
        """return the user BMI"""
        return self.weight / (self.height / 100) ** 2

    def _correct_for_obese(self, ffm: float):
        """correction for obesity"""
        if self.bmi >= 30:
            return ffm - 0.256 * (self.bmi - 30)
        return ffm

    @property
    def ffm_std(self):
        """return the free-fat mass in kg and as percentage
        of the total body weight"""
        if any(self._nones(self.right_body_r, self.right_body_x)):
            return None, None
        ffm = float(  # kanellakis
            +12.299
            - 0.116 * self.right_body_r / (self.height / 100)  # type: ignore
            + 0.164 * self.weight
            + 0.365 * self.right_body_x / (self.height / 100)  # type: ignore
            + 7.827 * self.is_male()
            + 0.2157 * self.height
        )
        ffm = self._correct_for_obese(ffm)
        return ffm, ffm / self.weight
        # lst_kg, lst_pr = self.lst_std
        # bmc_kg, bmc_pr = self.bmc
        # return lst_kg + bmc_kg, lst_pr + bmc_pr

    @property
    def ffm_atl(self):
        """return the free-fat mass in kg and as percentage
        of the total body weight"""
        if any(self._nones(self.right_body_r)):
            return None, None
        ffm = float(  # Mathias et al. 2021
            -2.261
            + 0.327 * self.height**2 / self.right_body_r  # type: ignore
            + 0.525 * self.weight
            + 5.462 * self.is_male()
        )
        # ffm = (  # campa et al 2023
        #     -7.729
        #     + 0.686 * self.weight
        #     + 1 / 0.227 * (self.height / 100) ** 2 / self.right_body_r  # type: ignore
        #     + 0.086 * self.right_body_x  # type: ignore
        #     + 0.058 * self.age
        # )
        ffm = self._correct_for_obese(ffm)
        return ffm, ffm / self.weight

    @property
    def fm_std(self):
        """return the fat mass in kg and as percentage of the total body weight"""
        if any(self._nones(self.ffm_std)):
            return None, None
        ffm_kg, ffm_rl = self.ffm_std
        return float(self.weight - ffm_kg), float(1 - ffm_rl)  # type: ignore

    @property
    def fm_atl(self):
        """return the fat mass in kg and as percentage of the total body weight"""
        if any(self._nones(self.ffm_atl)):
            return None, None
        ffm_kg, ffm_rl = self.ffm_atl
        return float(self.weight - ffm_kg), float(1 - ffm_rl)  # type: ignore

    @property
    def smm_std(self):
        """return the skeletal muscle mass in kg and as percentage of the total body weight"""
        if any(self._nones(self.right_body_r)):
            return None, None
        smm = float(
            +5.102
            + 0.401 * self.height**2 / self.right_body_r  # type: ignore
            - 0.071 * self.age
            + 3.825 * self.is_male()
        )
        return smm, smm / self.weight

    @property
    def smm_atl(self):
        """return the skeletal muscle mass in kg and as percentage of the total body weight"""
        return self.smm_std

    @property
    def _trunk_appendicular_index(self):
        """return the ratio between the trunk and appendicular resistance"""
        if any(
            self._nones(
                self.left_trunk_r,
                self.right_trunk_r,
                self.left_arm_r,
                self.left_leg_r,
                self.right_arm_r,
                self.right_leg_r,
            )
        ):
            return None
        return (
            2
            * (self.left_trunk_r + self.right_trunk_r)  # type: ignore
            / (self.left_arm_r + self.left_leg_r + self.right_arm_r + self.right_leg_r)  # type: ignore
        )

    @property
    def smm_left_arm(self):
        """return the left arm skeletal muscle mass in kg and as percentage of
        the user weight"""
        if any(self._nones(self.left_arm_r, self._trunk_appendicular_index)):
            return None, None
        smm = float(
            +0.676
            + 0.026 * self.height**2 / self.left_arm_r  # type: ignore
            - 11.398 * self._trunk_appendicular_index  # type: ignore
            + 0.346 * self.is_male()
        )
        return smm, smm / self.weight

    @property
    def smm_right_arm(self):
        """return the right arm skeletal muscle mass in kg and as percentage of
        the user weight"""
        if any(self._nones(self.right_arm_r, self._trunk_appendicular_index)):
            return None, None
        smm = float(
            +1.034
            + 0.024 * self.height**2 / self.right_arm_r  # type: ignore
            - 12.272 * self._trunk_appendicular_index  # type: ignore
            + 0.388 * self.is_male()
        )
        return smm, smm / self.weight

    @property
    def smm_left_leg(self):
        """return the left leg skeletal muscle mass in kg and as percentage of
        the user weight"""
        if any(self._nones(self.left_leg_r, self._trunk_appendicular_index)):
            return None, None
        smm = float(
            +4.756
            + 0.067 * self.height**2 / self.left_leg_r  # type: ignore
            - 54.597 * self._trunk_appendicular_index  # type: ignore
            + 0.901 * self.is_male()
        )
        return smm, smm / self.weight

    @property
    def smm_right_leg(self):
        """return the right leg skeletal muscle mass in kg and as percentage of
        the user weight"""
        if any(self._nones(self.right_leg_r, self._trunk_appendicular_index)):
            return None, None
        smm = float(
            +3.724
            + 0.071 * self.height**2 / self.right_leg_r  # type: ignore
            - 46.197 * self._trunk_appendicular_index  # type: ignore
            + 0.733 * self.is_male()
        )
        return smm, smm / self.weight

    @property
    def bmr_std(self):
        """return the basal metabolic rate in kcal"""
        if any(self._nones(self.ffm_std[0])):
            return None
        if self.bmi >= 30:
            return float(
                +478.23
                + 18.72 * self.ffm_std[0]  # type: ignore
                + 5.83 * self.fm_std[0]  # type: ignore
                - 2.55 * self.age
            )
        return float(
            +238.85
            * (
                +0.05192 * self.ffm_std[0]  # type: ignore
                + 0.04036 * self.fm_std[0]  # type: ignore
                + 0.869 * self.is_male()
                - 0.01181 * self.age
                + 2.992
            )
        )

    @property
    def bmr_atl(self):
        """return the basal metabolic rate in kcal"""
        if any(self._nones(self.ffm_atl[0])):
            return None
        return float(22.771 * self.ffm_atl[0] + 484.264)  # type: ignore

    @property
    def lst_std(self):
        """return the lean soft tissue in kg and as percentage of the user
        body weight"""
        if any(
            self._nones(
                self.left_body_r,
                self.right_body_r,
                self.right_trunk_r,
                self._trunk_appendicular_index,
            )
        ):
            return None, None
        left_body = float(
            +9.016
            + 0.399 * self.height**2 / self.left_body_r  # type: ignore
            - 91.962 * self._trunk_appendicular_index  # type: ignore
            + 1.229 * self.is_male()
        )
        right_body = float(
            +0.461
            + 0.273 * self.height**2 / self.right_body_r  # type: ignore
            + 0.006 * self.height**2 / self.right_trunk_r  # type: ignore
        )
        lst = left_body + right_body
        # if any(
        #    self._nones(
        #        self.upper_body_r,
        #        self.lower_body_r,
        #        self._trunk_appendicular_index,
        #    )
        # ):
        #    return None, None
        # lower_body = float(
        #     +7.998
        #     + 0.284 * self.height**2 / self.lower_body_r  # type: ignore
        #     - 100.561 * self._trunk_appendicular_index  # type: ignore
        #     + 1.559 * self.is_male()
        # )
        # upper_body = float(
        #     +1.560
        #     + 0.102 * self.height**2 / self.upper_body_r  # type: ignore
        #     - 23.420 * self._trunk_appendicular_index  # type: ignore
        #     + 0.717 * self.is_male()
        # )
        # lst = upper_body + lower_body
        return lst, lst / self.weight

    @property
    def lst_atl(self):
        """return the lean soft tissue in kg and as percentage of the user
        body weight"""
        if any(self._nones(self.right_body_r, self.right_body_x)):
            return None, None
        lst = (  # Campa et al. 2023
            -8.929
            + 0.635 * self.weight
            + 1 / 0.227 * (self.height / 100) ** 2 / self.right_body_r  #  type: ignore
            + 0.093 * self.right_body_x  # type: ignore
            + 0.048 * self.age
        )
        return lst, lst / self.weight

    @property
    def bmc(self):
        """return the bone mineral content in kg and as percentage of the
        user body weight"""
        if any(self._nones(self.right_body_r)):
            return None
        kg = float(
            0.89328
            * exp(
                -0.47127 * ln(self.right_body_r)  # type: ignore
                + 2.65176 * ln(self.height)
                - 9.62779
            )
            - 0.12978 * ~self.is_male()
            + 0.35966
        )
        return kg, kg / self.weight

    def to_dict(self):
        """return all the measures as dictionary"""
        return {
            i: getattr(self, i)
            for i in dir(self)
            if i.split("_")[0] not in ["set", "to", "", "is"]
        }


__all__ = ["BIAMeasure"]
