"""module dedicated to the integration of akern data"""

#! IMPORTS


from math import atan, pi, exp, log
from typing import Literal


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
    def phase_angle_left_arm(self):
        """return the left arm phase angle in degrees"""
        return self._phase_angle_deg(self.left_arm_r, self.left_arm_x)

    @property
    def phase_angle_left_leg(self):
        """return the left leg phase angle in degrees"""
        return self._phase_angle_deg(self.left_leg_r, self.left_leg_x)

    @property
    def phase_angle_left_trunk(self):
        """return the left trunk phase angle in degrees"""
        return self._phase_angle_deg(self.left_trunk_r, self.left_trunk_x)

    @property
    def phase_angle_left_body(self):
        """return the left body phase angle in degrees"""
        return self._phase_angle_deg(self.left_body_r, self.left_body_x)

    @property
    def phase_angle_right_arm(self):
        """return the right arm phase angle in degrees"""
        return self._phase_angle_deg(self.right_arm_r, self.right_arm_x)

    @property
    def phase_angle_left_left(self):
        """return the right leg phase angle in degrees"""
        return self._phase_angle_deg(self.right_leg_r, self.right_leg_x)

    @property
    def phase_angle_right_trunk(self):
        """return the right trunk phase angle in degrees"""
        return self._phase_angle_deg(self.right_trunk_r, self.right_trunk_x)

    @property
    def phase_angle_right_body(self):
        """return the right body phase angle in degrees"""
        return self._phase_angle_deg(self.right_body_r, self.right_body_x)

    @property
    def phase_angle_upper_body(self):
        """return the upper body phase angle in degrees"""
        return self._phase_angle_deg(self.upper_body_r, self.upper_body_x)

    @property
    def phase_angle_lower_body(self):
        """return the lower body phase angle in degrees"""
        return self._phase_angle_deg(self.lower_body_r, self.lower_body_x)

    def is_male(self):
        """return True if the user is declared as male"""
        return self.sex == "M"

    @property
    def total_body_water(self):
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
    def extra_cellular_water(self):
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
        if self.is_male():
            b0, b1, b2 = [12.869253, -0.023729, 0.014285]
        else:
            b0, b1, b2 = [-1.831863, 0.717955, 0.018176]
        ecw = b0 + b1 * lt + b2 * lt**2
        tbw = self.tbw_std[0]  # type: ignore
        rl = (ecw / tbw) if tbw is not None else None
        return ecw, rl

    @property
    def intra_cellular_water(self):
        """return the intracellular water in liters and as percentage
        of the total body water"""
        tbw_lt, tbw_rl = self.total_body_water  # type: ignore
        ecw_lt, ecw_rl = self.extra_cellular_water  # type: ignore
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

    @property
    def fat_free_mass(self):
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
        if self.bmi >= 30:
            ffm = ffm - 0.256 * (self.bmi - 30)
        if self.is_male():
            b0, b1, b2 = [40.949695, -0.393518, 0.017217]
        else:
            b0, b1, b2 = [50.468441, -1.532617, 0.047251]
        ffm = b0 + b1 * ffm + b2 * ffm**2
        return ffm, ffm / self.weight

    @property
    def fat_mass(self):
        """return the fat mass in kg and as percentage of the total body weight"""
        if any(self._nones(self.fat_free_mass)):
            return None, None
        ffm_kg, ffm_rl = self.fat_free_mass
        return float(self.weight - ffm_kg), float(1 - ffm_rl)  # type: ignore

    @property
    def bone_mineral_content(self):
        """return the bone mineral content in kg and as percentage of the
        user body weight"""
        if any(self._nones(self.right_body_r)):
            return None, None
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

    @property
    def lean_soft_mass(self):
        """return the lean soft mass in kg and as percentage of the user
        body weight"""
        bmc_kg, bmc_rl = self.bone_mineral_content
        ffm_kg, ffm_rl = self.fat_free_mass
        if any(self._nones(ffm_kg, bmc_kg)):
            lst_kg = None
        else:
            lst_kg = float(ffm_kg - bmc_kg)  # type: ignore
        if any(self._nones(ffm_rl, bmc_rl)):
            lst_rl = None
        else:
            lst_rl = float(ffm_rl - bmc_rl)  # type: ignore
        return lst_kg, lst_rl

    @property
    def skeletal_muscle_mass(self):
        """return the skeletal muscle mass in kg and as percentage of the total body weight"""
        if any(self._nones(self.right_body_r)):
            return None, None
        smm = float(
            +5.102
            + 0.401 * self.height**2 / self.right_body_r  # type: ignore
            - 0.071 * self.age
            + 3.825 * self.is_male()
        )
        if self.is_male():
            b0, b1, b2 = [132.992926, -7.665973, 0.146171]
        else:
            b0, b1, b2 = [26.291962, -1.826563, 0.083549]
        smm = b0 + b1 * smm + b2 * smm**2
        return smm, smm / self.weight

    @property
    def organs_mass(self):
        """return the mass of organs in kg and as percentage of the total body weight"""
        smm_kg, smm_rl = self.skeletal_muscle_mass
        lst_kg, lst_rl = self.lean_soft_mass
        if any(self._nones(lst_kg, smm_kg)):
            orm_kg = None
        else:
            orm_kg = float(ffm_kg - bmc_kg)  # type: ignore
        if any(self._nones(smm_rl, lst_rl)):
            orm_rl = None
        else:
            orm_rl = float(lst_rl - smm_rl)  # type: ignore
        return orm_kg, orm_rl

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
    def skeletal_muscle_mass_left_arm(self):
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
    def skeletal_muscle_mass_right_arm(self):
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
    def skeletal_muscle_mass_left_leg(self):
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
    def skeletal_muscle_mass_right_leg(self):
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
    def basal_metabolic_rate(self):
        """return the basal metabolic rate in kcal"""
        ffm_kg = self.fat_free_mass[0]
        if any(self._nones(ffm_kg)):
            return None
        fm_kg = self.weight - ffm_kg  # type: ignore
        return float(
            +238.85
            * (
                +0.05192 * ffm_kg  # type: ignore
                + 0.04036 * fm_kg  # type: ignore
                + 0.869 * self.is_male()
                - 0.01181 * self.age
                + 2.992
            )
        )

    def to_dict(self):
        """return all the measures as dictionary"""
        return {
            i: getattr(self, i)
            for i in dir(self)
            if i.split("_")[0] not in ["set", "to", "", "is"]
        }


__all__ = ["BIAMeasure"]
