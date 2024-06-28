"""module dedicated to the integration of akern data"""

#! IMPORTS


from math import atan, pi, exp, log
from typing import Literal
from os.path import join


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
    _left_arm_r: float
    _left_arm_x: float
    _left_trunk_r: float
    _left_trunk_x: float
    _left_leg_r: float
    _left_leg_x: float
    _left_body_r: float
    _left_body_x: float
    _right_arm_r: float
    _right_arm_x: float
    _right_trunk_r: float
    _right_trunk_x: float
    _right_leg_r: float
    _right_leg_x: float
    _right_body_r: float
    _right_body_x: float
    _upper_body_r: float
    _upper_body_x: float
    _lower_body_r: float
    _lower_body_x: float

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

    def set_left_arm_r(self, r: int | float):
        """set the left arm resistance in Ohm"""
        self._left_arm_r = float(r)

    def set_left_arm_x(self, x: int | float):
        """set the left arm reactance in Ohm"""
        self._left_arm_x = float(x)

    def set_left_leg_r(self, r: int | float):
        """set the left leg resistance in Ohm"""
        self._left_leg_r = float(r)

    def set_left_leg_x(self, x: int | float):
        """set the left leg reactance in Ohm"""
        self._left_leg_x = float(x)

    def set_left_trunk_r(self, r: int | float):
        """set the left trunk resistance in Ohm"""
        self._left_trunk_r = float(r)

    def set_left_trunk_x(self, x: int | float):
        """set the left trunk reactance in Ohm"""
        self._left_trunk_x = float(x)

    def set_left_body_r(self, r: int | float):
        """set the left body resistance in Ohm"""
        self._left_body_r = float(r)

    def set_left_body_x(self, x: int | float):
        """set the left body reactance in Ohm"""
        self._left_body_x = float(x)

    def set_right_arm_r(self, r: int | float):
        """set the right arm resistance in Ohm"""
        self._right_arm_r = float(r)

    def set_right_arm_x(self, x: int | float):
        """set the right arm reactance in Ohm"""
        self._right_arm_x = float(x)

    def set_right_leg_r(self, r: int | float):
        """set the right leg resistance in Ohm"""
        self._right_leg_r = float(r)

    def set_right_leg_x(self, x: int | float):
        """set the right leg reactance in Ohm"""
        self._right_leg_x = float(x)

    def set_right_trunk_r(self, r: int | float):
        """set the right trunk resistance in Ohm"""
        self._right_trunk_r = float(r)

    def set_right_trunk_x(self, x: int | float):
        """set the right trunk reactance in Ohm"""
        self._right_trunk_x = float(x)

    def set_right_body_r(self, r: int | float):
        """set the right body resistance in Ohm"""
        self._right_body_r = float(r)

    def set_right_body_x(self, x: int | float):
        """set the right body reactance in Ohm"""
        self._right_body_x = float(x)

    def set_upper_body_r(self, r: int | float):
        """set the upper body resistance in Ohm"""
        self._upper_body_r = float(r)

    def set_upper_body_x(self, x: int | float):
        """set the upper body reactance in Ohm"""
        self._upper_body_x = float(x)

    def set_lower_body_r(self, r: int | float):
        """set the lower body resistance in Ohm"""
        self._lower_body_r = float(r)

    def set_lower_body_x(self, x: int | float):
        """set the lower body reactance in Ohm"""
        self._upper_body_x = float(x)

    def __init__(
        self,
        age: int | float,
        sex: Literal["M", "F"],
        hcm: int,
        wgt: int | float,
        left_arm_r: int | float,
        left_arm_x: int | float,
        left_trunk_r: int | float,
        left_trunk_x: int | float,
        left_leg_r: int | float,
        left_leg_x: int | float,
        left_body_r: int | float,
        left_body_x: int | float,
        right_arm_r: int | float,
        right_arm_x: int | float,
        right_trunk_r: int | float,
        right_trunk_x: int | float,
        right_leg_r: int | float,
        right_leg_x: int | float,
        right_body_r: int | float,
        right_body_x: int | float,
        upper_body_r: int | float,
        upper_body_x: int | float,
        lower_body_r: int | float,
        lower_body_x: int | float,
    ):
        self.set_age(age)
        self.set_sex(sex)
        self.set_height(hcm)
        self.set_weight(wgt)

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

    def _phase_angle_deg(self, res: float, rea: float):
        """return the phase angle in degrees"""
        return float(atan(self.left_arm_x / self.left_arm_r)) * 180 / pi

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
        if self.is_male():
            lt = +1.20 + 0.45 * self.height**2 / self.right_body_r + 0.18 * self.weight
        else:
            lt = +3.75 + 0.45 * self.height**2 / self.right_body_r + 0.11 * self.weight
        return lt, lt / self.weight

    @property
    def tbw_atl(self):
        """return the total body water in liters and as percentage
        of the total body weight"""
        lt = (
            +0.286
            + 0.195 * self.height**2 / self.right_body_r
            + 0.385 * self.weight
            + 5.086 * self.is_male()
        )
        return lt, lt / self.weight

    @property
    def ecw_std(self):
        """return the extracellular water in liters and as percentage
        of the total body water"""
        lt = (
            -5.22
            + 0.2 * self.height**2 / self.right_body_r
            + 0.005 * self.height**2 / self.right_body_x
            + 1.86 * ~self.is_male()
            + 0.08 * self.weight
            + 1.9
        )
        return lt, lt / self.tbw_std[0]

    @property
    def ecw_atl(self):
        """return the extracellular water in liters and as percentage
        of the total body water"""
        lt = (
            +1.579
            + 0.055 * self.height**2 / self.right_body_r
            + 0.127 * self.weight
            + 0.006 * self.height**2 / self.right_body_x
            + 0.932 * self.is_male()
        )
        return lt, lt / self.tbw_atl[0]

    @property
    def icw_std(self):
        """return the intracellular water in liters and as percentage
        of the total body water"""
        tbw_lt, tbw_rl = self.tbw_std
        ecw_lt, ecw_rl = self.ecw_std
        return tbw_lt - ecw_lt, tbw_rl - ecw_rl

    @property
    def icw_atl(self):
        """return the intracellular water in liters and as percentage
        of the total body water"""
        tbw_lt, tbw_rl = self.tbw_atl
        ecw_lt, ecw_rl = self.ecw_atl
        return tbw_lt - ecw_lt, tbw_rl - ecw_rl

    @property
    def bmi(self):
        """return the user BMI"""
        return self.weight / (self.height / 100)

    @property
    def ffm_std(self):
        """return the free-fat mass in kg and as percentage
        of the total body weight"""
        # ffm = (
        #     +12.299
        #     - 0.116 * self.right_body_r / (self.height / 100) ** 2
        #     + 0.164 * self.weight
        #     + 0.365 * self.right_body_x / (self.height / 100) ** 2
        #     + 7.827 * self.is_male()
        #     + 0.2157 * self.height
        # )
        # if self.bmi >= 30:
        #     ffm -= 0.256 * (self.bmi - 30)
        lst_kg, lst_pr = self.lst_std
        bmc_kg, bmc_pr = self.bmc
        return lst_kg + bmc_kg, lst_pr + bmc_pr

    @property
    def ffm_atl(self):
        """return the free-fat mass in kg and as percentage
        of the total body weight"""
        ffm = (
            -2.261
            + 0.327 * self.height**2 / self.right_body_r
            + 0.525 * self.weight
            + 5.462 * self.is_male()
        )
        return ffm, ffm / self.weight

    @property
    def fm_std(self):
        """return the fat mass in kg and as percentage of the total body weight"""
        ffm_kg, ffm_rl = self.ffm_std
        return self.weight - ffm_kg, 1 - ffm_rl

    @property
    def fm_atl(self):
        """return the fat mass in kg and as percentage of the total body weight"""
        ffm_kg, ffm_rl = self.ffm_atl
        return self.weight - ffm_kg, 1 - ffm_rl

    @property
    def smm_std(self):
        """return the skeletal muscle mass in kg and as percentage of the total body weight"""
        smm = (
            +5.102
            + 0.401 * self.height**2 / self.right_body_r
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
        return (
            2
            * (self.left_trunk_r + self.right_trunk_r)
            / (self.left_arm_r + self.left_leg_r + self.right_arm_r + self.right_leg_r)
        )

    @property
    def smm_left_arm(self):
        """return the left arm skeletal muscle mass in kg and as percentage of
        the user weight"""
        smm = (
            +0.676
            + 0.026 * self.height**2 / self.left_arm_r
            - 11.398 * self._trunk_appendicular_index
            + 0.346 * self.is_male()
        )
        return smm, smm / self.weight

    @property
    def smm_right_arm(self):
        """return the right arm skeletal muscle mass in kg and as percentage of
        the user weight"""
        smm = (
            +1.034
            + 0.024 * self.height**2 / self.right_arm_r
            - 12.272 * self._trunk_appendicular_index
            + 0.388 * self.is_male()
        )
        return smm, smm / self.weight

    @property
    def smm_left_leg(self):
        """return the left leg skeletal muscle mass in kg and as percentage of
        the user weight"""
        smm = (
            +4.756
            + 0.067 * self.height**2 / self.left_leg_r
            - 54.597 * self._trunk_appendicular_index
            + 0.901 * self.is_male()
        )
        return smm, smm / self.weight

    @property
    def smm_right_leg(self):
        """return the right leg skeletal muscle mass in kg and as percentage of
        the user weight"""
        smm = (
            +3.724
            + 0.071 * self.height**2 / self.left_leg_r
            - 46.197 * self._trunk_appendicular_index
            + 0.733 * self.is_male()
        )
        return smm, smm / self.weight

    @property
    def bmr_std(self):
        """return the basal metabolic rate in kcal"""
        if self.bmi >= 30:
            return (
                +478.23
                + 18.72 * self.ffm_std[0]
                + 5.83 * self.fm_std[0]
                - 2.55 * self.age
            )
        return +238.85 * (
            +0.05192 * self.ffm_std[0]
            + 0.04036 * self.fm_std[0]
            + 0.869 * self.is_male()
            - 0.01181 * self.age
            + 2.992
        )

    @property
    def bmr_atl(self):
        """return the basal metabolic rate in kcal"""
        return 22.771 * self.ffm_atl[0] + 484.264

    @property
    def lst_std(self):
        """return the lean soft tissue in kg and as percentage of the user
        body weight"""
        left_body = (
            +9.016
            + 0.399 * self.height**2 / self.left_body_r
            - 91.962 * self._trunk_appendicular_index
            + 1.229 * self.is_male()
        )
        right_body = (
            +0.461
            + 0.273 * self.height**2 / self.right_body_r
            + 0.006 * self.height**2 / self.right_trunk_r
        )
        lst = left_body + right_body
        # lower_body = +7.998 + 0.284 * self.height ** 2 / self.lower_body_r - 100.561 * self._trunk_appendicular_index + 1.559 * self.is_male()
        # upper_body = +1.560 + 0.102 * self.height ** 2 / self.upper_body_r - 23.420 * self._trunk_appendicular_index + 0.717 * self.is_male()
        # lst = upper_body + lower_body
        return lst, lst / self.weight

    @property
    def bmc(self):
        """return the bone mineral content in kg and as percentage of the
        user body weight"""
        kg = (
            0.89328
            * exp(
                -0.47127 * ln(self.right_body_r) + 2.65176 * ln(self.height) - 9.62779
            )
            - 0.12978 * ~self.is_male()
            + 0.35966
        )
        return kg, kg / self.weight


__all__ = ["BIAMeasure"]
